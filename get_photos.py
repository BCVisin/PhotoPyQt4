import os
import time
import random

import threading
import Queue

from PIL import ImageTk
from PIL import Image

PHOTO_FILE_EXTENSIONS = ['.JPG', '.JPEG', '.GIF']

class get_photos(object):

	def __init__(self, root_path):

		self.images = []
		self.preload_num = 5
		self.image_queue = Queue.Queue()
		self.root_path = root_path
		self.image_index = -1

		self.preload()
		time.sleep(1)
		self.thread_load_images()

	def thread_load_images(self):

		while True:
			try:
				image_location = self.image_queue.get_nowait()
				self.images.append(image_location)
			except Queue.Empty:
				break

	def get_next_index(self):

		if len(self.images) < self.image_index + self.preload_num:
			self.preload()

		self.image_index += 1

		return self.image_index

	def get_previous_index(self):
		if self.image_index <= 0:
			self.image_index = len(self.images) - 1
		else:
			self.image_index -= 1

		return self.image_index

	def get_photo(self, index):
		#check the queue for other images that we may have returned
		self.thread_load_images()

		return self.images[index]

	def get_next(self):

		return self.get_photo(self.get_next_index())

	def get_previous(self):

		return self.get_photo(self.get_previous_index())

	def preload(self):
		for i in range(0, self.preload_num):
			load_image(return_queue=self.image_queue, root_path=self.root_path, seen_images=self.images).start()


class load_image(threading.Thread):

	def __init__(self, return_queue, root_path, seen_images):

		self.root_path = root_path
		self.return_queue = return_queue
		self.seen_images = seen_images
		threading.Thread.__init__(self)

	def run(self):

		self.return_queue.put(self.get_rand_photo())

	def get_rand_photo(self):

		final_files = []

		for root, _, files in os.walk(self.root_path, topdown=True):
			for single_file in files:
				file_name, file_extension = os.path.splitext('%s/%s' % (root, single_file,))
				if file_extension.upper() in PHOTO_FILE_EXTENSIONS:
					image_location = '%s%s' % (file_name, file_extension,)
					if image_location not in self.seen_images:
						final_files.append(image_location)
		return random.choice(final_files)




