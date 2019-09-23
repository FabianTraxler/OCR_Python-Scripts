import requests
import sys
import os
import xml.dom.minidom
import Abbyy as abbyy
import time
import boto3
import re
import json
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/ftraxler/OneDrive - Capgemini/Projekte/OCR Research/Scripts/Credentials/Vision-OCR-734bc8b231c8.json"

def amazon_process_image(path):

    # Read document content
    with open(path, 'rb') as document:
        imageBytes = bytearray(document.read())

    # Amazon Textract client
    textract = boto3.client('textract')

    # Call Amazon Textract
    response = textract.detect_document_text(Document={'Bytes': imageBytes})
    text = ''

    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            text += item["Text"] + '\n'

    return text



def microsoft_process_image(path):
    # Replace <Subscription Key> with your valid subscription key.
    subscription_key = "9c43ff6d3a5a49cdb25cb451bc761b63"
    assert subscription_key

    vision_base_url = "https://ocr-testing.cognitiveservices.azure.com//vision/v2.0/"

    analyze_url = vision_base_url + "ocr"

    # Set image_path to the local path of an image that you want to analyze.

    # Read the image into a byte array
    with open(path, 'rb') as image_file:
        image_data = image_file.read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    params = {}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. 
    # The most relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    # Retrieve Text out of Microsoft response
    text = ''
    for region in analysis['regions']:
        for line in region['lines']:
            for word in line['words']:
                text += ' ' + word['text']
    return text


def google_process_image(path):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    text = texts[0].description
    return text


def abbyy_process_image(path):
    applicationId = 'OCR_API_TESTING'
    password = '1TPypgcgdJiXw8WHF5/j5lfG'
    url_params = {
        "language": 'English',
        "exportFormat": 'XML'
    }
    request_url = "http://cloud-eu.ocrsdk.com/processImage"

    with open(path, 'rb') as image_file:
        image_data = image_file.read()

    response = requests.post(request_url, data=image_data, params=url_params,
                             auth=(applicationId, password), proxies={})

    # Any response other than HTTP 200 means error - in this case exception will be thrown
    response.raise_for_status()

    # parse response xml and extract task ID
    task = abbyy.decode_response(response.text)
    while task.is_active():
        time.sleep(5)
        task = abbyy.get_task_status(task, applicationId, password)

    if task.Status == "Completed":
        if task.DownloadUrl is not None:
            result = abbyy.download_result(task)
    text = ''
    xml_doc = xml.dom.minidom.parseString(result.text)
    for Char in xml_doc.getElementsByTagName('charParams'):
        text += str(Char.firstChild.nodeValue)
    return text


if __name__ == '__main__':
    api = sys.argv[1]
    img_path = sys.argv[2]
    if api == 'Google':
        print(google_process_image(img_path))
    elif api == 'Microsoft':
        print(microsoft_process_image(img_path))
    elif api == 'Abby':
        print(abbyy_process_image(img_path))
    elif api == 'Amazon':
        print(amazon_process_image(img_path))
