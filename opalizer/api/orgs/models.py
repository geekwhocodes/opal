import sqlalchemy as sa

from opalizer.models import BaseModel

class Org(BaseModel):
    __tablename__ = "orgs"

    id = sa.Column("id", sa.Integer, primary_key=True, nullable=False)
    name = sa.Column("name", sa.String(256), nullable=False, index=True, unique=True)
    schema = sa.Column("schema", sa.String(64), nullable=False, unique=True)
    slug = sa.Column("slug", sa.String(32), nullable=False, unique=True)


    __table_args__ = ({"schema": "public"},)