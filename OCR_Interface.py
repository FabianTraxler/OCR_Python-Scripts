# This file is meant to test different OCR APIs with self made pictures
# Test Pictures have to be stored in 'test_pictures' folder
import Tesseract as ts
import APIs as api
from os import walk
import sys
from pprint import pprint
import json


def analyze_image(img_path):
    results = {}

    # get result from tesseract
    data, tess_text = ts.process_image(img_path)
    results['Tesseract'] = tess_text

    # get result from Google Cloud Vision API
    google_text = api.google_process_image(img_path)
    results['Google'] = google_text

    # get result from Microsoft Cognitive API
    microsoft_text = api.microsoft_process_image(img_path)
    results['Microsoft'] = microsoft_text

    # get result from Microsoft Cognitive API
    abbyy_text = api.abbyy_process_image(img_path)
    results['Abbyy'] = abbyy_text


    # get result from Amazon Textract
    amazon_text = api.amazon_process_image(img_path)
    results['Amazon'] = amazon_text

    return results


def analyze_images(img_folder, **kwargs):
    # possible to pass file='path_to_file' as argument to store result as json file

    files = []
    for (dirpath, dirnames, filenames) in walk(img_folder):
        files.extend(filenames)
        break

    results = {}

    for file in files:
        img_path = 'test_images/' + file

        results[file] = analyze_image(img_path)
    if 'file' in kwargs.keys():
        with open(result_file, 'w') as file:
            json.dump(results, file)

    return results


if __name__ == '__main__':
    folder = sys.argv[1]
    result_file = sys.arg[2]
    result = analyze_images(folder, result_file)
    pprint(result)