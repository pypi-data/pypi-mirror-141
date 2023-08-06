import os
import argparse
import sqlite3
import abc
import requests
import logging
import boto3
import oss2
import csv

from typing import List

MODE_LOCAL = "local"
MODE_S3 = "s3"
MODE_OSS = "oss"

MODES = {MODE_LOCAL: "Local", MODE_S3: "Amazon S3", MODE_OSS: "AliCloud OSS"}
VALID_CSV_EXT = (".csv", ".CSV")
VALID_IMAGE_EXT = (".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG")


class StorageClient(metaclass=abc.ABCMeta):
    def __init__(self, storage_args: dict):
        self.storage_args = storage_args

    @abc.abstractmethod
    def read_image_list(self, directory: str) -> List:
        pass

    @abc.abstractmethod
    def download_image(self, location: str) -> str:
        pass


class LocalStorageClient(StorageClient):
    def read_image_list(self, directory: str) -> List:
        return [x for x in os.listdir(directory) if x.endswith(VALID_IMAGE_EXT)]

    def download_image(self, location: str) -> str:
        return location


class S3StorageClient(StorageClient):
    def __init__(self, storage_args: dict):
        super().__init__(storage_args)
        access_key = storage_args.get("access_key")
        secret = storage_args.get("secret")
        bucket = storage_args.get("bucket")
        if not access_key or not secret or not bucket:
            raise Exception("Please provide S3 credentials and bucket name.")
        self.s3 = boto3.resource("s3", aws_access_key_id=access_key, aws_secret_access_key=secret)
        self.bucket = self.s3.Bucket(name=bucket)

    def read_image_list(self, directory: str) -> List:
        lst = []
        for obj in self.bucket.objects.filter(Prefix=directory):
            name = obj.key
            if name.endswith(VALID_IMAGE_EXT):
                lst.append(name.replace(directory, ""))

        return lst

    def download_image(self, location: str) -> str:
        temp_file = "temp_file"
        self.bucket.download_file(location, temp_file)
        return temp_file


class OSStorageClient(StorageClient):
    def __init__(self, storage_args: dict):
        super().__init__(storage_args)
        access_key = storage_args.get("access_key")
        secret = storage_args.get("secret")
        bucket = storage_args.get("bucket")
        endpoint = storage_args.get("endpoint")
        if not access_key or not secret or not bucket or not endpoint:
            raise Exception("Please provide Alibaba Cloud credentials, bucket name and endpoint.")
        auth = oss2.Auth(access_key, secret)
        self.bucket = oss2.Bucket(auth, endpoint, bucket)

    def read_image_list(self, directory: str) -> List:
        lst = []
        for obj in oss2.ObjectIterator(self.bucket, prefix=directory):
            name = obj.key
            if name.endswith(VALID_IMAGE_EXT):
                lst.append(name.replace(directory, ""))

        return lst

    def download_image(self, location: str) -> str:
        temp_file = "temp_file"
        self.bucket.get_object_to_file(location, temp_file)
        return temp_file


class ImageNameProvider(metaclass=abc.ABCMeta):
    def __init__(self, storage_client: StorageClient, provider_args: dict):
        self.storage_client = storage_client
        self.provider_args = provider_args

    @abc.abstractmethod
    def get_id_and_path(self, directory: str) -> List:
        pass


class CSVProvider(ImageNameProvider):
    def get_id_and_path(self, directory: str) -> List:
        id_paths = []
        with open(self.provider_args.get("csv_file"), "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            id_header_index = None
            location_header_index = None

            for index, header in enumerate(next(csv_reader)):
                if header == self.provider_args.get("id_header"):
                    id_header_index = index
                if header == self.provider_args.get("location_header"):
                    location_header_index = index
                if id_header_index is not None and location_header_index is not None:
                    break
            if id_header_index is None or location_header_index is None:
                raise Exception(f"Please ensure the csv file contains both inputted image id and location headers.")
            for index, row in enumerate(csv_reader):
                if row[id_header_index].replace(" ", "") == "":
                    logging.info(f"Id is empty for data row: {index + 1}, will be skipped.")
                    continue
                if row[location_header_index].replace(" ", "") == "":
                    logging.info(f"Image location is empty for id: {row[id_header_index]}, will be skipped.")
                    continue
                id_paths.append([row[id_header_index], row[location_header_index]])
        return id_paths


class StorageProvider(ImageNameProvider):
    def get_id_and_path(self, directory: str) -> List:
        id_paths = []
        image_list = self.storage_client.read_image_list(directory)
        for image_name in image_list:
            id_paths.append([image_name[0 : image_name.rfind(".")], f"{directory}{image_name}"])
        return id_paths


class DbBuilder:
    def __init__(self, db_builder_args: dict, storage_client: StorageClient):
        self.mode = db_builder_args.get("mode")
        self.directory = db_builder_args.get("directory")
        if self.directory and not self.directory.endswith("/"):
            self.directory = self.directory + "/"

        self.api_args = db_builder_args.get("api_args")
        self.provider_args = db_builder_args.get("provider_args")
        self.storage_client = storage_client
        self.image_provider = None
        self.resume = False
        self.id_paths = []
        self.connection = sqlite3.connect("images.db")

    def __del__(self):
        if self.connection:
            self.connection.close()

    def _handle_config(self):
        source = None
        if self.provider_args.get("csv_file") is not None:
            if not self.provider_args.get("csv_file").endswith(VALID_CSV_EXT):
                raise Exception(f"Please input a valid csv file if you decide to import locations from csv file.")
            if self.provider_args.get("id_header") is None or self.provider_args.get("location_header") is None:
                raise Exception(
                    f"Please input valid id header or location header if you decide to import locations "
                    f"from csv file."
                )
            self.image_provider = CSVProvider(self.storage_client, self.provider_args)
            source = self.provider_args.get("csv_file")
        else:
            self.image_provider = StorageProvider(self.storage_client, self.provider_args)
            source = self.directory

        self.connection.cursor().execute("CREATE TABLE IF NOT EXISTS config(mode TEXT NOT NULL, source TEXT NOT NULL)")
        self.connection.commit()

        for row in self.connection.cursor().execute("SELECT * FROM config limit 1"):
            if self.mode != row[0]:
                raise Exception(f"Please keep the same mode {row[0]} if you are continuing the program.")
            if source != row[1]:
                raise Exception(f"Please keep the same source {row[1]} if you are continuing the program.")
            self.resume = True

        if not self.resume:
            self.connection.cursor().execute(f'INSERT INTO config VALUES ("{self.mode}", "{source}")')
            self.connection.commit()

    def _read_list(self):
        self.id_paths = self.image_provider.get_id_and_path(self.directory)
        self.connection.cursor().execute(
            "CREATE TABLE IF NOT EXISTS image(path TEXT NOT NULL UNIQUE, id TEXT NOT NULL, completed INT NULL)"
        )
        self.connection.commit()

        for id_path in self.id_paths:
            try:
                self.connection.cursor().execute(
                    f'INSERT INTO image (path, id) VALUES ("{id_path[1]}", ' f'"{id_path[0]}")'
                )
            except sqlite3.IntegrityError:
                continue
        self.connection.commit()

    def _process(self):
        for row in self.connection.cursor().execute("SELECT * FROM image WHERE completed IS NULL"):
            image_path = row[0]
            id_number = row[1]

            try:
                image_location = self.storage_client.download_image(image_path)
                headers = {"X-ADVAI-KEY": self.api_args.get("x_advai_key")}
                files = {self.api_args.get("img_parameter"): open(image_location, "rb")}
                data = {
                    self.api_args.get("id_number_parameter"): id_number,
                    self.api_args.get("refer_id_parameter"): id_number,
                    "imageType": "PHOTO_FACE",  # https://doc.advance.ai/face_search_db.html#face-search-db
                }
                resp = requests.post(self.api_args.get("url"), headers=headers, files=files, data=data)

                if resp.status_code == 200 and str(resp.json().get("status")) == self.api_args.get(
                    "success_status_code"
                ):
                    logging.info(f"Marking as completed for the image {image_path} ...")
                    self.connection.cursor().execute(
                        f'UPDATE image SET completed=strftime("%s", "now") WHERE path="{image_path}"'
                    )
                    self.connection.commit()
                else:
                    logging.error(
                        f"Error while calling the API with status {resp.status_code} and response: {resp.json()}"
                    )
            except Exception as e:
                logging.error(e)

    def build(self):
        self._handle_config()
        self._read_list()
        self._process()


def run():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str, help="mode of upload: 'local', 's3' or 'oss'")
    parser.add_argument(
        "url",
        type=str,
        help="URL of JSON POST (non multipart) db build API e.g. http://127.0.0.1:8127/face-search/v1/form/db-build",
    )
    parser.add_argument(
        "--directory",
        help="Applicable only if csv file is not provided. Images directory. Images inside must have extension .jpg or .png.",
    )
    parser.add_argument("--img_parameter", help="Parameter name for the image. Default: 'img'.")
    parser.add_argument(
        "--id_number_parameter",
        help="ID number parameter. Default: 'idNumber'. The image name without extension will be used. E.g. for 'photo.jpg', 'photo' will be sent as 'idNumber'.",
    )
    parser.add_argument(
        "--refer_id_parameter",
        help="Reference parameter. Default: 'referId'. The image name without extension will be used. E.g. for 'photo.jpg', 'photo' will be sent as 'referId'.",
    )
    parser.add_argument("--success_status_code", help="Success status code of the API. Default: '0'.")
    parser.add_argument("--x_advai_key", help="X-ADVAI-KEY header value for your access key. Default is empty.")
    parser.add_argument("--access_key", help="AWS / Alibaba Cloud access key")
    parser.add_argument("--secret", help="AWS / Alibaba Cloud secret")
    parser.add_argument("--bucket", help="AWS / Alibaba Cloud bucket name")
    parser.add_argument("--endpoint", help="Alibaba Cloud OSS endpoint")
    parser.add_argument("--csv_file", help="Input csv file")
    parser.add_argument("--csv_id_header", help="Name of the header of id numbers within the csv file")
    parser.add_argument("--csv_location_header", help="Name of the header of locations within the csv file")
    args = parser.parse_args()

    if args.mode not in MODES:
        raise Exception("Invalid mode")

    if not args.directory and not args.csv_file:
        raise Exception("Please provide a csv file or directory for images.")

    api_args = {
        "url": args.url,
        "img_parameter": args.img_parameter if args.img_parameter else "img",
        "id_number_parameter": args.id_number_parameter if args.id_number_parameter else "idNumber",
        "refer_id_parameter": args.refer_id_parameter if args.refer_id_parameter else "referId",
        "success_status_code": args.success_status_code if args.success_status_code else "0",
        "x_advai_key": args.x_advai_key,
    }

    provider_args = {
        "csv_file": args.csv_file if args.csv_file else None,
        "id_header": args.csv_id_header if args.csv_id_header else None,
        "location_header": args.csv_location_header if args.csv_location_header else None,
    }

    db_builder_args = {
        "mode": args.mode,
        "directory": args.directory,
        "api_args": api_args,
        "provider_args": provider_args,
    }

    db_builder = None
    if args.mode == MODE_LOCAL:
        storage_args = {}
        db_builder = DbBuilder(db_builder_args, LocalStorageClient(storage_args))
    elif args.mode == MODE_S3:
        storage_args = {
            "access_key": args.access_key,
            "secret": args.secret,
            "bucket": args.bucket,
        }
        db_builder = DbBuilder(db_builder_args, S3StorageClient(storage_args))
    elif args.mode == MODE_OSS:
        storage_args = {
            "access_key": args.access_key,
            "secret": args.secret,
            "bucket": args.bucket,
            "endpoint": args.endpoint,
        }
        db_builder = DbBuilder(db_builder_args, OSStorageClient(storage_args))
    db_builder.build()


if __name__ == "__main__":
    run()
