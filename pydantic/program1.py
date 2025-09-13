from pydantic import BaseModel, EmailStr,AnyUrl,Field
from typing import List, Dict, Optional , Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    LinkedIn: AnyUrl
    email: EmailStr
    age: int
    weight: Annotated[float, Field(..., gt=0, strict=True,description="Weight must be a positive number")]
    married: bool
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]

patient_info = {
    'name': 'John Doe',
    "LinkedIn": "https://www.linkedin.com/in/johndoe",
    'age': 30,
    'email': 'abc@gmail.com',
    'weight': 70.5,
    'married': False,
    'allergies': ['peanuts', 'penicillin'],
    'contact_details': {'phone': '123-456-7890'}
}    

patient1 = Patient(**patient_info)

def insert_patient(patient: Patient):
    print(f"Inserting patient: {patient.name}, Age: {patient.age}")

insert_patient(patient1)
