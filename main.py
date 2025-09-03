from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data   # ✅ return the data

@app.get("/view")
def view():
    data = load_data()
    return data   # ✅ will return the JSON content

@app.get("/")
def hello():
    return {"message": "patients management system api"}

@app.get("/about")
def about():
    return {"message": "this is a patient management system api"}
