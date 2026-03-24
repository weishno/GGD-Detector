import cv2
import numpy as np

class ManualAnnotationTool:
    def __init__(self):
        self.drawing = False  # True if the mouse is being pressed
        self.ix, self.iy = -1, -1  # initial x and y coordinates
        self.bboxes = []  # list to store bounding boxes

    def draw_bbox(self, event, x, y, flags, param):
        # If the left mouse button is pressed, record the starting coordinates
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                # Draw a rectangle on the image
                img_copy = self.img.copy()
                cv2.rectangle(img_copy, (self.ix, self.iy), (x, y), (255, 0, 0), 2)
                cv2.imshow('Manual Annotation Tool', img_copy)
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            cv2.rectangle(self.img, (self.ix, self.iy), (x, y), (255, 0, 0), 2)
            self.bboxes.append((self.ix, self.iy, x, y))  # store the bbox coordinates

    def annotate_image(self, image_path):
        # Load the image and set up the mouse callback
        self.img = cv2.imread(image_path)
        cv2.namedWindow('Manual Annotation Tool')
        cv2.setMouseCallback('Manual Annotation Tool', self.draw_bbox)

        while True:
            cv2.imshow('Manual Annotation Tool', self.img)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:  # Esc key to exit
                break
            elif k == ord('s'):  # Save the annotations
                self.save_annotations()
                print('Annotations saved!')

        cv2.destroyAllWindows()

    def save_annotations(self):
        # Save the bounding boxes to a file or database
        with open('annotations.txt', 'w') as f:
            for bbox in self.bboxes:
                f.write(f'{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}\n')

# Usage Example
# if __name__ == '__main__':
#     tool = ManualAnnotationTool()
#     tool.annotate_image('path_to_image.jpg')
