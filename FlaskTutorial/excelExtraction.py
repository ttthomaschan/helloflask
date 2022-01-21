import jpype
jpype.startJVM()
from asposecells.api import Workbook, PdfSaveOptions, ImageOrPrintOptions, SheetRender

import cv2
import numpy as np

DEBUG_MODE = False

def excel2imgs(excel_path):

    workbook = Workbook(excel_path)

    ''' Excel to PDF '''
    # pdfOptions = PdfSaveOptions()
    # pdfOptions.setOnePagePerSheet(True)
    # workbook.save("../test_images/example.pdf", pdfOptions)

    imgOptions = ImageOrPrintOptions()
    imgOptions.setHorizontalResolution(300)
    imgOptions.setVerticalResolution(300)
    imgOptions.setCellAutoFit(True)
    imgOptions.setOnePagePerSheet(True)

    img_datasets = []
    sheet_Count = workbook.getWorksheets().getCount()
    for i in range(sheet_Count):

        sheet = workbook.getWorksheets().get(i)
        sr = SheetRender(sheet, imgOptions)

        imgbytes_content = sr.toImageBytes(0)
        img = cv2.imdecode(np.frombuffer(imgbytes_content, np.uint8), cv2.IMREAD_COLOR)
        img_datasets.append(img)

        if DEBUG_MODE:
            cv2.imwrite("../test_results/Excel2Image/bytes2cvimg_" + str(i) + ".png", img)
            # sr.toImage(i, "../test_results/Excel2Image/excel2img_" + str(i) +".png")

    # jpype.shutdownJVM()
    return img_datasets, sheet_Count


###############################
if __name__ == "__main__":
    excel_path = "/home/elimen/Data/helloflask/FlaskTutorial/rewrite.xls"
    img_datasets = excel2imgs(excel_path)
    print(" Number of images: {}".format(len(img_datasets)))
    print(" Type of image: {}".format(type(img_datasets[0])))
