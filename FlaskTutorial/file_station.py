import requests
import argparse
import json
import os
import cv2
import numpy as np
import xlrd
import xlwt
from xlutils.copy import copy
from tools import pdfExtraction, excelExtraction
from io import BufferedReader, BytesIO
import time

# Initialize the PyTorch REST API endpoint URL.
FILE_STATION_UPLOAD_URL = 'http://file.sit.elimen.com.cn:8899/edfs/file/upload'
FILE_STATION_DOWNLOAD_URL = 'http://file.sit.elimen.com.cn:8899/edfs/file/download'
DEBUG_MODE = True

''' TO DO -- input image_bytes directly'''
def upload_file_imgcv(imgcv):
    timestamp = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))

    _, img_encode = cv2.imencode('.jpg', imgcv)
    img_bytes = img_encode.tobytes()
    img_bytesIO = BytesIO(img_bytes)  # 转化为_io.BytesIO类型
    img_bytesIO.name = timestamp + '.jpg'  # 名称赋值, 相同名称会产生相同fileId！！
    img_ioBufferReader = BufferedReader(img_bytesIO)  # 转化为_io.BufferReader类型

    ## Debug
    if DEBUG_MODE:
        img_tmp = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
        cv2.imwrite("./img_tmp.jpeg", img_tmp)

    files = {'MultipartFile': img_ioBufferReader}
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

def upload_file_imgpath(image_path):
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


def download_file(fileId, fileType):
    '''
    Input:
    fileId -- Elimen File Station parameters
    fileType -- ["IMAGE", "EXCEL", "PDF"]
    Output:
    img_dataset -- list of images
    '''
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
            return [img], 1
        else:
            print("Fail to load img.")
    elif fileType == "PDF":
        img_dataset, pages = pdfExtraction.pdf2img(r.content, zoom_x=3, zoom_y=3)
        return img_dataset, pages
    elif fileType == "EXCEL":
        ## check save dir
        excel_save_dir_tmp = "./tmp"
        if not os.path.exists(excel_save_dir_tmp):
            os.mkdir(excel_save_dir_tmp)

        excel_bytes = xlrd.open_workbook(file_contents=r.content, formatting_info=True)
        workbook = copy(excel_bytes)
        excel_save_path_tmp = os.path.join(excel_save_dir_tmp, "excel_xlwt.xls")
        workbook.save(excel_save_path_tmp)

        img_dataset, sheets = excelExtraction.excel2imgs(excel_save_path_tmp)
        return img_dataset, sheets


if __name__ == '__main__':
    ''''''
    # parser = argparse.ArgumentParser(description='Classification demo')
    # parser.add_argument('--file', default='./insexp.jpeg', type=str, help='test image file')
    # args = parser.parse_args()
    # fileId = upload_file(args.file)
    ''''''
    # fileId = "211a1232f7d24da7a4f2d07ece52d7d5"  # PDF
    # fileId = "0062316af652494d9ad24f5d271f1f1b"  # EXCEL
    # img_datasets, nums = download_file(fileId, "PDF")
    # print(type(img_datasets))
    # print(nums)

    ''''''
    #0: 7c39e83e8803430a87de6938098746db
    #1: 7c39e83e8803430a87de6938098746db
    #2: 7c39e83e8803430a87de6938098746db

    imgpath = "../test_images/test_22.jpg"
    img = cv2.imread(imgpath)

    fileId = upload_file_imgcv(img)
    print(fileId)