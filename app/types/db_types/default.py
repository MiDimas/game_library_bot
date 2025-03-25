from typing import Annotated
from sqlalchemy.orm import mapped_column
from sqlalchemy import func
from datetime import datetime

int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(nullable=False, unique=True)]
str_null_true = Annotated[str, mapped_column(nullable=True)]