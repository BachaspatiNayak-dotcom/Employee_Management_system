from sqlalchemy import Integer, String,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,DeclarativeBase

class Base(DeclarativeBase):
    pass

class Department(Base):
    __tablename__ = "departments"

    deptno: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    dname: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )


class Employee(Base):

    __tablename__ = "emp"

    eid: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    ename: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    designation: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    phone: Mapped[str | None] = mapped_column(
    String(20),
    unique=True,
    nullable=True
)

    deptno: Mapped[int] = mapped_column(
        ForeignKey("departments.deptno"),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="EMPLOYEE"
    )