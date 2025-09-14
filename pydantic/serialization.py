from pydantic  import BaseModel

class Address(BaseModel):
    state: str
    city: str
    zip_code: str
    
class Patient(BaseModel):
    name: str
    age: int
    address: Address
    
address_dict = {
    'state': 'California',
    'city': 'Los Angeles',
    'zip_code': '90001'
}

Address1= Address(**address_dict)

Patient_dict = {
    'name': 'John Doe',
    'age': 30,
    'address': Address1
}
patient1 = Patient(**Patient_dict)

temp_dict = patient1.model_dump(include={'address':{'city','zip_code'}})
print(temp_dict)

temp_json = patient1.model_dump_json(exclude={'address':{'state'}})
print(temp_json)