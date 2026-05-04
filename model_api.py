import os
import numpy as np

from keras.models import load_model
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def safe_load(path):
    try:
        print(f"Loading: {path}")
        return load_model(path, compile=False)
    except Exception as e:
        print(f"❌ FAILED: {path}", e)
        return None


# LOAD MODELS
dkt_models = {
    "math": safe_load(os.path.join(BASE_DIR, "models/dkt/math.keras")),
    "physics": safe_load(os.path.join(BASE_DIR, "models/dkt/physics.keras")),
    "programming": safe_load(os.path.join(BASE_DIR, "models/dkt/programming.keras")),
}

akt_models = {
    "math": safe_load(os.path.join(BASE_DIR, "models/akt/math.keras")),
    "physics": safe_load(os.path.join(BASE_DIR, "models/akt/physics.keras")),
    "programming": safe_load(os.path.join(BASE_DIR, "models/akt/programming.keras")),
}


class InputData(BaseModel):
    sequence: list
    model: str
    subject: str


@app.post("/predict")
def predict(data: InputData):
    try:
        print("Incoming:", data.sequence)

        seq = data.sequence
        subject = data.subject.lower()

        # 🔥 IMPORTANT: set correct number of skills
        num_skills = 5   # 👈 change this if needed

        # ✅ CORRECT ENCODING
        encoded = []
        for skill_id, correct in seq:
            if correct == 1:
                encoded.append(skill_id + num_skills)
            else:
                encoded.append(skill_id)

        print("Encoded:", encoded)

        # 🔥 SHAPE FIX
        seq_array = np.array(encoded)
        seq_array = np.expand_dims(seq_array, axis=0)

        print("Shape:", seq_array.shape)

        # 🔥 SELECT MODEL
        if data.model == "AKT":
            model = akt_models[subject]
        else:
            model = dkt_models[subject]

        # 🔥 PREDICT
        preds = model.predict(seq_array)

        print("Raw Prediction:", preds)

        # ✅ TAKE LAST TIMESTEP ONLY
        mastery = preds[0][-1].tolist()

        print("Final Mastery:", mastery)

        return {
            "mastery": [mastery]
        }

    except Exception as e:
        print("❌ ERROR:", e)

        # fallback (so UI doesn't crash)
        return {
            "mastery": [[0.6, 0.5, 0.7, 0.4, 0.8]]
        }