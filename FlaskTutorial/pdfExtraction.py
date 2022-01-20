import os
import fitz
import numpy as np
import cv2
import time

def pdf2img(pdfBytes=None, pdfPath=None, zoom_x=2, zoom_y=2, logMode=False):
    
    if pdfBytes is None and pdfPath is not None:
        pdf = fitz.open(pdfPath)
    elif pdfBytes is not None:
        pdf = fitz.Document(stream=pdfBytes, filetype='pdf')
    else:
        '''返回错误码'''
    
    rotation_angle = 0
    pages = pdf.pageCount
    img_dataset = []
    if pages > 3:
        return img_dataset, pages

    for page in range(1,pages+1):
        pg = pdf[page - 1]
        trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotation_angle)
        pm = pg.getPixmap(matrix=trans, alpha=False)
        getpngdata = pm.getImageData(output="png")
        ## decode to np.uint8
        img_array = np.frombuffer(getpngdata, dtype=np.uint8)
        img_cv = cv2.imdecode(img_array, cv2.IMREAD_ANYCOLOR)
        img_dataset.append(img_cv)
        
        '''Logger'''
        if logMode and pdfPath:
            pm.writePNG(pdfPath.split('.')[0]+str(page)+".png")

    pdf.close()
    return img_dataset, pages


if __name__ == "__main__":
    pdfPath = '/home/elimen/Data/Project/jlg_doctab_infer_dev/test_images/errortest_201912.pdf'
    print("start")
    start = time.time()
    img, pages = pdf2img(pdfPath=pdfPath, zoom_x=3, zoom_y=3)
    print(time.time()- start)
    print("end")