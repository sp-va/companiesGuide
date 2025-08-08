import typing as t
import datetime

from sqlalchemy import (
    func,
    ForeignKey
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)

from app.models.base import Base
from app.models.organization import Organization, OrganizationsToActivities


class Activity(Base):
    __tablename__ = "activities"
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column()

    parent_id: Mapped[t.Optional[int]] = mapped_column(ForeignKey("activities.id", ondelete="SET NULL"), nullable=True)

    parent: Mapped["Activity"] = relationship(back_populates="children", remote_side="Activity.id")
    children: Mapped[t.List["Activity"]] = relationship(back_populates="parent", cascade="all, delete-orphan")

    orgs: Mapped[t.List["Organization"]] = relationship(secondary=OrganizationsToActivities.__table__, back_populates="activity_types")


