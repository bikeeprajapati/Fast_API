from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd
import os

# Load model
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]


# Pydantic model with computed fields inside the class
class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age must be between 1 and 119")]
    weight: Annotated[float, Field(..., gt=0, lt=500, description="Weight must be between 1 and 499")]
    height: Annotated[float, Field(..., gt=0, lt=300, description="Height must be between 1 and 299")]
    income_lpa: Annotated[float, Field(..., gt=0, lt=1000, description="Income must be between 1 and 999")]
    smoker: Annotated[Literal["yes", "no"], Field(..., description="Smoker must be either 'yes' or 'no'")]
    city: Annotated[Literal["tier_1", "tier_2", "tier_3"], Field(..., description="City must be 'tier_1', 'tier_2' or 'tier_3'")]
    occupation: Annotated[
        Literal["retired", "freelancer", "student", "government_job",
                "business_owner", "unemployed", "private_job"],
        Field(..., description="Occupation must be one of the allowed categories")
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker == "yes" and self.bmi > 30:
            return "high"
        elif self.smoker == "yes" and self.bmi > 27:
            return "medium"
        return "low"

    @computed_field
    @property
    def city_tier(self) -> int:
        # Direct mapping because input is already "tier_1", "tier_2", "tier_3"
        return int(self.city.split("_")[1])

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"


@app.post("/predict")
def predict_premium(input_data: UserInput):
    input_df = pd.DataFrame([{
        "bmi": input_data.bmi,
        "age_group": input_data.age_group,
        "lifestyle_risk": input_data.lifestyle_risk,
        "city_tier": input_data.city_tier,
        "income_lpa": input_data.income_lpa,
        "occupation": input_data.occupation
    }])

    prediction = model.predict(input_df)[0]

    return JSONResponse(content={"predicted_insurance_premium_category": prediction})
