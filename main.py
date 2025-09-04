from fastapi import FastAPI , Path,HTTPException , Query
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data   



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