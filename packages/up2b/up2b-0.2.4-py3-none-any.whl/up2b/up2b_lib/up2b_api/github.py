#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thepoy
# @Email: thepoy@aliyun.com
# @File Name: github.py
# @Created: 2021-02-13 09:10:14
# @Modified:  2022-03-10 11:32:58

import os
import time
import requests

from typing import Optional, List, Dict, Tuple, Union
from base64 import b64encode
from requests.exceptions import ConnectionError
from up2b.up2b_lib.up2b_api import Base, ImageBedMixin, CONF_FILE
from up2b.up2b_lib.constants import GITHUB
from up2b.up2b_lib.utils import Login, check_image_exists, child_logger

logger = child_logger(__name__)


class Github(Base, ImageBedMixin):
    def __init__(
        self,
        auto_compress: bool = False,
        add_watermark: bool = False,
        conf_file: str = CONF_FILE,
    ):
        self.image_bed_code = GITHUB
        super().__init__(auto_compress, add_watermark, conf_file)

        self.max_size = 20 * 1024 * 1024

        if self.auth_info:
            self.token: str = self.auth_info["token"]
            self.username: str = self.auth_info["username"]
            self.repo: str = self.auth_info["repo"]
            self.folder: str = self.auth_info["folder"]

            self.headers = {
                "Accept": "application/vnd.github.v3+json",
                "Authorization": "token " + self.token,
            }

    def login(self, token: str, username: str, repo: str, folder: str = "md"):
        auth_info = {
            "token": token,
            "username": username,
            "repo": repo,
            "folder": folder,
        }
        self._save_auth_info(auth_info)

    @Login
    def upload_image(self, image_path: str) -> Union[str, dict]:
        raw_filename = os.path.basename(image_path)
        image_path = self._compress_image(image_path)
        image_path = self._add_watermark(image_path)
        suffix = os.path.splitext(image_path)[-1]
        if suffix.lower() == ".apng":
            suffix = ".png"
        filename = f"{int(time.time() * 1000)}{suffix}"
        with open(image_path, "rb") as fb:
            url = self.base_url + filename
            data = {
                "content": b64encode(fb.read()).decode("utf-8"),
                "message": "typora - " + raw_filename,
            }
            try:
                resp = requests.put(url, headers=self.headers, json=data)
            except ConnectionError as e:
                return "Warning: %s upload failed, please try again: (%s)" % (
                    image_path,
                    e,
                )
            if resp.status_code == 201:
                uploaded_url = resp.json()["content"]["download_url"]
                logger.debug("uploaded: %s => %s", image_path, uploaded_url)
                return uploaded_url
            else:
                error = resp.json()["message"]
                logger.error("upload failed: image=%s, error=%s", image_path, error)
                return {
                    "error": error,
                    "status_code": resp.status_code,
                    "image_path": image_path,
                }

    @Login
    def upload_images(self, images_path: List[str]) -> List[str]:
        check_image_exists(images_path)

        self._check_images_valid(images_path)

        images_url = []
        for img in images_path:
            images_url.append(self.upload_image(img))

        cdn_urls = []
        for url in images_url:
            if type(url) == str:
                cdn_urls.append(self.cdn_url(url))
            else:
                cdn_urls.append(url)

        # 终端打印url，typora需要
        for url in cdn_urls:
            print(url)

        self._clear_cache()
        return cdn_urls

    @Login
    def get_all_images(self):
        images = []
        all_images_resp = self.get_all_images_in_image_bed()
        if all_images_resp:
            for file in self.get_all_images_in_image_bed():
                images.append(
                    {
                        "url": self.cdn_url(file["download_url"]),
                        "sha": file["sha"],
                        "delete_url": file["url"],
                    }
                )
        return images

    @Login
    def get_all_images_in_image_bed(self) -> Optional[Dict[str, str]]:
        resp = requests.get(self.base_url, headers=self.headers)
        if resp.status_code == 200:
            return resp.json()
        else:
            return None

    @Login
    def delete_image(
        self,
        sha: str,
        url: str,
        message: str = "Delete pictures that are no longer used",
    ):
        data = {"sha": sha, "message": message}
        resp = requests.delete(url, headers=self.headers, json=data)
        return resp.status_code == 200

    @Login
    def delete_images(
        self,
        info: Tuple[str, str],
        message: str = "Delete pictures that are no longer used",
    ):
        failed = []
        for sha, url in info:
            result = self.delete_image(sha, url, message)
            if not result:
                failed.append(sha)
        return failed

    @property
    def base_url(self) -> str:
        return "https://api.github.com/repos/%s/%s/contents/%s/" % (
            self.username,
            self.repo,
            self.folder,
        )

    def cdn_url(self, url: str) -> str:
        path = url.split("/main/")[-1]
        return "https://cdn.jsdelivr.net/gh/%s/%s/%s" % (self.username, self.repo, path)

    def __repr__(self):
        return "github.com"
