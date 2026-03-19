from ultralytics import YOLO
model = YOLO("https://huggingface.co/ge7921033/food-yolov8/resolve/main/food_yolov8.pt")
model.predict(source=0, show=True)