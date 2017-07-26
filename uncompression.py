# -*- coding: UTF-8 -*-
import os
import threading
import config
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def unrar(path, filename):
	new_path = os.path.join(path, filename.replace('.rar', ''))
	if not os.path.exists(new_path):
		os.popen('mkdir \'' + new_path + '\'')
	os.popen('unrar x -o+ \'' + os.path.join(path, filename) + '\' \'' + new_path + '\'')


def unzip(path, filename):
	new_path = os.path.join(path, filename.replace('.zip', ''))
	if not os.path.exists(new_path):
		os.popen('mkdir \'' + new_path + '\'')
	os.popen('unzip -o \'' + os.path.join(path, filename) + '\' -d \'' + new_path + '\'')


def untar_gz(path, filename):
	new_path = os.path.join(path, filename.replace('.tar.gz', ''))
	if not os.path.exists(new_path):
		os.popen('mkdir \'' + new_path + '\'')
	os.popen('tar -xzf \'' + os.path.join(path, filename) + '\' -C \'' + new_path + '\'')
	pass


def unpack(path, filename):
	if filename.find('.rar') >= 0:
		t = threading.Thread(target=unrar, args=(path, filename,))
	elif filename.find('.zip') >= 0:
		t = threading.Thread(target=unzip, args=(path, filename,))
	elif filename.find('.tar.gz') >= 0:
		t = threading.Thread(target=untar_gz, args=(path, filename,))
	t.run()
