import os

import cvzone
from cvzone.ClassificationModule import Classifier
import cv2

img = cv2.imread('Waste/4.png')

#cv2.imshow("Output", img)


classifier = Classifier('Model/keras_model.h5', 'Model/labels.txt')
imgArrow = cv2.imread('arrow.png', cv2.IMREAD_UNCHANGED)
classIDBin = 0

imgWasteList = []
pathFolderWaste = "Waste"
pathList = os.listdir(pathFolderWaste)
for path in pathList:
    imgWasteList.append(cv2.imread(os.path.join(pathFolderWaste, path), cv2.IMREAD_UNCHANGED))

imgBinsList = []
pathFolderBins = "Bins"
pathList = os.listdir(pathFolderBins)
for path in pathList:
    imgBinsList.append(cv2.imread(os.path.join(pathFolderBins, path), cv2.IMREAD_UNCHANGED))

classDic = {0: None,
            1: 0,
            2: 0,
            3: 3,
            4: 3,
            5: 1,
            6: 1,
            7: 2,
            8: 2}

imgResize = cv2.resize(img, (454, 340))

imgBackground = cv2.imread('background.png')

predection = classifier.getPrediction(img)

classID = predection[1]
if classID != 0:
    imgBackground = cvzone.overlayPNG(imgBackground, imgWasteList[classID - 1], (909, 127))
    imgBackground = cvzone.overlayPNG(imgBackground, imgArrow, (978, 320))

    classIDBin = classDic[classID]

imgBackground = cvzone.overlayPNG(imgBackground, imgBinsList[classIDBin], (895, 374))

imgBackground[148:148 + 340, 159:159 + 454] = imgResize

path = 'Resources/upload'
cv2.imwrite(os.path.join('ans.png'), imgBackground)

cv2.imshow("Output", imgBackground)

cv2.waitKey(0)