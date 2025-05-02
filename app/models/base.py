from sqlalchemy.orm import DeclarativeBase, declared_attr, MappedAsDataclass


class Base(MappedAsDataclass, DeclarativeBase):
    """Общий Declarative-Base со включённым `dataclass`-API."""

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: D401
        return cls.__name__.lower()
