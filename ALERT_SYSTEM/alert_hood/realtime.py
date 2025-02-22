import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
import tensorflow as tf
import h5py
import json

# Load video
#video_path = "Violent.mov"
cap = cv2.VideoCapture(0)

# Initialize Mediapipe
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

# Load Model Properly
custom_objects = {'Orthogonal': tf.keras.initializers.Orthogonal}

with h5py.File("poseModel.h5", 'r') as f:
    model_config = json.loads(f.attrs.get('model_config'))  
    for layer in model_config['config']['layers']:
        if 'time_major' in layer['config']:
            del layer['config']['time_major']

    model = tf.keras.models.model_from_json(json.dumps(model_config), custom_objects=custom_objects)
    
    # Load weights correctly
    weights_group = f['model_weights']
    for layer in model.layers:
        layer_name = layer.name
        if layer_name in weights_group:
            weight_names = weights_group[layer_name].attrs['weight_names']
            layer_weights = [weights_group[layer_name][weight_name] for weight_name in weight_names]
            layer.set_weights(layer_weights)

lm_list = []
label = "neutral"


def make_landmark_timestep(results):
    c_lm = []
    for lm in results.pose_landmarks.landmark:
        c_lm.append(lm.x)
        c_lm.append(lm.y)
        c_lm.append(lm.z)
        c_lm.append(lm.visibility)

    return c_lm

# Function to draw pose on frame
def draw_landmark_on_image(mpDraw, results, frame):
    mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
    return frame

# Function to draw predicted label
def draw_class_on_image(label, img):
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 255, 0) if label == "neutral" else (0, 0, 255)
    cv2.putText(img, str(label), (10, 30), font, 1, color, 2, 2)
    return img

# Violence detection function (NO THREADING)
def detect(model, lm_list):
    global label
    lm_list = np.array(lm_list)

    # Ensure correct shape before prediction
    print(f"DEBUG: Input shape to model: {lm_list.shape}")  # Should be (1, 40, 131)
    
    lm_list = np.expand_dims(lm_list, axis=0)  # Make it (1, 40, 131)

    # Normalize input (if needed)
    lm_list = lm_list / np.linalg.norm(lm_list)

    result = model.predict(lm_list)
    print(f"DEBUG: Raw Model Prediction: {result}")

    # Adjust threshold if needed
    label = "violent" if result[0][0] < 0.35 else "neutral"
    if label=="violent":
        with open('rojan.txt', 'w') as file:
            file.write('0')
    return str(label)

# Frame processing
i = 0
warm_up_frames = 40

while True:
    ret, frame = cap.read()
    if not ret:
        break  # Exit when video ends

    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frameRGB)
    i += 1

    if i > warm_up_frames and results.pose_landmarks:
        lm = make_landmark_timestep(results)
        lm_list.append(lm)

        if len(lm_list) == 50:  # Make batch of 50 frames
            label = detect(model, lm_list)
            lm_list = []  # Reset list

        # Draw bounding box
        x_coords = [int(lm.x * frame.shape[1]) for lm in results.pose_landmarks.landmark]
        y_coords = [int(lm.y * frame.shape[0]) for lm in results.pose_landmarks.landmark]
        cv2.rectangle(frame, (min(x_coords), max(y_coords)), (max(x_coords), min(y_coords) - 25), (0, 255, 0), 1)

        frame = draw_landmark_on_image(mpDraw, results, frame)

    frame = draw_class_on_image(label, frame)
    cv2.imshow("image", frame)

    if cv2.waitKey(1) == ord('q'):
        break


