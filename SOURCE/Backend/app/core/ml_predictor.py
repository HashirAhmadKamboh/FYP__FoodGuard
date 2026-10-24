import os
import cv2
import json
import pickle
import numpy as np
import tensorflow as tf
from app.core.config import MODEL_DIR

class FoodGuardPredictor:
    def __init__(self):
        self.model = None
        self.item_map = {}
        self.freshness_list = []
        self.img_size = (160, 160)
        self.load_model()

    def load_model(self):
        print("Loading Deep Learning Model...")
        model_path = os.path.join(MODEL_DIR, "best_model.keras")
        labels_path = os.path.join(MODEL_DIR, "labels.pkl")
        
        self.model = tf.keras.models.load_model(model_path)
        
        with open(labels_path, "rb") as f:
            labels_data = pickle.load(f)
            # Invert item map to get {0: 'Apple', 1: 'Banana'}
            self.item_map = {v: k for k, v in labels_data["item_map"].items()}
            self.freshness_list = labels_data["freshness_list"]
            self.img_size = tuple(labels_data["img_size"])
            self.irrelevant_threshold = labels_data.get("irrelevant_threshold", 0.55)
            self.confidence_threshold = labels_data.get("confidence_threshold", 0.60)
        print("Model Loaded Successfully!")

    def predict(self, image_bytes):
        # Decode image
        np_img = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Failed to decode image bytes")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, self.img_size)
        
        # Normalize: pixel/127.5 - 1.0 (as per your training script)
        img = img.astype("float32") / 127.5 - 1.0
        img = np.expand_dims(img, axis=0) # Add batch dimension

        # Predict
        predictions = self.model.predict(img)
        foodness_prob = float(predictions["foodness"][0][0])
        freshness_pred = predictions["freshness"][0]
        item_pred = predictions["item"][0]

        freshness_idx = np.argmax(freshness_pred)
        item_idx = np.argmax(item_pred)

        item_name = self.item_map[item_idx]
        freshness_name = self.freshness_list[freshness_idx]

        # Determine if it is food or irrelevant/NonFood
        is_food = True
        irrelevant_threshold = getattr(self, "irrelevant_threshold", 0.55)
        if foodness_prob < irrelevant_threshold or item_name == "NonFood":
            is_food = False

        return {
            "item": item_name,
            "item_confidence": float(item_pred[item_idx]),
            "freshness": freshness_name,
            "freshness_confidence": float(freshness_pred[freshness_idx]),
            "foodness_prob": foodness_prob,
            "is_food": is_food
        }

ml_model = FoodGuardPredictor()