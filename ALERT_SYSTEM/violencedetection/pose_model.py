from tensorflow.keras.models import load_model
import numpy as np

# Load the pretrained model
model_path = "violence_detection/poseModel.h5"
model = load_model(model_path)


def predict_violence(pose_data):
    """
    Takes pose data as input and returns 1 if violence is detected, 0 otherwise.
    """
    pose_data = np.array(pose_data).reshape(1, -1)  # Ensure proper input shape
    prediction = model.predict(pose_data)
    return int(
        prediction[0] > 0.5
    )  # Assuming a binary classifier (0: Non-violent, 1: Violent)
