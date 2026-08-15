from datetime import datetime
from typing import TYPE_CHECKING
import sqlalchemy as sa
import sqlalchemy.orm as so

from ..extensions import db

if TYPE_CHECKING:
    from .users import User
    
    
class Project(db.Model):
    __tablename__ = "projects"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(120),index=True)
    description: so.Mapped[str] = so.mapped_column(sa.Text())
    markdown: so.Mapped[str] = so.mapped_column(sa.Text())
    github_url: so.Mapped[str | None] = so.mapped_column(sa.String(255))
    demo_url: so.Mapped[str | None] = so.mapped_column(sa.String(255))
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime,server_default=sa.func.now())
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id"),index=True)
    
    user: so.Mapped["User"] = so.relationship(back_populates="projects")