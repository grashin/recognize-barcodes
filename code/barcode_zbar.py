from pyzbar import pyzbar
import imutils
from imutils.video import VideoStream
import cv2
from cv2 import aruco
import yaml
import numpy as np

vs = cv2.VideoCapture('/Users/grashin/video_detection/barcodes_2.mp4')
csv = open('/Users/grashin/video_detection/examples/barcodes.csv', "w")
found = set()

length = 5.3
with open("/Users/grashin/video_detection/calibration_3.yaml") as f:
	loadeddict = yaml.load(f)
mtx = loadeddict.get('camera_matrix')
dist = loadeddict.get('dist_coeff')
mtx = np.array(mtx)
dist = np.array(dist)	
aruco_dict = aruco.getPredefinedDictionary( aruco.DICT_6X6_250 )

arucoParams = aruco.DetectorParameters_create()
writer = None

while True:
	(grabbed, image) = vs.read()
	if not grabbed:
		break
	image = imutils.resize(image, width=400)
	barcodes = pyzbar.decode(image)
	for barcode in barcodes:
	    (x, y, w, h) = barcode.rect
	    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

	    barcodeData = barcode.data.decode('utf-8')
	    barcodeType = barcode.type
	    text = "{} ( {} )".format(barcodeData, barcodeType)
	    cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 2)
	    print(text)
	    if barcodeData not in found:
	    	csv.write("{}\n".format(barcodeData))
	    	csv.flush()
	    	found.add(barcodeData)


	img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


	corners, ids, rejectedImgPoints = aruco.detectMarkers(img_gray, aruco_dict, parameters=arucoParams)
	imaxis = image.copy()

	# print(ids)
	# print(corners)
	# print(mtx)
	# print(dist)
	# print(board)
	# _, rvec, tvec = aruco.estimatePoseBoard(corners, ids, board, mtx, dist, None, None)
	if ids is not None:
		rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, length, mtx, dist, None, None)
		imaxis = aruco.drawDetectedMarkers(imaxis, corners, ids)
		# for i in range(len(tvec)):
			# imaxis = aruco.drawAxis(imaxis, mtx, dist, rvec[i], tvec[i], 10) 

		
	if writer is None:
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter("/Users/grashin/video_detection/examples/barcodes_3.avi", fourcc, 15,
		(imaxis.shape[1], imaxis.shape[0]), True)
	writer.write(imaxis)	
cv2.destroyAllWindows()
writer.release()
vs.release()
csv.close()