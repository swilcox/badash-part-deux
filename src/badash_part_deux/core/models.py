from sqlmodel import SQLModel, Field
from sqlalchemy import JSON, Column


class JobBase(SQLModel):
    """Job Model"""

    slug: str  # how do mark this as unique=True?
    title: str
    description: str
    config: dict


class Job(JobBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
    config: dict = Field(sa_column=Column(JSON), default={})


class JobCreate(JobBase):
    pass
