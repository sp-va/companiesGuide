import typing as t
import datetime

from sqlalchemy import (
    func,
    ForeignKey
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from geoalchemy2 import Geography

from app.models.base import Base



class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[tuple[float, float]] = mapped_column(Geography(geometry_type="POINT", srid=4326), nullable=False, index=False)

    organizations: Mapped["Organization"] = relationship("Organization", back_populates="building")