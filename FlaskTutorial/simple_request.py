import requests
import argparse
import cv2

# Initialize the PyTorch REST API endpoint URL.
PyTorch_REST_API_URL = 'http://127.0.0.1:5000'

def predict_result(image_path):
    # Initialize image path
    image = open(image_path, 'rb').read()
    payload = {'image': image, 'image_url': "/home/elimen/Data/helloflask/FlaskTutorial/dog.JPEG"}

    # Submit the request.
    r = requests.post(PyTorch_REST_API_URL, files=payload).json()

    # Ensure the request was successful.
    if r['success']:
        # Loop over the predictions and display them.
        result = r['predictions']
        url = r['url']
        print('{}: {}, image_url:{}'.format("pred_label", result, url))
        res_image = cv2.imread(url)
        cv2.imwrite("/home/elimen/Data/helloflask/FlaskTutorial/res_image.jpg", res_image)
        print("Image loaded.")

    # Otherwise, the request failed.
    else:
        print('Request failed')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Classification demo')
    parser.add_argument('--file', default='./dog.JPEG', type=str, help='test image file')
    args = parser.parse_args()
    predict_result(args.file)