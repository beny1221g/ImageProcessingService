import os
import cv2
import numpy as np

class Img:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image_data = self.load_image()

    def load_image(self):
        try:
            image = cv2.imread(self.image_path)
            if image is not None:
                return image
            else:
                raise FileNotFoundError(" Unable to load image.")
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def save_image(self, image_data, suffix='_filtered'):
        try:
            directory = 'images'
            if not os.path.exists(directory):
                os.makedirs(directory)

            file_path = os.path.join(directory, f"{os.path.basename(self.image_path).split('.')[0]}{suffix}.jpg")
            cv2.imwrite(file_path, image_data)
            print(f"Image saved successfully: {file_path}")
            return file_path
        except Exception as e:
            print(f"Error saving image: {e}")
            return None

    def blur(self, blur_level=16):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")
            blur_level = max(1, blur_level)
            blur_level = blur_level + 1 if blur_level % 2 == 0 else blur_level
            blurred_image = cv2.GaussianBlur(self.image_data, (blur_level, blur_level), 0)
            return blurred_image
        except Exception as e:
            print(f"Error applying blur: {e}")
            return None

    def rotate(self):
        try:
            img = cv2.imread(self.image_path)
            if img is None:
                raise FileNotFoundError("Unable to load image.")
            rotated_img = cv2.rotate(img, cv2.ROTATE_180)
            return rotated_img
        except Exception as e:
            print(f"Error rotating image: {e}")
            return None

    def salt_n_pepper(self, amount=0.05):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")
            noisy_image = self.image_data.copy()
            mask = np.random.choice([0, 1, 2], size=noisy_image.shape[:2], p=[amount / 2, amount / 2, 1 - amount])
            noisy_image[mask == 0] = 0
            noisy_image[mask == 1] = 255
            return noisy_image
        except Exception as e:
            print(f"Error adding salt and pepper noise: {e}")
            return None

    def concat(self, other_image_data, direction='horizontal'):
        try:
            if self.image_data is None or other_image_data is None:
                raise ValueError("Image data is missing.")

            if direction not in ['horizontal', 'vertical']:
                raise ValueError("Invalid direction. Please use 'horizontal' or 'vertical'.")

            if direction == 'horizontal':
                concatenated_img = np.concatenate((self.image_data, other_image_data), axis=1)
            else:
                concatenated_img = np.concatenate((self.image_data, other_image_data), axis=0)

            return concatenated_img
        except Exception as e:
            print(f"Error concatenating images: {e}")
            return None

    def segment(self, num_clusters=100):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")

            image_rgb = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2RGB)
            pixels = image_rgb.reshape((-1, 3))
            pixels = np.float32(pixels)

            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
            _, labels, centers = cv2.kmeans(pixels, num_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

            centers = np.uint8(centers)
            segmented_image = centers[labels.flatten()]
            segmented_image = segmented_image.reshape(image_rgb.shape)

            # Convert segmented image back to BGR format
            segmented_image_bgr = cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR)

            # Darken the segmented image
            segmented_image_bgr = segmented_image_bgr * 0.5  # Reduce brightness by 50%

            return segmented_image_bgr
        except Exception as e:
            print(f"Error segmenting image: {e}")
            return None



    def grayscale(self):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")
            gray_image = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2GRAY)
            return cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
        except Exception as e:
            print(f"Error converting image to grayscale: {e}")
            return None

    def sharpen(self):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            sharpened_image = cv2.filter2D(self.image_data, -1, kernel)
            return sharpened_image
        except Exception as e:
            print(f"Error applying sharpen filter: {e}")
            return None

    def emboss(self):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")
            kernel = np.array([[0, -1, -1], [1, 0, -1], [1, 1, 0]])
            embossed_image = cv2.filter2D(self.image_data, -1, kernel)
            return embossed_image
        except Exception as e:
            print(f"Error applying emboss filter: {e}")
            return None

    def invert_colors(self):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")
            inverted_image = cv2.bitwise_not(self.image_data)
            return inverted_image
        except Exception as e:
            print(f"Error inverting colors: {e}")
            return None

    def oil_painting(self, size=7, dynRatio=0.2):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")

            # Convert image to grayscale
            gray_image = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2GRAY)

            # Apply median blur to create a smoother image
            blurred_image = cv2.medianBlur(gray_image, size)

            # Apply adaptive threshold to create a binary image
            _, mask = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # Create an output image using bitwise and operation with original image
            oil_painting_effect = cv2.bitwise_and(self.image_data, self.image_data, mask=mask)

            return oil_painting_effect
        except Exception as e:
            print(f"Error applying oil painting effect: {e}")
            return None
    def cartoonize(self):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")
            gray_image = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2GRAY)
            blurred_image = cv2.medianBlur(gray_image, 7)
            edges = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
            color = cv2.bilateralFilter(self.image_data, 9, 300, 300)
            cartoon_image = cv2.bitwise_and(color, color, mask=edges)
            return cartoon_image
        except Exception as e:
            print(f"Error cartoonizing image: {e}")
            return None