from ultralytics import YOLO

model = YOLO('custrom.pt')

model.predict(source='data/images', show=True)