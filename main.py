from fastapi import FastAPI , Path,HTTPException , Query 
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field , computed_field
from typing  import Annotated , Literal , Optional
import json

class Patient(BaseModel):
    id: Annotated[int ,Field(...,gt=0, description="The ID of the patient", example=1)]
    name :Annotated[str, Field(...,min_length=1, max_length=100, description="The name of the patient", example="John Doe")]
    age : Annotated[int, Field(...,gt=0, lt=150, description="The age of the patient", example=30)]
    gender : Annotated[Literal['male','female','other'], Field(..., description="The gender of the patient", example="male")]
    blood_group : Annotated[Literal['A+','A-','B+','B-','AB+','AB-','O+','O-'], Field(..., description="The blood group of the patient", example="O+")]
    medical_history : Annotated[list[str], Field(..., description="The medical history of the patient", example=["diabetes", "hypertension"])]
    
    
    @computed_field
    @property
    def BMI(self) -> float:
        # Dummy implementation for BMI calculation
        return round(22.5, 2)  # Replace with actual calculation if height and weight are available

class PatientUpdate(BaseModel):
    name : Optional[Annotated[str, Field(None,min_length=1, max_length=100, description="The name of the patient", example="John Doe")]]
    age : Optional[Annotated[int, Field(None,gt=0, lt=150, description="The age of the patient", example=30)]]
    gender : Optional[Annotated[Literal['male' , 'female' , 'other'], Field(None, description="the gender of the patient",)]]
    blood_group : Optional[Annotated[Literal['A+','A-','B+','B-','AB+','AB-','O+','O-'], Field(None, description="The blood group of the patient", example="O+")]]
    medical_history : Optional[Annotated[list[str], Field(None, description="The medical history of the patient", example=["diabetes", "hypertension"])]]
    


app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data   

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=4)



@app.get("/")
def hello():
    return {"message": "patients management system api"}

@app.get("/about")
def about():
    return {"message": "this is a patient management system api"}

@app.get("/patient/{patient_id}")

def view_patients(patient_id: int = Path(..., description="The ID of the patient to retrieve", example=1,gt=0)):
    data = load_data()
    
    for patient in data:
        if patient["id"] == patient_id:
            return patient
        
    
        raise HTTPException(status_code=404, detail="Patient not found")
    
    
    

@app.get('/sort')
def sort_patients(
    sort_by: str = Query(..., description="The field to sort by: age, gender, blood_group"),
    order: str = Query("asc", description="The order to sort by: asc or desc")
):

    valid_sort_fields = ["age","gender","blood_group"]
    if sort_by not  in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are:{valid_sort_fields}")
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Valid orders are: asc or desc")
    data = load_data()
    sorted_data = sorted(data, key=lambda x: x[sort_by], reverse=(order=="desc"))
    return sorted_data


@app.post("/add_patient")
def add_patient(patient: Patient):
    data = load_data()
    
    # Check if patient with this ID already exists
    for p in data:
        if p["id"] == patient.id:
            raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    
    # Append new patient (convert model -> dict)
    data.append(patient.dict())
    
    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Patient added successfully"})

@app.put("/update_patient/{patient_id}")
def update_patient(patient_id: int ,patient_update: PatientUpdate):
     data = load_data()
     # Find patient by ID
     for i, patient in enumerate(data):
        if patient["id"] == patient_id:
            # Only update provided fields
            updated_data = patient_update.model_dump(exclude_unset=True)
            for key, value in updated_data.items():
                patient[key] = value

            data[i] = patient
            save_data(data)
            return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})

    # If not found
     raise HTTPException(status_code=404, detail="Patient not found")
 
@app.delete("/delete_patient/{patient_id}")
def delete_patient(patient_id: int):
    data = load_data()
    
    for i , patient  in enumerate(data):
        if patient["id"] == patient_id:
            del data[i]
            save_data(data)
            return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})