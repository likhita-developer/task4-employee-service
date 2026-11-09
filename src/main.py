import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

DATA_FILE = Path(__file__).parent / "employees.json"


class Employee(BaseModel):
    name: str = Field(min_length=1)
    department: str
    salary: float = Field(gt=0)


def load_employees():
    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_employees(employees):
    with open(DATA_FILE, "w") as file:
        json.dump(employees, file, indent=4)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/employees")
def get_employees():
    return load_employees()


@app.get("/employees/{name}")
def get_employee(name: str):
    employees = load_employees()

    for employee in employees:
        if employee["name"].lower() == name.lower():
            return employee

    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees")
def create_employee(employee: Employee):
    employees = load_employees()

    for existing in employees:
        if existing["name"].lower() == employee.name.lower():
            raise HTTPException(status_code=400, detail="Employee already exists")

    new_employee = employee.model_dump()
    employees.append(new_employee)
    save_employees(employees)

    return new_employee
