from pydantic import BaseModel, EmailStr,AnyUrl,Field , field_validator,model_validator,computed_field
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
    
    @field_validator('age',mode='after')
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError("Age must be between 0 and 100")
    
    @field_validator('name')
    @classmethod
    def Upper_name(cls,value):
        return value.upper()
    
    @field_validator('email')
    @classmethod
    def validate_email_domain(cls, value):
        valid_domain =['ebl.com', 'gbl.com', 'nbl.com']
        domain_name = value.split('@')[-1]
        
        if domain_name not in valid_domain:
            raise ValueError(f"Email domain must be one of the following: {', '.join(valid_domain)}")
        return value
    
    @model_validator(mode='after')
    def valid_emergency_contact(cls,model):
        if model.age >60  and 'emergency_contact' not in model.contact_details:
            raise ValueError("Emergency contact is required for patients over 60")
        return model
    
    @computed_field
    @property
    def BMI(self) -> float:
        BMI = self.weight / ((self.age/100) ** 2)
        return  round(BMI,2)
    
    
patient_info = {
    'name': 'John Doe',
    "LinkedIn": "https://www.linkedin.com/in/johndoe",
    'age': '78',
    'email': 'abc@gbl.com',
    'weight': 70.5,
    'married': False,
    'allergies': ['peanuts', 'penicillin'],
    'contact_details': {'phone': '123-456-7890','emergency_contact':'987-654-3210'}
}    

patient1 = Patient(**patient_info)

def insert_patient(patient: Patient):
    print(f"Inserting patient: {patient.name}, Age: {patient.age},BMI: {patient.BMI}")

insert_patient(patient1)
