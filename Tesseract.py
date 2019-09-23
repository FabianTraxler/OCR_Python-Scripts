import pytesseract
import cv2
import sys
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ftraxler\AppData\Local\Tesseract-OCR\tesseract.exe'


def process_image(img_path):
    # load image
    image = cv2.imread(img_path)
    # resize image
    height, width, channels = image.shape
    resize_factor = 800 / height
    resized = cv2.resize(image, (int(width * resize_factor),int(height * resize_factor)))
    # convert to grey
    grey = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    # use Tesseract Library to Recognize Characters
    data = pytesseract.image_to_data(grey, output_type=pytesseract.Output.DICT)
    text = pytesseract.image_to_string(grey)
    return data, text


def show_image(img_path):
    # load image
    image = cv2.imread(img_path)
    # resize image
    height, width, channels = image.shape
    resize_factor = 800 / height
    image = cv2.resize(image, (int(width * resize_factor),int(height * resize_factor)))
    tess_data, text = process_image(img_path)
    n_boxes = len(tess_data['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (tess_data['left'][i], tess_data['top'][i], tess_data['width'][i], tess_data['height'][i])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Output", image)
    cv2.waitKey(0)


if __name__ == '__main__':
    img_path = sys.argv[1]
    data, text = process_image(img_path)
    print(text)