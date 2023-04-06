from PIL.Image import open as imopen
from sys import stdout
from datetime import timedelta
from cv2 import VideoCapture, imencode, resize
from io import BytesIO
file = open("roseila-badapple.srt", "w")
START_TIME = 4000 #Start to show see this video in captions (milliseconds)
def I2T(File):
	im = imopen(File)
	(w, h) = im.size
	mim = im.convert("1")
	data = list(mim.getdata())
	counter = 0
	field = True
	for pixel in data:
		if field:
			if pixel > 127: file.write("1")
			else: file.write("0")
		counter = counter + 1
		if counter >= w:
			counter = 0
			if field: file.write("\n")
			field = not field
vidcap = VideoCapture('./video.mp4') #<-- Did your match?
success, image = vidcap.read()
index = 0
while success:
	index += 1
	file.write(str(index) + "\n" + (str(timedelta(milliseconds = (index * 100) + START_TIME))[:11] + " --> " + str(timedelta(milliseconds = ((index + 1) * 100) + START_TIME))[:11]).replace('.', ',') + "\n")
	I2T(BytesIO(imencode(".jpg", resize(image, (24, 32), interpolation = 3))[1]))
	file.write("\n")
	vidcap.read()
	vidcap.read()
	success, image = vidcap.read()

file.close()