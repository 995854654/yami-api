import os.path
import uuid
from fastapi import status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.db.resources import ResourceInfo, ResourceBase
from models.db.job import BackgroundJob, JobStatus
from models.custom_status import WebsiteStatus
from typing import List
from models.custom_response import ResMsg
from services.storage import BaseStorage
from models.custom_request import DownloadResourceRequest
from urllib.parse import urlparse
from utils.logger import LoguruLogger
from services.downloader import YoutubeDownloader, UnknownDownloader, ResourceSupportModel, BilibiliDownloader
import requests

# 资源支持列表
RESOURCE_SUPPORT_LIST = [
    "https://www.youtube.com", "https://www.bilibili.com"
]
# 下载器列表
RESOURCE_MODEL_LIST = [
    ResourceSupportModel(data_source="youtube", domain="www.youtube.com", file_type="mp4", downloader=YoutubeDownloader()),
    ResourceSupportModel(data_source="bilibili", domain="www.bilibili.com", file_type="mp4", downloader=BilibiliDownloader()),
]

unknown_downloader = ResourceSupportModel(data_source="unknown", domain="unknown", file_type="unknown", downloader=UnknownDownloader())


class ResourceService:
    def __init__(self, db: Session, user_id: str, storage: BaseStorage = None):
        self.db = db
        self.user_id = user_id
        self.store = storage
        self.logger = LoguruLogger.get_logger()

    def get_resource_list(self) -> ResMsg:
        resource_list: List[ResourceInfo] = self.db.query(ResourceInfo).filter(ResourceInfo.user_id == self.user_id).all()
        job_id_list = [item.job_id for item in resource_list]

        job_list: List[BackgroundJob] = self.db.query(BackgroundJob).filter(or_(*[BackgroundJob.job_id == job_id for job_id in job_id_list])).all()
        data = []
        for resource in resource_list:
            resource_obj = ResourceBase.from_orm(resource).dict()
            has_job = False
            for job in job_list:
                if job.job_id == resource.job_id:
                    resource_obj.update({
                        "status": job.status.value,
                        "description": job.description
                    })
                    has_job = True
            if not has_job:
                resource_obj.update({"status": JobStatus.unknown.value})
            data.append(resource_obj)
        return ResMsg(data=data)

    def add_resource_record(self, job_id: str, resource_url: str, data_source: str):
        resource_id = str(uuid.uuid1())
        resource_object = ResourceInfo()
        resource_object.resource_name = "unknown"
        resource_object.user_id = self.user_id
        resource_object.resource_id = resource_id
        resource_object.job_id = job_id
        resource_object.resource_url = resource_url
        resource_object.data_source = data_source
        self.db.add(resource_object)
        self.db.commit()
        return resource_id

    def download_resource(self, request: DownloadResourceRequest, job_id: str) -> ResMsg:
        # create resource object
        domain = urlparse(request.url).netloc

        support_object = None
        parse_success = False
        for source in RESOURCE_MODEL_LIST:
            if domain == source.domain:
                support_object = source
                parse_success = True
                break
        if not support_object:
            support_object = unknown_downloader

        # 先添加资源列表
        resource_id = self.add_resource_record(job_id, request.url, support_object.data_source)

        downloader = support_object.downloader
        downloader.init_source_loader(url=request.url, file_type=support_object.file_type)
        try:
            resource_name = downloader.get_resource_title()
        except Exception as err:
            self.logger.error("resource download failed: " + str(err))
            return ResMsg(
                success=False,
                code=status.HTTP_400_BAD_REQUEST,
                msg=f"资源名称获取失败"
            )

        # 更新资源名称
        self.db.query(ResourceInfo).filter(ResourceInfo.resource_id == resource_id).update({
            "resource_name": resource_name
        })
        self.db.commit()
        filepath = self.store.get_path() + f"/{self.user_id}/{resource_name}"
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        self.logger.info(f"保存位置：{filepath}")

        if not parse_success:
            return ResMsg(
                success=False,
                code=status.HTTP_400_BAD_REQUEST,
                msg=f"无法解析{domain}的资源"
            )
        try:
            downloader.get_resource_data(filepath)
        except Exception as err:
            self.logger.error("resource download failed: " + str(err))
            return ResMsg(
                success=False,
                code=status.HTTP_400_BAD_REQUEST,
                msg=f"资源下载失败"
            )
        return ResMsg()

    @staticmethod
    def check_website_status() -> ResMsg:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        }
        result = []
        for domain in RESOURCE_SUPPORT_LIST:
            dic = {"website": domain, "remark": ""}
            try:
                response = requests.get(domain, headers=headers, verify=False, timeout=3)
                if response.status_code == 200:
                    dic["status"] = WebsiteStatus.READY
                else:
                    dic["status"] = WebsiteStatus.OTHER
                    dic["remark"] = "不详"

            except:
                dic["status"] = WebsiteStatus.FAIL
                dic["remark"] = "连接异常"
            finally:
                result.append(dic)
        return ResMsg(data=result)


if __name__ == '__main__':
    import warnings

    warnings.filterwarnings("ignore")
    ResourceService.check_website_status()
