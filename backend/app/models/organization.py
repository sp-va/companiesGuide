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


class OrganizationsToActivities(Base):
    __tablename__ = "orgs_to_activities"

    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id",), primary_key=True)
    activity_type_id: Mapped[int] = mapped_column(ForeignKey("activities.id",), primary_key=True)


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)


    building_id: Mapped[str] = mapped_column(ForeignKey("buildings.id", ondelete="SET NULL"))

    phone_numbers: Mapped[t.List["PhoneNumber"]] = relationship("PhoneNumber", back_populates="organization")
    activity_types: Mapped[t.List["Activity"]] = relationship(secondary=OrganizationsToActivities.__table__, back_populates="orgs")
    building: Mapped["Building"] = relationship("Building", back_populates="organizations")


class PhoneNumber(Base):
    __tablename__ = "phone_numbers"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(unique=True)

    related_org: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"))
    organization: Mapped["Organization"] = relationship("Organization", back_populates="phone_numbers")