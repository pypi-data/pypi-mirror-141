import asyncio
from dataclasses import asdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

from redis import Redis
from rq import Queue
from rq.job import Job
from rq.registry import FailedJobRegistry, StartedJobRegistry
from rq_scheduler import Scheduler
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

# from nb_workflows.workflows.registers import register_history_db
from nb_workflows.conf.server_settings import settings
from nb_workflows.db.sync import SQL
from nb_workflows.executors.docker import builder_executor, docker_exec
from nb_workflows.executors.utils import generate_execid
from nb_workflows.hashes import Hash96, generate_random
from nb_workflows.managers import projects_mg, workflows_mg
from nb_workflows.models import WorkflowModel

# from nb_workflows.notebooks import nb_job_executor
from nb_workflows.types import NBTask, ScheduleData
from nb_workflows.utils import run_async

_DEFAULT_SCH_TASK_TO = 60 * 5  # 5 minutes


def scheduler_dispatcher(projectid: str, jobid: str) -> Union[Job, None]:
    """
    This is the entrypoint of any workflow or job to be executed by RQ and it
    will be executed by :class:`nb_workflows.scheduler.SchedulerExecutor`
    in the RQWorker of the control plane.


    This function receive the projectid and jobid as reference of the task to
    be completed. Then it will prepare the context for it.


    Because rq-scheduler has some limitations
    and could be abandoned in the future, this abstraction was created
    where the idea is to use the scheduler only to enqueue works through rq.

    Also, adopting this strategy, allows to react dinamically to changes
    in the workflow. Usually rq caches the params of each job.

    :param projectid: is the id of project, from ProjectModel
    :type str:
    :param jobid: jobid from WorkflowModel
    :type str:


    :return: a Job instance from RQ a or None if the Job or the project is not found
    :rtype: an Union between Job or None.
    """
    db = SQL(settings.SQL)
    _cfg = settings.rq2dict()
    redis = Redis(**_cfg)
    scheduler = SchedulerExecutor(redis=redis, qname=settings.RQ_CONTROL_QUEUE)

    Session = db.sessionmaker()

    with Session() as session:
        obj_model = workflows_mg.get_by_jobid_model_sync(session, jobid)
        if obj_model and obj_model.enabled:

            priv_key = projects_mg.get_private_key_sync(session, projectid)

            task = NBTask(**obj_model.job_detail)
            _job = scheduler.enqueue_notebook_in_docker(
                projectid,
                priv_key,
                task,
            )
            return _job
        else:
            if not obj_model:
                scheduler.cancel_job(jobid)
                print(f"job: {jobid} not found, deleted")
                # raise IndexError(f"job: {jobid} not found")

            print(f"Job: {jobid} disabled")
    return None


class SchedulerExecutor:
    """
    It manages the logic to enqueue and dispatch jobs.
    The SchedulerExecutor belongs to the server side, it connects the webserver with
    the workers in the control plane.

    Because their main function wraps RQ and RQ-Scheduler some variables names could be
    confusing. When we talk about jobs we talk about the task executed by RQ or RQ-Scheduler.

    :param redis: A Redis instance
    :param qname: configured by default from settings, it MUST BE consistent between the different control plane components.
    """

    def __init__(self, redis: Redis, qname, is_async=True):
        self.redis = redis
        self.Q = Queue(qname, connection=self.redis, is_async=is_async)
        self.qname = qname
        # on_success=rq_job_ok, on_failure=rq_job_error)
        self.scheduler = Scheduler(queue=self.Q, connection=self.redis)
        self.is_async = is_async

    def dispatcher(self, projectid, jobid) -> Job:
        j = self.Q.enqueue(scheduler_dispatcher, projectid, jobid)
        return j

    def enqueue_notebook_in_docker(
        self, projectid, priv_key, task: NBTask, executionid=None
    ) -> Job:
        """It executes the task in the remote machine with runtime configuration of
        the project for this task

        :param projectid: id of the project
        :param task: NBTask object
        :param executionid: An optional executionid
        """

        _id = executionid or generate_execid(size=settings.EXECUTIONID_LEN)
        Q = Queue(task.machine, connection=self.redis, is_async=self.is_async)
        job = Q.enqueue(
            docker_exec,
            projectid,
            priv_key,
            task.jobid,
            job_id=_id,
            job_timeout=task.timeout,
        )
        return job

    def enqueue_build(
        self, projectid, project_zip_route, qname=settings.RQ_CONTROL_QUEUE
    ) -> Job:
        """
        TODO: in the future a special queue should exists.
        TODO: set default timeout for build tasks,
              or better add a type like BuildTaskOptions
        TODO: design internal, onpremise or external docker registries.
        """

        _id = generate_execid(size=10)
        if qname == settings.RQ_CONTROL_QUEUE:
            job = self.Q.enqueue(
                builder_executor,
                projectid,
                project_zip_route,
                job_id=_id,
                job_timeout=(60 * 60) * 24,
            )
        else:
            Q = Queue(qname, connection=self.redis)
            job = Q.enqueue(
                builder_executor,
                projectid,
                project_zip_route,
                job_id=_id,
                job_timeout=(60 * 60) * 24,
                is_async=self.is_async,
            )

        return job

    async def schedule(self, project_id, jobid, task: NBTask) -> str:
        """Put in RQ-Scheduler a workflows previously created"""
        # schedule_data = data_dict["schedule"]
        # task = NBTask(**data_dict)
        # task.schedule = ScheduleData(**schedule_data)
        # jobid = await workflows_mg.register(session, project_id, task, update=update)

        if task.schedule.cron:
            await run_async(self._cron2redis, project_id, jobid, task)
        else:
            await run_async(self._interval2redis, project_id, jobid, task)

        return jobid

    def _interval2redis(self, projectid: str, jobid: str, task: NBTask):
        interval = task.schedule
        start_in_dt = datetime.utcnow() + timedelta(minutes=interval.start_in_min)

        self.scheduler.schedule(
            id=jobid,
            scheduled_time=start_in_dt,
            func=scheduler_dispatcher,
            args=[projectid, jobid],
            interval=interval.interval,
            repeat=interval.repeat,
            queue_name=self.qname,
            timeout=_DEFAULT_SCH_TASK_TO,
        )

    def _cron2redis(self, projectid: str, jobid: str, task: NBTask):
        cron = task.schedule
        self.scheduler.cron(
            cron.cron,
            id=jobid,
            func=scheduler_dispatcher,
            args=[projectid, jobid],
            repeat=cron.repeat,
            queue_name=self.qname,
        )

    def list_jobs(self):
        """List jobs from Redis"""
        jobs = []
        for x in self.scheduler.get_jobs():
            jobs.append(
                dict(
                    jobid=x.id,
                    func_name=x.func_name,
                    created_at=x.created_at.isoformat(),
                )
            )
        return jobs

    def cancel_all(self):
        """Cancel all from redis"""
        for j in self.scheduler.get_jobs():
            self.scheduler.cancel(j)

    def cancel_job(self, jobid):
        """Cancel job from redis"""
        self.scheduler.cancel(jobid)

    async def cancle_job_async(self, jobid):
        await run_async(self.scheduler.cancel, jobid)

    async def delete_workflow(self, session, projectid, jobid: str):
        """Delete job from redis and db"""

        await run_async(self.cancel_job, jobid)
        await workflows_mg.delete_wf(session, projectid, jobid)
