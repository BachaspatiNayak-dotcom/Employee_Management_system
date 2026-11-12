from pydantic import BaseModel, ConfigDict,Field


class EmployeeCreate(BaseModel):

    ename: str
    designation: str
    deptno: int
    role: str = "EMPLOYEE"


class EmployeeResponse(BaseModel):

    eid: int
    ename: str
    designation: str
    phone: str | None
    deptno: int
    role: str

    model_config = ConfigDict(from_attributes=True)


class EmployeeLogin(BaseModel):
    ename: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=7, max_length=20)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"