import requests
import argparse
import json
import cv2
import numpy as np

# Initialize the PyTorch REST API endpoint URL.
FILE_STATION_UPLOAD_URL = 'http://file.sit.elimen.com.cn:8899/edfs/file/upload'
FILE_STATION_DOWNLOAD_URL = 'http://file.sit.elimen.com.cn:8899/edfs/file/download'

def upload_file(image_path):
    # Initialize image path
    image = open(image_path, 'rb') ## 与 open(image_path, 'rb').read() 区别 ？？

    ## Debug
    img_tmp = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
    cv2.imwrite("./img_tmp.jpeg", img_tmp)

    files = {'MultipartFile': image}
    data = {'fileType': "image", 'filePath': "fin", 'uploadLocation': "OSS", 'expireTime': 60}

    # Submit the request.
    r = requests.post(FILE_STATION_UPLOAD_URL, data=data, files=files).json()
    print(r)

    # Ensure the request was successful.
    if r['content'] :
        # Loop over the predictions and display them.
        fileId = json.loads(r['content'])['fileId']
        print('{}: {}'.format("fileId", fileId))
        return fileId

    # Otherwise, the request failed.
    else:
        print(r['msg'])
        return -1

def download_file(fileId):
    # Initialize image path
    data = {'fileId': fileId}

    # Submit the request.
    r = requests.get(FILE_STATION_DOWNLOAD_URL, params=data)
    img = cv2.imdecode(np.frombuffer(r.content, np.uint8), cv2.IMREAD_COLOR)
    if img is not None:
        print("Img downloaded from file station.")

        ## Debug:
        cv2.imwrite("./filedown.jpeg", img)

        return img
    else:
        print("Fail to load img.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Classification demo')
    parser.add_argument('--file', default='./insexp.jpeg', type=str, help='test image file')
    args = parser.parse_args()
    fileId = upload_file(args.file)
    download_file(fileId)
