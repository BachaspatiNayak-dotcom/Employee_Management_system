from fastapi import FastAPI, Depends, status,HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt


from database import get_db
from models import Employee
from schemas import EmployeeCreate, EmployeeResponse,TokenResponse,EmployeeLogin
from security import create_access_token,decode_access_token



app = FastAPI()


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_employee(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        payload = decode_access_token(credentials.credentials)
        employee_id = int(payload["sub"])

    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    employee = db.query(Employee).filter(
        Employee.eid == employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Employee no longer exists"
        )

    return employee


"""normal employee can only see his details,manager can only see his dept emp details,HR can see everyone's details"""

@app.get("/employees", response_model=list[EmployeeResponse])
def get_employees(
    current_user: Employee = Depends(get_current_employee),
    db: Session = Depends(get_db)
):

    if current_user.role == "EMPLOYEE":

        employees = db.query(Employee).filter(
            Employee.eid == current_user.eid
        ).all()

    elif current_user.role == "MANAGER":

        employees = db.query(Employee).filter(
            Employee.deptno == current_user.deptno
        ).all()

    elif current_user.role == "HR":

        employees = db.query(Employee).all()

    else:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to access this resource"
        )

    return employees

@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
    )
def add_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    new_employee = Employee(
        ename=employee.ename,
        designation=employee.designation,
        deptno=employee.deptno,
        role=employee.role
    )

    db.add(new_employee)

    db.commit()

    db.refresh(new_employee)

    return new_employee

@app.put("/employees/{eid}")
def update_employee(
    eid: int,
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    # Find employee
    emp = db.query(Employee).filter(
        Employee.eid == eid
    ).first()

    # Check whether employee exists
    if not emp:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Update fields
    emp.ename = employee.ename
    emp.designation = employee.designation
    

    db.commit()
    db.refresh(emp)

    return emp

@app.delete("/employees/{eid}")
def delete_employee(
    eid: int,
    db: Session = Depends(get_db)
):

    emp = db.query(Employee).filter(
        Employee.eid == eid
    ).first()

    if not emp:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(emp)

    db.commit()

    return {
        "message": "Employee deleted successfully"
    }


@app.post(
    "/auth/login",
    response_model=TokenResponse
)
def login(
    credentials: EmployeeLogin,
    db: Session = Depends(get_db)
):

    emp = db.query(Employee).filter(
        Employee.ename == credentials.ename,
        Employee.phone == credentials.phone
    ).first()

    if not emp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    payload = {
        "sub": str(emp.eid),
        "ename": emp.ename,
        "designation": emp.designation
    }

    token = create_access_token(payload)

    return {
        "access_token": token,
        "token_type": "bearer"
    }