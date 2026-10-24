# FoodGuard – AI-Powered Food Scanner

FoodGuard is an AI-powered mobile application developed as a Bachelor of Science in Computer Science Final Year Project at the **University of Central Punjab (UCP)**. The system helps users evaluate the freshness of food from an image and provides related nutrition information, local market prices, and prediction history.

> **Disclaimer:** FoodGuard is an AI-assisted decision-support tool. Its predictions are intended for guidance only and should not replace proper food-safety practices, expert advice, or personal judgment.

## Project Information

- **Project:** FoodGuard – AI Powered Food Scanner
- **Institution:** University of Central Punjab
- **Program:** BS Computer Science
- **Group ID:** F25CS191
- **Supervisor:** Ms. Rabia Arshad

### Team Members

| Registration No. | Student Name |
|---|---|
| L1F22BSCS0379 | Talha Mudassar |
| L1F22BSCS0141 | Muhammad Rehan Asghar |
| L1F23BSCS1023 | Hashir Ahmad |

## Overview

Consumers often rely on visual inspection or seller recommendations when purchasing fruits, vegetables, meat, chicken, and fish. This can lead to uncertain purchasing decisions, especially when food is partially spoiled or its quality is difficult to assess.

FoodGuard addresses this problem by allowing a user to capture or select a food image using a mobile application. The image is sent to a FastAPI backend, where a trained deep-learning model analyzes it and returns:

- Whether the image contains food or an irrelevant/non-food object
- The recognized food item
- The predicted freshness level
- Confidence scores
- Nutrition information
- Market prices for the selected district
- Prediction history for authenticated users

## Main Features

### AI Food Analysis

- Capture an image using the device camera
- Select an image from the gallery
- Detect food and reject irrelevant images
- Identify supported food items
- Classify freshness as **Fresh**, **Semi-Fresh**, or **Spoiled**
- Return prediction confidence scores

### Nutrition Information

The application can display food-related nutritional information such as:

- Serving size
- Calories/energy
- Protein
- Fat
- Carbohydrates
- Fiber

### Punjab Market Prices

FoodGuard collects and displays market-price information from official Punjab-related sources, including:

- AMIS Pakistan
- Punjab Price Control and Commodities Management Department (PCCMD)
- Punjab Sahulat Bazaar Authority (PSBA)

Prices can include minimum, maximum, DC, and PSBA values, depending on the available source data and selected district.

### Authentication and History

- User registration and login
- JWT-based authentication
- Password hashing
- Protected API endpoints
- Saved prediction history for authenticated users
- History containing food item, freshness, confidence, nutrition information, market prices, and prediction date

## Supported Food Categories

### Fruits

- Apple
- Banana
- Grape
- Guava
- Jujube
- Mango
- Orange
- Pomegranate
- Strawberry

### Vegetables

- Bell Pepper
- Bitter Gourd
- Capsicum
- Carrot
- Cucumber
- Okra
- Potato
- Tomato

### Protein Items

- Chicken
- Fish
- Meat

### Additional Classes

- Non-Food
- Irrelevant Image

### Freshness Classes

- Fresh
- Semi-Fresh
- Spoiled

## System Architecture

FoodGuard follows a client-server architecture:

```text
                         React Native / Expo Mobile App
                                      |
                                      | REST API
                                      v
                              FastAPI Backend
                                      |
             +------------------------+------------------------+
             |                        |                        |
             v                        v                        v
       AI Prediction            SQLite Database           Price Scrapers
             |                        |                        |
             v                        v                        v
       TensorFlow /              Users, history,       AMIS, PCCMD,
       MobileNetV2                nutrition, prices        and PSBA
```

### Prediction Workflow

1. The user captures or selects a food image.
2. The mobile application uploads the image to the backend.
3. The backend converts the image to RGB and resizes it to **192 × 192 pixels**.
4. MobileNetV2 preprocessing is applied.
5. The AI model predicts food/non-food status, item category, and freshness.
6. The backend retrieves nutrition and local market-price information.
7. A JSON response is returned to the mobile application.
8. The result is displayed to the user and stored in history when the user is authenticated.

## Technology Stack

### Mobile Frontend

- React Native
- Expo
- Expo Router
- TypeScript/TSX
- Axios
- Async Storage
- Expo Image Picker
- Expo File System
- React Native Reanimated

### Backend

- Python 3.12+
- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic
- Pydantic
- SQLite
- JWT authentication

### Artificial Intelligence

- TensorFlow
- Keras
- MobileNetV2 transfer learning
- OpenCV
- NumPy
- Pillow
- Scikit-learn

### Web Scraping

- Requests
- BeautifulSoup
- Selenium
- WebDriver Manager

## Repository Structure

```text
FYP__FoodGuard/
├── DATABASE/
│   ├── alembic.ini
│   ├── alembic/
│   └── sqlite.db
├── OTHERS/
│   └── README.MD
├── PREREQUISITES/
│   ├── package.json
│   ├── package-lock.json
│   ├── requirements.txt
│   └── eas.json
├── SETUP/
│   ├── setup_backend.txt
│   └── setup_frontend.txt
└── SOURCE/
    ├── AI_Model/
    │   ├── foodguard_model_training_clean.py
    │   ├── modelcode.txt
    │   └── FoodGuard_Export_Final.../
    ├── Backend/
    │   ├── app/
    │   ├── models_weights/
    │   ├── scraper/
    │   ├── static/
    │   ├── Test/
    │   ├── requirements.txt
    │   └── sqlite.db
    └── Frontend/
        ├── app/
        ├── assets/
        ├── constants/
        ├── styles/
        ├── package.json
        └── app.json
```

## Prerequisites

Install the following before running the project:

- Python 3.12 or later
- Node.js LTS and npm
- Git
- Android Studio or an Android device
- Expo Go for testing on a physical device
- Google Chrome and a compatible ChromeDriver if running the Selenium scrapers
- At least 8 GB RAM recommended; 16 GB is preferred for development

## Backend Setup

Open a terminal in the backend directory:

```bash
cd SOURCE/Backend
```

Create and activate a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Apply database migrations:

```bash
alembic upgrade head
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The backend should be available at:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

The backend requires the following model files in its configured model directory:

```text
best_model.keras
labels.pkl
model_config.json
```

The repository includes these files under `SOURCE/Backend/models_weights/` and also includes an exported model package under `SOURCE/AI_Model/`.

## Frontend Setup

Open a second terminal in the frontend directory:

```bash
cd SOURCE/Frontend
npm install
```

Configure the backend address in:

```text
SOURCE/Frontend/constants/api.ts
```

Use the appropriate address for your environment:

```text
Local machine:  http://127.0.0.1:8000
Android emulator: http://10.0.2.2:8000
Physical device: http://YOUR_LOCAL_IP:8000
```

When using a physical device, the device and the computer running the backend must be connected to the same Wi-Fi network.

Start the Expo development server:

```bash
npx expo start
```

You can then:

- Press `a` to open the Android emulator
- Scan the QR code using Expo Go on a physical device
- Use the Expo development tools to run the web version when supported

## Machine-Learning Model

The training code is available in `SOURCE/AI_Model/`. It is designed for training in Google Colab and uses Google Drive for dataset and checkpoint storage.

The model uses MobileNetV2 transfer learning and has three output heads:

- **Foodness:** food vs. irrelevant/non-food
- **Freshness:** Fresh, Semi-Fresh, or Spoiled
- **Item:** supported food-item classification

The training pipeline includes:

- Dataset collection from multiple food datasets
- Image resizing and MobileNetV2 preprocessing
- Data augmentation
- Dataset balancing and oversampling of training buckets
- Train/validation/test splitting
- Class weighting
- Two-phase training: classifier training followed by MobileNetV2 fine-tuning
- Export of the trained model and label metadata

The model expects RGB images with a size of **192 × 192 pixels**.

## Dataset Sources

The project documentation identifies publicly available datasets used for training, including datasets for fruits and vegetables, meat, and fish. These datasets are hosted on Kaggle and may need to be downloaded separately when retraining the model.

Training and deployment artifacts included in the repository include:

- `best_model.keras`
- `labels.pkl`
- `model_config.json`
- Model-training scripts

## Example API Result

A prediction response contains AI prediction data and may also include nutrition and district-pricing information. A simplified response shape is shown below:

```json
{
  "ai_prediction": {
    "item": "Carrot",
    "item_confidence": 0.84,
    "freshness": "Spoiled",
    "freshness_confidence": 0.61
  },
  "nutritional_info": {},
  "district_pricing": []
}
```

The exact response fields depend on the backend data available for the recognized item and selected district.

## Testing

Backend test files are available in:

```text
SOURCE/Backend/Test/
```

They include API and prediction-related test scripts, as well as a sample image and sample output.

Before testing prediction endpoints, confirm that:

1. The virtual environment is active.
2. Backend dependencies are installed.
3. Database migrations have been applied.
4. The model files are available in the configured directory.
5. The FastAPI server is running.

## Troubleshooting

### Backend cannot start

```bash
pip install -r requirements.txt
```

Also verify that Python 3.12+ is being used and that the virtual environment is active.

### Database or table errors

```bash
alembic upgrade head
```

### Model loading errors

Check that these files exist and are readable:

```text
best_model.keras
labels.pkl
model_config.json
```

### Frontend cannot connect to the backend

- Confirm that the backend is running.
- Check the URL in `SOURCE/Frontend/constants/api.ts`.
- Use `10.0.2.2` for an Android emulator instead of `127.0.0.1`.
- Use the computer's local IP address for a physical device.
- Ensure both devices are connected to the same network.
- Check firewall access to port `8000`.

### Expo has cached configuration

```bash
npx expo start --clear
```

### Camera or gallery access is denied

Enable the required camera or media-library permissions in the device settings and try again.

## Future Improvements

Potential future enhancements include:

- Offline AI prediction
- Multi-food detection in a single image
- Barcode scanning
- OCR-based food-label recognition
- Urdu and multilingual support
- Cloud deployment and synchronization
- Push notifications
- Voice assistant support
- AI-based food and nutrition recommendations
- Role-based access control
- Model versioning and performance monitoring

## Acknowledgements

We thank the University of Central Punjab, the Faculty of Information Technology & Computer Science, our project supervisor, the TensorFlow and FastAPI communities, React Native and Expo contributors, Kaggle dataset contributors, and the wider open-source community.

---

**FoodGuard – AI Powered Food Scanner**  
BSCS Final Year Project  
University of Central Punjab
