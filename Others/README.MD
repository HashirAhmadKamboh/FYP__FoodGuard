#  FoodGuard – AI Powered Food Scanner


**Project Title**

FoodGuard: AI Powered Food Scanner

**University**

University of Central Punjab (UCP)

Faculty of Information Technology & Computer Science

Bachelor of Science in Computer Science (BSCS)

**Group ID**

F25CS191

---

# Team Members

| Registration No. | Student Name |
|------------------|--------------|
| L1F22BSCS0379 | Talha Mudassar |
| L1F22BSCS0141 | Muhammad Rehan Asghar |
| L1F23BSCS1023 | Hashir Ahmad |

---

# Supervisor

Ms. Rabia Arshad

---

# Project Overview

FoodGuard is an Artificial Intelligence powered mobile application developed to assist consumers in evaluating the freshness of raw food before purchasing or consuming it.

The system combines Computer Vision, Deep Learning, Mobile Development, Backend APIs, Database Management, and Automated Government Market Price Collection into one complete software solution.

Unlike traditional food freshness applications that only classify fruits or vegetables, FoodGuard provides an end-to-end intelligent platform capable of:

- AI based food freshness prediction
- Food item recognition
- Irrelevant image detection
- Nutrition information
- Punjab government market prices
- User authentication
- Prediction history
- Mobile application interface
- FastAPI backend services

The application was developed as the Final Year Project for the BS Computer Science program at the University of Central Punjab.

---

# Problem Statement

Consumers often purchase fruits, vegetables, chicken, meat, and fish based only on visual inspection or seller recommendations. This approach is subjective and may result in poor purchasing decisions.

FoodGuard addresses this problem by providing an AI-assisted system that analyzes food images captured using a smartphone camera and predicts the freshness level of supported food items.

The application also increases consumer awareness by presenting nutritional information and official Punjab market prices within the same mobile application.

---

# Objectives

The primary objectives of FoodGuard are:

- Develop an AI-powered food freshness detection system.
- Identify supported food items using deep learning.
- Detect Fresh, Semi-Fresh, and Spoiled food.
- Reject irrelevant or non-food images.
- Display nutritional information.
- Display Punjab government market prices.
- Store prediction history.
- Demonstrate practical integration of AI with mobile and backend technologies.
- Develop a scalable client-server architecture.
- Provide a user-friendly mobile application.

---

# Major Features

## Authentication

- User Registration
- User Login
- JWT Authentication
- Secure Password Hashing

---

## AI Prediction

- Camera Capture
- Gallery Upload
- Food Detection
- Freshness Detection
- Confidence Score
- Non-Food Detection

---

## Nutrition Module

Displays nutritional information including:

- Serving Size
- Calories
- Protein
- Fat
- Carbohydrates
- Fiber

---

## Punjab Market Prices

Displays latest market prices collected from official government sources.

Supported Sources:

- AMIS
- PCCMD
- Punjab Sahulat Bazaar Authority

---

## Prediction History

Authenticated users can view:

- Previous Predictions
- Food Item
- Freshness
- Confidence
- Nutrition Information
- Market Prices
- Prediction Date

---

# Supported Categories

## Fruits

- Apple
- Banana
- Grape
- Guava
- Jujube
- Mango
- Orange
- Pomegranate
- Strawberry

---

## Vegetables

- Bell Pepper
- Bitter Gourd
- Capsicum
- Carrot
- Cucumber
- Okra
- Potato
- Tomato

---

## Protein Items

- Chicken
- Fish
- Meat

---

## Freshness Classes

- Fresh
- Semi-Fresh
- Spoiled

---

## Other Classes

- Non-Food
- Irrelevant Image

---

# System Architecture

The FoodGuard system follows a Client–Server Architecture.

```
                React Native Mobile App
                         │
                         │ REST API
                         ▼
                 FastAPI Backend Server
                         │
        ┌────────────────┼─────────────────┐
        │                │                 │
        ▼                ▼                 ▼
 AI Prediction     SQLite Database    Price Scraper
        │                │                 │
        ▼                ▼                 ▼
 TensorFlow      Users / History     AMIS
 MobileNetV2     Nutrition           PCCMD
                 Prices              PSBA
```

---

# Technology Stack

## Mobile Development

- React Native
- Expo
- JavaScript
- Axios

---

## Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- Uvicorn
- JWT Authentication

---

## Artificial Intelligence

- TensorFlow
- Keras
- MobileNetV2
- OpenCV
- NumPy
- Pillow

---

## Database

- SQLite

---

## Web Scraping

- BeautifulSoup
- Selenium
- Requests
- WebDriver Manager

---

## Development Tools

- Google Colab
- VS Code
- Android Studio
- Git
- GitHub

---

# Folder Structure

```
FoodGuard/

│
├── dataset/
│
├── foodguard_backend/
│
├── foodguard_frontend/
│
├── model_training/
│
└── others/
```

---

## Backend Folder

Contains:

- FastAPI APIs
- Authentication
- AI Prediction
- Nutrition APIs
- Price APIs
- History APIs
- Database Models
- SQLAlchemy
- Alembic
- Web Scraper
- AI Integration

---

## Frontend Folder

Contains:

- React Native Screens
- Navigation
- Components
- API Calls
- Authentication UI
- Prediction UI
- Nutrition UI
- Market Rates UI
- History UI

---

## Model Training

Contains:

- Training Code
- Google Colab Notebook
- Dataset Preparation
- Image Augmentation
- Model Export
- Evaluation

Generated Files

- best_model.keras
- labels.pkl
- model_config.json

---

## Dataset Folder

Contains all datasets used for AI model training.

---

# Dataset Sources

The AI model was trained using publicly available datasets obtained from Kaggle. Multiple datasets were combined to improve class diversity and support different food categories.

## Fruits and Vegetables

Food Freshness Dataset

https://www.kaggle.com/datasets/ulnnproject/food-freshness-dataset/code

Fresh and Stale Classification Dataset

https://www.kaggle.com/datasets/swoyam2609/fresh-and-stale-classification

---

## Meat Dataset

Meat Quality Assessment Dataset

https://www.kaggle.com/datasets/crowww/meat-quality-assessment-based-on-deep-learning

---

## Fish Dataset

Freshness Fish Dataset

https://www.kaggle.com/datasets/atcharachumpol/freshness-fish-dataset

---

# External Data Sources

FoodGuard also collects market prices from official Punjab Government websites.

- AMIS Pakistan
- Punjab Price Control and Commodities Management Department (PCCMD)
- Punjab Sahulat Bazaar Authority (PSBA)

---

# AI Model Workflow

1. User uploads image.
2. Backend receives image.
3. Image is resized.
4. Image converted to RGB.
5. MobileNetV2 preprocessing applied.
6. AI model predicts:
   - Food / Non-Food
   - Food Item
   - Freshness
7. Backend retrieves:
   - Nutrition
   - Market Prices
8. JSON response returned.
9. Mobile application displays prediction.

---

# Database

SQLite stores:

- Users
- Authentication Tokens
- Prediction History
- Nutrition Profiles
- Commodities
- Price Records

---

# Security Features

- Password Hashing
- JWT Authentication
- Token Verification
- Protected APIs
- Input Validation
- Secure User Sessions

---

# Future Improvements

Future versions of FoodGuard may include:

- Offline AI Prediction
- Multi-food Detection
- Barcode Scanner
- Cloud Deployment
- Voice Assistant
- Urdu Language Support
- iOS Version
- AI Recommendation Engine
- Real-Time Notifications
- Nutrition Recommendation System

---

# Project Deliverables

This repository contains:

- React Native Source Code
- FastAPI Backend
- SQLite Database
- AI Model
- Dataset
- Model Training Code
- Documentation
- Installation Guide
- User Manual
- Presentation
- Final Report

---

# Disclaimer

FoodGuard is an AI-assisted decision support application.

Predictions are generated using a trained deep learning model and should be considered as guidance only. Users should continue to use proper food safety practices and personal judgment before consuming any food item. The application is not intended to replace professional laboratory testing or official food safety inspections.

---

# Acknowledgements

We sincerely thank:

- University of Central Punjab
- Faculty of Information Technology & Computer Science
- Our Project Supervisor
- TensorFlow Team
- FastAPI Community
- React Native Community
- Kaggle Dataset Contributors
- Open Source Community

for providing the tools, datasets, and guidance that made this project possible.


FoodGuard – AI Powered Food Scanner

BSCS Final Year Project

University of Central Punjab

All Rights Reserved.