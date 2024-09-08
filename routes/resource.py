from fastapi import APIRouter, Security, Depends, BackgroundTasks
from models.custom_response import ResMsg
from models.token import TokenData
from sqlalchemy.orm import Session
from services.common import verify_user_request, get_resource_service, get_db, get_job_service
from utils.logger import LoguruLogger
from models.custom_request import DownloadResourceRequest
from models.db.job import JobType, JobStatus

resource_router = APIRouter(
    tags=["resource"]
)


@resource_router.get("/resource")
def index():
    return ResMsg(msg="resource router")


@resource_router.post("/resource/resource_table")
def get_resource_table(db: Session = Depends(get_db), token: TokenData = Security(verify_user_request)) -> ResMsg:
    logger = LoguruLogger.get_logger()
    logger.info(f"[{token.username}] call API /resource/resource_table..")
    answer = get_resource_service(db=db, user_id=token.user_id).get_resource_list()
    return answer


def download_resource_task(request: DownloadResourceRequest, db: Session, token: TokenData):
    job_service = get_job_service(db, token.username)
    job_id = job_service.add_job(JobType.RESOURCE_DOWNLOAD, description="下载资源")
    answer = get_resource_service(db=db, user_id=token.user_id).download_resource(request, job_id)
    if not answer.success:
        job_service.update_job(job_id, {
            "description": answer.msg,
            "status": JobStatus.fail
        })
    else:
        job_service.update_job(job_id, {
            "status": JobStatus.ready
        })
    db.commit()


@resource_router.post("/resource/download_resource")
def download_resource(
        request: DownloadResourceRequest,
        task: BackgroundTasks,
        db: Session = Depends(get_db),
        token: TokenData = Security(verify_user_request)
) -> ResMsg:
    logger = LoguruLogger.get_logger()
    logger.info(f"[{token.username}] call API /resource/download_resource..")

    task.add_task(download_resource_task, request, db, token)
    return ResMsg(msg="已成功添加下载列表")


@resource_router.get("/resource/check_resource_status")
def check_resource_status(token: TokenData = Security(verify_user_request)) -> ResMsg:
    logger = LoguruLogger.get_logger()
    logger.info(f"[{token.username}] call API /resource/check_resource_status..")
    return get_resource_service(db=None, user_id=None).check_website_status()


