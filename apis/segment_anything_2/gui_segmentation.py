import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, 
    QSlider, QListWidget, QWidget, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QBrush, QPen, QFont
from PIL import Image
import matplotlib.pyplot as plt
import torch
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor

class SegmentationGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive Segmentation with SAM 2")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize SAM 2 model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        sam2_checkpoint = "./checkpoints/sam2.1_hiera_large.pt"
        model_cfg = "configs/sam2.1/sam2.1_hiera_l.yaml"
        self.sam2_model = build_sam2(model_cfg, sam2_checkpoint, device=self.device)
        self.predictor = SAM2ImagePredictor(self.sam2_model)

        # GUI components
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.mousePressEvent = self.on_image_click

        self.list_widget = QListWidget(self)
        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear_selections)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.update_score_threshold)

        self.score_label = QLabel("Score Threshold: 0.50", self)

        # Layouts
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QLabel("Objects:"))
        controls_layout.addWidget(self.list_widget)
        controls_layout.addWidget(self.clear_button)
        controls_layout.addWidget(self.score_label)
        controls_layout.addWidget(self.slider)

        layout.addLayout(controls_layout)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # State variables
        self.image = None
        self.segmented_objects = []
        self.score_threshold = 0.50
        self.highlighted_index = -1  # Track the highlighted object index
        self.list_widget.itemClicked.connect(self.on_list_item_click)  # Connect list click event

    def load_image(self, image_path):
        self.image = Image.open(image_path)
        self.image = np.array(self.image.convert("RGB"))
        self.predictor.set_image(self.image)
        self.display_image(self.image)

    def display_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

    def on_image_click(self, event):
        if self.image is None:
            return

        x = event.pos().x()
        y = event.pos().y()
        input_point = np.array([[x, y]])
        input_label = np.array([1])

        masks, scores, _ = self.predictor.predict(
            point_coords=input_point,
            point_labels=input_label,
            multimask_output=True,
        )

        sorted_ind = np.argsort(scores)[::-1]
        masks = masks[sorted_ind]
        scores = scores[sorted_ind]

        for mask, score in zip(masks, scores):
            if score >= self.score_threshold:
                self.segmented_objects.append((mask, score))
                self.segmented_objects.sort(key=lambda obj: np.sum(obj[0]), reverse=True)  # Sort by area
                self.update_segmented_list()
                self.display_mask_on_image()  # Update display without highlight
                break

    def display_mask_on_image(self, highlight_index=None):
        overlay = self.image.copy()

        # Combine all masks
        for i, (mask, _) in enumerate(self.segmented_objects):
            mask = mask.astype(bool)  # Ensure mask is a boolean array
            if i == highlight_index:  # Highlight the selected mask
                overlay[mask] = [0, 255, 0]  # Highlight in green
            else:
                overlay[mask] = overlay[mask] * 0.5 + np.array([255, 0, 0]) * 0.5  # Half-transparent red

        # Create a QPixmap to draw labels
        height, width, channel = overlay.shape
        bytes_per_line = 3 * width
        q_image = QImage(overlay.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        painter = QPainter(pixmap)

        # Draw labels for each object
        painter.setPen(QPen(Qt.white))
        painter.setFont(QFont("Arial", 16))
        for i, (obj_mask, _) in enumerate(self.segmented_objects):
            obj_mask = obj_mask.astype(bool)
            y, x = np.argwhere(obj_mask).mean(axis=0).astype(int)  # Get the center of the mask
            painter.drawText(x, y, f"{i + 1}")  # Draw label number

        painter.end()
        self.image_label.setPixmap(pixmap)

    def on_list_item_click(self, item):
        self.highlighted_index = self.list_widget.row(item)  # Get the clicked item's index
        self.display_mask_on_image(highlight_index=self.highlighted_index)  # Update display

    def update_segmented_list(self):
        self.list_widget.clear()
        for i, (mask, score) in enumerate(self.segmented_objects):
            area = np.sum(mask)
            self.list_widget.addItem(f"Object {i + 1}: Score {score:.2f}, Area {area}")

    def clear_selections(self):
        self.segmented_objects = []
        self.list_widget.clear()
        self.highlighted_index = -1  # Reset highlighted index
        self.display_image(self.image)  # Reset to the original image

    def update_score_threshold(self):
        self.score_threshold = self.slider.value() / 100
        self.score_label.setText(f"Score Threshold: {self.score_threshold:.2f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = SegmentationGUI()

    # Load an example image
    image_path, _ = QFileDialog.getOpenFileName(gui, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
    if image_path:
        gui.load_image(image_path)

    gui.show()
    sys.exit(app.exec_())
