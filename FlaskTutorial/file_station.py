import requests
import argparse
import json
import cv2
import numpy as np
import xlrd
import xlwt
from xlutils.copy import copy
import pdfExtraction

# Initialize the PyTorch REST API endpoint URL.
FILE_STATION_UPLOAD_URL = 'http://file.sit.elimen.com.cn:8899/edfs/file/upload'
FILE_STATION_DOWNLOAD_URL = 'http://file.sit.elimen.com.cn:8899/edfs/file/download'
DEBUG_MODE = True

''' TO DO -- input image_bytes directly'''
def upload_file(image_path):
    # Initialize image path
    image = open(image_path, 'rb') ## 与 open(image_path, 'rb').read() 区别 ？？

    ## Debug
    if DEBUG_MODE:
        img_tmp = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
        cv2.imwrite("./img_tmp.jpeg", img_tmp)

    files = {'MultipartFile': image}
    data = {'fileType': "image", 'filePath': "fin", 'uploadLocation': "OSS", 'expireTime': 60}

    # Submit the request.
    r = requests.post(FILE_STATION_UPLOAD_URL, data=data, files=files).json()

    # Ensure the request was successful.
    if r['content']:
        # Loop over the predictions and display them.
        fileId = json.loads(r['content'])['fileId']
        return fileId

    # Otherwise, the request failed.
    else:
        return "Upload failed -- {}".format(r['msg'])

'''Version _1: return '''
def download_file(fileId, fileType):
    # Initialize image path
    data = {'fileId': fileId}

    # Submit the request.
    r = requests.get(FILE_STATION_DOWNLOAD_URL, params=data)
    data_bytes = r.content

    if fileType == "IMAGE":
        img = cv2.imdecode(np.frombuffer(data_bytes, np.uint8), cv2.IMREAD_COLOR)
        if img is not None:
            if DEBUG_MODE:
                print("Img downloaded from file station.")
                cv2.imwrite("./filedown.jpeg", img)
            return [img]
        else:
            print("Fail to load img.")
    elif fileType == "PDF":
        img_dataset, pages = pdfExtraction.pdf2img(r.content, zoom_x=3, zoom_y=3)
        return img_dataset
    elif fileType == "EXCEL":
        excel_bytes = xlrd.open_workbook(file_contents=r.content, formatting_info=True)
        workbook = copy(excel_bytes)
        workbook.save("rewrite.xls")

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Classification demo')
    # parser.add_argument('--file', default='./insexp.jpeg', type=str, help='test image file')
    # args = parser.parse_args()
    # fileId = upload_file(args.file)
    fileId = "211a1232f7d24da7a4f2d07ece52d7d5"
    download_file(fileId, "PDF")
