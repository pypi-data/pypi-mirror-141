from __future__ import print_function, absolute_import, division
import logging
import os
import time
import shutil
import re
from errno import ENOENT
import requests
import ujson as json
from tqdm import tqdm
from trieregex import TrieRegEx as TRE
from stat import S_IFDIR, S_IFREG
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn, fuse_get_context


class LocalMixin:
    """
    Perform operations on local FS
    """

    def ensure_local_folder(self, path, name):
        if self.config.enable_local_files:
            newpath = os.path.join(self.local_fs, path.lstrip("/"), name)
            if not os.path.exists(newpath):
                logging.debug(f"MKDIRLOCAL\t{newpath}")
                os.mkdir(newpath)

    def local_truncate(self, path, length, fh=None):
        with open(f"{self.local_fs}{path}", "wb") as fl:
            fl.write("\x00".encode("ascii") * length)

    def local_unlink(self, path):
        return self.local_destroy(path)

    def local_create(self, path, mode):
        with open(f"{self.local_fs}{path}", "w") as fl:
            fl.write("")
        return 0

    def local_destroy(self, path):
        shutil.rmtree(f"{self.local_fs}{path}", ignore_errors=True)

    def local_mkdir(self, path, mode):
        os.mkdir(f"{self.local_fs}{path}")
        return 0

    def local_read(self, path, size, offset, fh):
        with open(f"{self.local_fs}{path}", "rb") as fl:
            fl.seek(offset)
            return fl.read(size)

    def local_readdir(self, path, fh):
        nodes = [
            n for n in os.listdir(f"{self.local_fs}{path}") if n != "." and n != ".."
        ]
        return [".", ".."] + nodes

    def local_write(self, path, data, offset, fh):
        with open(f"{self.local_fs}{path}", "wb") as fl:
            fl.seek(offset)
            fl.write(data)
        return len(data)

    def local_rmdir(self, path):
        shutil.rmtree(f"{self.local_fs}{path}", ignore_errors=True)

    def local_getattr(self, path, fh=None):
        stat = os.stat(f"{self.local_fs}{path}")
        return {
            k: getattr(stat, k)
            for k in [
                "st_gid",
                "st_mode",
                "st_uid",
                "st_atime",
                "st_ctime",
                "st_mtime",
                "st_size",
            ]
        }


class RemoteMixin:
    """
    Perform operations on instabase FS.
    """

    api_cache = {}

    def __flush_api_cache__(self):
        now = int(time.time()) // self.config.invalidate_cache_after_n_seconds
        self.api_cache = {now: {}}
        logging.info(f"FLUSHCACHE\t{now}")

    def __jobapi__(self, job_id):
        url = f"{self.config.instance}{self.config.api}/jobs/status"
        headers = {
            "Authorization": f"Bearer {self.config.token}",
        }
        r = self.session.get(
            url,
            params={"job_id": job_id},
            headers=headers,
            timeout=self.config.api_timeout,
        )
        return r

    def __fsapi__(self, method, path, ib_kwargs=None, *, use_cache=False, **kwargs):
        ib_kwargs = {} if ib_kwargs is None else ib_kwargs
        # Flush cache if it's too old
        now = int(time.time()) // self.config.invalidate_cache_after_n_seconds
        if now not in self.api_cache or method != "get":
            self.__flush_api_cache__()
        # Should we cache?
        fresh_call = True
        cache_key = (method, path, tuple(sorted(ib_kwargs.items())))
        if use_cache and cache_key in self.api_cache[now]:
            fresh_call = False
        logging.debug(f"{'MISS' if fresh_call else 'HIT'}\t {cache_key}")
        if fresh_call:
            url = f"{self.config.instance}{self.config.api}/drives{self.config.folder}"
            url = f"{url}{path}"
            headers = {
                "Authorization": f"Bearer {self.config.token}",
                "Instabase-API-Args": json.dumps(ib_kwargs),
            }
            resp = self.session.request(
                method, url, headers=headers, timeout=self.config.api_timeout, **kwargs
            )
            logging.info(f"API\t{method} {url} {ib_kwargs} {resp.status_code}")
        if use_cache:
            if fresh_call:
                self.api_cache[now][cache_key] = resp
            return self.api_cache[now][cache_key]
        return resp

    def remote_unlink(self, path):
        return self.remote_destroy(path)

    def remote_truncate(self, path, length, fh=None):
        self.remote_write(path, ("\x00".encode("ascii") * length), 0, fh)

    def remote_getattr(self, path, fh=None):
        uid, gid, pid = fuse_get_context()
        st = {}
        r = self.__fsapi__(
            "get", path, {"get_content": False, "get_metadata": True}, use_cache=True
        )
        if r.json()["status"] == "ERROR":
            logging.error(f"APIERROR\t{r.json()}")
            raise FuseOSError(ENOENT)
        meta = r.json()["metadata"]
        st["st_gid"] = gid
        st["st_mode"] = (
            (S_IFDIR | 0o755) if meta["type"] == "folder" else (S_IFREG | 0o700)
        )
        st["st_uid"] = uid
        st["st_atime"] = int(time.time())
        st["st_ctime"] = st["st_mtime"] = meta["modified_timestamp"]
        if "size" in meta and meta["type"] == "file":
            st["st_size"] = meta["size"]
        return st

    def remote_mkdir(self, path, mode):
        r = self.__fsapi__("post", path, {"type": "folder"})
        self.__flush_api_cache__()
        return_code = 0 if r.status_code == 200 else 1
        if return_code == 0:
            self.nodes[path] = {}
        return 0

    def remote_read(self, path, size, offset, fh):
        r = self.__fsapi__(
            "get",
            path,
            {
                "type": "file",
                "get_content": True,
                "range": f"bytes={offset}-{offset+size}",
            },
        )
        return r.content[:size]

    def remote_readdir(self, path, fh):
        children = []
        next_page_token = ""
        count = 0
        while True:
            r = self.__fsapi__(
                "get",
                path,
                {
                    "type": "folder",
                    "get_content": True,
                    "get_metadata": False,
                    "start_page_token": next_page_token,
                },
                use_cache=True,
            )
            if "nodes" not in r.json():
                logging.info(r.json())
            for node in r.json()["nodes"]:
                children.append(node)
                self.nodes[os.path.join(path, node["name"])] = node
            next_page_token = r.json()["next_page_token"]
            if not r.json()["has_more"]:
                logging.debug(f"LISTDIR\t{count} pending {path}")
                break
            logging.debug(f"LISTDIR\t {count} ok {path}")
            count += 1
        paths = [".", ".."] + [node["name"] for node in children]
        return paths

    def remote_write(self, path, data, offset, fh):
        r = self.__fsapi__(
            "post",
            path,
            {"type": "file", "cursor": offset, "if_exists": "overwrite",},
            data=data,
        )
        self.__flush_api_cache__()
        end_cursor = r.json()["cursor"]
        if end_cursor == -1:
            return len(data)
        return end_cursor - offset

    def remote_rmdir(self, path):
        self.__fsapi__("delete", path, {"force": True})
        self.__flush_api_cache__()
        self.nodes.pop(path, None)

    def remote_create(self, path, mode):
        r = self.__fsapi__(
            "post", path, {"type": "file", "if_exists": "overwrite",}, data="",
        )
        self.__flush_api_cache__()
        self.fd += 1
        return self.fd

    def remote_destroy(self, path):
        self.__fsapi__("delete", path, {"force": True})
        self.nodes.pop(path, None)
        self.__flush_api_cache__()

    def remote_rename(self, old, new):
        new_name = new.split("/")[-1]
        r = self.__fsapi__("patch", f"{old}", json={"new_name": new_name})
        # Wait for job to finish
        job_id = r.json()
        logging.info(f"RENAME: {job_id}")
        job_id = job_id["job_id"]
        while True:
            status = self.__jobapi__(job_id).json()
            logging.info(f"JOB\t{status}")
            if status["state"] == "DONE":
                break
            time.sleep(0.05)
        logging.info(f"RENAME DONE\t{old}  -> {new_name}")
        self.__flush_api_cache__()

    def remote_move(self, old, new):
        r = self.__fsapi__(
            "post",
            f"{old}/move",
            data=json.dumps(
                {"new_full_path": f"{self.config.folder.lstrip('/')}{new}"}
            ),
        )
        # Wait for job to finish
        job_id = r.json()
        logging.info(f"MOVE: {job_id}")
        job_id = job_id["job_id"]
        while True:
            status = self.__jobapi__(job_id).json()
            logging.info(f"JOB\t{status}")
            if status["state"] == "DONE":
                break
            time.sleep(0.05)
        logging.info(f"MOVE DONE\t{old}  -> {new}")
        self.__flush_api_cache__()


class IBFS(LoggingMixIn, Operations, LocalMixin, RemoteMixin):
    """
    Instabase file system.

    Mounts a remote file system locally via the instabase filesystem api.
    Files extensions that are not allowed are not synced to remote.
    However they are put inside a local folder and presented as if it exists in
    both places.

    For example if `remote` is the file system on instabase and `local` is a
    local folder that we use for caching non-allowed files:

        remote
            - some_file.txt
            - some_folder/
                - some_other_file.txt
        local
            - .some_file.txt.backup

    These are merged together and are presented as:

        mounted
            - some_file.txt
            - .some_file.txt.backup
            - some_folder/
                - some_other_file.txt

    This way, existing tools can continue to work as if this is a normal file
    system and specific allowed files are synced to and from the IB file system
    API.
    """

    def __init__(self, config, mount_point):
        """
        mount_point : Where was this file system mounted.
                      This is used to calculate a `mount_point.local` folder path
                      that acts as a local filesystem copy for all files that
                      are not part of the allow_ext list.

                      Thus existing tools can continue to exist and work
                      assuming things like `.swp` files will exist right next
                      to actual files.
        Config      :
            instance    :str        = Url of the instabase instance
            api         :str        = API version prefixes
            folder      :str        = The path of the folder on instabase
            token       :str        = Instabase API token.
            allow_ext   :List[str]  = List of extensions to mount. Everything else is ignored.
        """
        self.local_fs = f"{mount_point}.local"
        if not os.path.exists(self.local_fs):
            os.mkdir(self.local_fs)
        self.config = config
        self.nodes = {}
        self.fd = 0  # Used for creation
        self.session = requests.Session()
        # --- regex to ignore some file names
        self.remote_node = r"^[^\.].*\." + TRE(*self.config.allow_ext).regex() + "\s*$"
        self.remote_node = re.compile(self.remote_node)

    def handle(self, opname, path, *args):
        """
        Handle some operation either locally or remotely
        """
        fname = path.split("/")[-1]
        islocal = self.remote_node.match(fname) is None
        if islocal:
            logging.debug(f"HANDLELOCAL\t{opname} {fname} {path}")
        else:
            logging.debug(f"HANDLEREMOT\t{opname} {fname} {path}")
        handler = f"remote_{opname}"
        if islocal and self.config.enable_local_files:
            handler = f"local_{opname}"
        handler = getattr(self, handler)
        return handler(path, *args)

    # FUSE apis
    def chmod(self, path, mode):
        return 1

    def chown(self, path, uid, gid):
        pass

    def create(self, path, mode):
        self.handle("create", path, mode)
        self.fd += 1
        return self.fd

    def destroy(self, path):
        # Never delete ROOT. Nothing good can happen with this.
        if path != "/":
            self.handle("destroy", path)

    def getattr(self, path, fh=None):
        return self.handle("getattr", path, fh)

    def mkdir(self, path, mode):
        # Directory needs to exist in both places
        self.local_mkdir(path, mode)
        self.remote_mkdir(path, mode)

    def read(self, path, size, offset, fh):
        return self.handle("read", path, size, offset, fh)

    def readdir(self, path, fh):
        # Get list of remote folders/files
        remote = self.remote_readdir(path, fh)
        # Create the folder tree locally
        to_delete = os.listdir(f"{self.local_fs}{path}")
        for name in remote:
            if name not in "..":
                newpath = os.path.join(path, name)
                node = self.nodes[newpath]
                if node["type"] == "folder":
                    logging.debug(f"ENSURE\t{newpath}")
                    if name in to_delete:
                        to_delete.remove(name)
                    self.ensure_local_folder(path, name)
        for name in to_delete:
            shutil.rmtree(f"{self.local_fs}{os.path.join(path, name)}")
        # Get list of files present locally
        local = []
        if self.config.enable_local_files:
            local = self.local_readdir(path, fh)
        paths = set(remote + local) - {".", "..", "._."}
        paths = [".", ".."] + list(paths)
        logging.debug(f"READDIR\t{path} {paths}")
        return paths

    def rename(self, old, new):
        old_fname = old.split("/")[-1]
        old_isdir = old in self.nodes and self.nodes[old]["type"] == "folder"
        old_islocal = self.remote_node.match(old_fname) is None
        new_fname = new.split("/")[-1]
        new_islocal = self.remote_node.match(new_fname) is None
        op = "move"
        if old.split("/")[:-1] == new.split("/")[:-1]:
            op = "rename"
        logging.info(f"{op.upper()}: {old} -> {new}")
        if old_isdir:
            fn = self.remote_rename if op == "rename" else self.remote_move
            fn(old, new)
            shutil.move(f"{self.local_fs}{old}", f"{self.local_fs}{new}")
        else:  # Is a file
            if not old_islocal:  # Move on remote
                fn = self.remote_rename if op == "rename" else self.remote_move
                fn(old, new)
            else:
                shutil.move(f"{self.local_fs}{old}", f"{self.local_fs}{new}")
            self.__flush_api_cache__()

    def rmdir(self, path):
        if path != "/":
            self.local_rmdir(path)
            self.remote_rmdir(path)
        return 0

    def unlink(self, path):
        if path != "/":
            self.handle("unlink", path)
        return 1

    def truncate(self, path, length, fh=0):
        self.handle("truncate", path, length, fh)

    def utimens(self, path, times=None):
        return 1

    def write(self, path, data, offset, fh):
        return self.handle("write", path, data, offset, fh)
