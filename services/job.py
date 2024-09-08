from sqlalchemy.orm import Session
import uuid
from models.db.job import BackgroundJob, JobType, JobStatus


class JobService:
    def __init__(self, db: Session, username: str):
        self.db = db
        self.username = username

    def add_job(self, job_type: JobType, description: str) -> str:
        job_object = BackgroundJob()
        job_id = str(uuid.uuid1())
        job_object.job_id = job_id
        job_object.job_type = job_type
        job_object.creator = self.username
        job_object.description = description
        job_object.status = JobStatus.processing
        self.db.add(job_object)
        self.db.commit()
        return job_id

    def update_job(self, job_id: str, update_dict: dict):
        self.db.query(BackgroundJob).filter(BackgroundJob.job_id == job_id).update(update_dict)
