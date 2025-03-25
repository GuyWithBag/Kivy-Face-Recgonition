from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import numpy as np
import json
import requests
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load model
model = load_model('fruit_recognition_model.h5')

# Manually define class mappings
fruit_classes = {
    0: "apple",
    1: "garlic",
    2: "ginger",
    3: "onion",
    4: "potato"
}

# Function to get nutrition info
def get_nutrition(fruit_name):
    api_key = "AruAFSTx9fcRdxMaHf5I9p696DotbfO8W1v2HWYp"
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {"query": fruit_name, "api_key": api_key, "pageSize": 1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        foods = data.get("foods", [])
        if foods:
            nutrients = foods[0].get("foodNutrients", [])
            return {nutrient["nutrientName"]: nutrient["value"] for nutrient in nutrients[:3]}
    return {"error": "No data found."}

# Function to get recipes
def get_recipes(fruit_name):
    api_key = "6c78811f86d741188e3c416a21c496c9"
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {"query": fruit_name, "apiKey": api_key, "number": 3}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return [recipe["title"] for recipe in response.json().get("results", [])]
    return ["No recipes found."]

class FruitApp(App):
    def build(self):
        self.capture = False
        self.layout = BoxLayout(orientation='vertical')
        self.image = Image()
        self.button = Button(text='Start', size_hint=(1, 0.2))
        self.button.bind(on_press=self.toggle_camera)
        self.layout.add_widget(self.image)
        self.layout.add_widget(self.button)
        self.cap = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return self.layout

    def toggle_camera(self, instance):
        self.capture = not self.capture
        self.button.text = "Stop" if self.capture else "Start"

    def update(self, dt):
        if self.capture:
            ret, frame = self.cap.read()
            if ret:
                resized = cv2.resize(frame, (100, 100))
                normalized = resized / 255.0
                input_tensor = np.expand_dims(normalized, axis=0)
                predictions = model.predict(input_tensor, verbose=0)
                class_idx = np.argmax(predictions)
                confidence = np.max(predictions)
                fruit_name = fruit_classes.get(class_idx, "Unknown")
                label = f"{fruit_name} ({confidence:.2f})"
                nutrition = get_nutrition(fruit_name)
                recipes = get_recipes(fruit_name)
                nutrition_text = ", ".join(f"{k}: {v}" for k, v in nutrition.items())
                recipes_text = ", ".join(recipes)
                cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
                cv2.putText(frame, f"Nutrition: {nutrition_text}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255))
                cv2.putText(frame, f"Recipes: {recipes_text}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 165, 0))
                buf = cv2.flip(frame, 0).tobytes()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.image.texture = texture

    def on_stop(self):
        self.cap.release()

if _name_ == '_main_':
    FruitApp().run()