import sys
import os
import utils
import time
import random

import get_photos

from PyQt4 import QtGui, QtCore


class SlideShowPics(QtGui.QMainWindow):

	""" SlideShowPics class defines the methods for UI and
		working logic
	"""
	def __init__(self, root_path, parent=None):
		super(SlideShowPics, self).__init__(parent)
		# self._path = path

		self.move_timer_time = 150
		self.next_timer = 10000
		self.move_x = True
		self.move_y = True

		self.photos = get_photos.get_photos(root_path)

		self._pause = False
		self._count = 0
		self.animFlag = True

		self.updateTimer = QtCore.QTimer()
		self.connect(self.updateTimer, QtCore.SIGNAL("timeout()"), self.nextImage)
		self.moveTimer = QtCore.QTimer()
		self.connect(self.moveTimer, QtCore.SIGNAL("timeout()"), self.move_label)
		self.prepairWindow()
		self.nextImage()

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

		image_path = self.photos.get_next()
		print 'image_path: %s' % image_path
		self.showImageByPath(image_path)

		if self.animFlag:
			self._count += 1
		else:
			self._count -= 1

		self.moveTimer.start(self.move_timer_time)

	def move_label(self):
			x = 1 if self.move_x else -1
			y = 1 if self.move_y else -1

			self.label.move(self.label.x() + x, self.label.y() + y)

			QtGui.QApplication.processEvents()

	def showImageByPath(self, path):
		if path:
			self.image = QtGui.QImage(path)
			self.pp_orignal = QtGui.QPixmap.fromImage(self.image)
			w_p_10 = self.label.size().width() + (self.label.size().width() * .1)
			h_p_10 = self.label.size().height() + (self.label.size().height() * .1)
			print w_p_10, h_p_10

			self.pp = self.pp_orignal.scaled(w_p_10, h_p_10, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

			self.label.setPixmap(self.pp)

			QtGui.QApplication.processEvents()

			self.move_x = bool(random.getrandbits(1))
			self.move_y = bool(random.getrandbits(1))

			print 'self.label.size(): %s' % self.label.size()

	def playPause(self):
		if not self._pause:
			self._pause = True
			self.updateTimer.start(self.next_timer)
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


def main(paths):
	app = QtGui.QApplication(sys.argv)
	window = SlideShowPics(paths)
	window.show()
	window.raise_()
	app.exec_()


if __name__ == '__main__':
	#curntPaths = os.getcwd()
	#if len(sys.argv) > 1:
		#curntPaths = sys.argv[1:]
	root_path = '/media/blake/BLAKE KEYS/Photos'
	main(root_path)
