from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text
)

from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Experiment(Base):

    __tablename__ = "experiments"

    id = Column(
        Integer,
        primary_key=True
    )

    project_name = Column(
        String(255),
        nullable=False
    )

    mode = Column(
        String(50),
        nullable=False
    )

    selected_metrics = Column(
        Text,
        nullable=False
    )

    dataset = Column(
        Text,
        nullable=False
    )

    results = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )