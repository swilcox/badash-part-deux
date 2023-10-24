from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.middleware.sessions import SessionMiddleware

from .core.models import Job, JobBase
from .core.db import DBSetup

api = FastAPI()
db_setup = DBSetup()


@api.get("/")
async def root():
    return {"message": "Hello, World"}


@api.get("/jobs", response_model=list[Job])
async def get_jobs(session: AsyncSession = Depends(db_setup.get_session)):
    result = await session.execute(
        select(Job.id, Job.title, Job.slug, Job.description, Job.config).order_by(
            Job.slug
        )
    )
    jobs = result.all()
    return jobs


@api.post("/jobs", response_model=Job)
async def add_job(
    title: str,
    config: dict = None,
    description: str = "",
    slug: str = "",
    session: AsyncSession = Depends(db_setup.get_session),
):
    job = Job(slug=slug, title=title, description=description, config=config)
    session.add(job)
    await session.commit()
    await session.refresh(job)
    return job
