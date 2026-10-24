import cv2
import numpy as np
import requests

# Create a valid 160x160 image
img = np.zeros((160, 160, 3), dtype=np.uint8)
cv2.imwrite("test_valid.jpg", img)

# Send to API
with open("test_valid.jpg", "rb") as f:
    files = {"file": ("test_valid.jpg", f, "image/jpeg")}
    data = {"city": "lahore"}
    r = requests.post("http://127.0.0.1:8000/predict/", data=data, files=files)
    print("STATUS:", r.status_code)
    print("RESPONSE:", r.text)
