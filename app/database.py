from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped

from app.types.db_types.default import int_pk, created_at, updated_at
from app.config.main_conf import get_db_url

# Создание асинхронного подключения к PostgreSQL
DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        import app.models
        await conn.run_sync(Base.metadata.create_all)


class Base (AsyncAttrs,DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
    
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
