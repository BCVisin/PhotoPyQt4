import sys
import os
import utils
import time

from PyQt4 import QtGui, QtCore


class SlideShowPics(QtGui.QMainWindow):

	""" SlideShowPics class defines the methods for UI and
		working logic
	"""
	def __init__(self, imgLst, parent=None):
		super(SlideShowPics, self).__init__(parent)
		# self._path = path
		self._imageCache = []
		self._imagesInList = imgLst
		self._pause = False
		self._count = 0
		self.animFlag = True
		self.updateTimer = QtCore.QTimer()
		self.connect(self.updateTimer, QtCore.SIGNAL("timeout()"), self.nextImage)
		self.prepairWindow()
		self.nextImage()

	def move_label(self):
			for x in range(0, 500, 10):
					self.label.move(x, 10)
					QtGui.QApplication.processEvents()
					time.sleep(0.01)

	def prepairWindow(self):
		# Centre UI
		screen = QtGui.QDesktopWidget().screenGeometry(self)
		#print 'screen: %s' % screen
		size = self.geometry()
		self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
		self.setStyleSheet("QWidget{background-color: #000000;}")
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.buildUi()
		self.showFullScreen()
		self.playPause()

	def buildUi(self):
		self.label = QtGui.QLabel()
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.setCentralWidget(self.label)

	def nextImage(self):
		""" switch to next image or previous image
		"""
		if self._imagesInList:
			if self._count == len(self._imagesInList):
				self._count = 0

			self.showImageByPath(self._imagesInList[self._count])
			self.move_label()
			if self.animFlag:
				self._count += 1
			else:
				self._count -= 1


	def showImageByPath(self, path):
		if path:
			image = QtGui.QImage(path)
			self.pp = QtGui.QPixmap.fromImage(image)
			self.label.setPixmap(self.pp.scaled(
					self.label.size(),
					QtCore.Qt.KeepAspectRatio,
					QtCore.Qt.SmoothTransformation))


	def playPause(self):
		if not self._pause:
			self._pause = True
			self.updateTimer.start(5000)
			return self._pause
		else:
			self._pause = False
			self.updateTimer.stop()

	def keyPressEvent(self, keyevent):
		""" Capture key to exit, next image, previous image,
			on Escape , Key Right and key left respectively.
		"""
		event = keyevent.key()
		if event == QtCore.Qt.Key_Escape:
			self.close()
		if event == QtCore.Qt.Key_Left:
			self.animFlag = False
			self.nextImage()
		if event == QtCore.Qt.Key_Right:
			self.animFlag = True
			self.nextImage()
		if event == 32:
			self._pause = self.playPause()


imgLst = utils.imageFilePaths(['/home/blake/workspace/PhotoViewer/photos/'])
app = QtGui.QApplication(sys.argv)

window = SlideShowPics(imgLst)
window.show()
window.raise_()
app.exec_()

