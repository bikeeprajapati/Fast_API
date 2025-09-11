from pydantic import BaseModel
from typing import List, Dict

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    married = bool
    allergies: List[str]
    contact_details: Dict[str, str]

patient_info ={'name': 'John Doe', 'age': 30 , 'weight': 70.5, 'married': False, 'allergies': ['peanuts', 'penicillin'], 'contact_details': {'phone': '123-456-7890', 'email': 'abc@gmail.com'}}    

patient1 = Patient(**patient_info)

def insert_patient(patient: Patient):
    print(f"Inserting patient: {patient.name}, Age: {patient.age}")
    
insert_patient(patient1)