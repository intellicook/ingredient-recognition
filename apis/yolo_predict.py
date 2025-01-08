from ultralytics import YOLO
import cv2

# Load the trained model
model = YOLO('model/train/runs/detect/train/weights/best.pt')

def yolo_detect(image_path: str, threshold: float = 0.5):
    """Detect ingredients in the provided image."""
    results = model.predict(source=image_path, show=False)
    ingredients = []
    for result in results:
        for box in result.boxes:
            xyxy = box.xyxy.tolist()[0]  # Convert tensor to list and access the first element
            x1, y1, x2, y2 = xyxy[0], xyxy[1], xyxy[2], xyxy[3]
            class_id = int(box.cls.tolist()[0])
            class_name = model.names[class_id]  # Get class name from model's class labels
            if box.conf.tolist()[0] > threshold:
              ingredients.append({
                  'name': class_name,
                  'probability': box.conf.tolist()[0],
                  'x': x1,
                  'y': y1,
                  'width': x2 - x1,
                  'height': y2 - y1
              })
    print("yolo_detect: ", ingredients)
    return ingredients

def visualize_detections(image_path: str, detections: list):
    """Visualize the detected ingredients on the image."""
    image = cv2.imread(image_path)
    for detection in detections:
        x1, y1 = int(detection['x']), int(detection['y'])
        x2, y2 = x1 + int(detection['width']), y1 + int(detection['height'])
        label = f"{detection['name']} ({detection['probability']:.2f})"
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    # cv2.imshow('Detections', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    output_path = "output/yolo_output.jpg"
    cv2.imwrite(output_path, image)

if __name__ == "__main__":
    # Example usage
    image_path = 'tests/fridge.png'
    detected_ingredients = yolo_detect(image_path, 0.35)
    print(detected_ingredients)
    visualize_detections(image_path, detected_ingredients)
