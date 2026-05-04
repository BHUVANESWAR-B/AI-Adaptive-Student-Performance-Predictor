import torch
import numpy as np

# Load trained model
model_path = "models/dkt_model.pt"

try:
    model = torch.load(model_path, map_location="cpu")
    model.eval()
except:
    model = None


def predict_mastery(skill_id, correct):

    if model is None:
        # fallback if model not loaded
        return np.random.uniform(0.4, 0.9)

    x = torch.tensor([[skill_id]])
    y = torch.tensor([[correct]])

    with torch.no_grad():
        output = model(x, y)

    mastery_prob = float(output.squeeze())

    return mastery_prob