import os, shutil
from tkinter import filedialog

try:
	path = filedialog.askdirectory(title='Choose Folder')
	for (pa, dirs, files) in os.walk(path):
		for file in files:
			try:
				extension = str(file.split('.')[-1])
				new_path = path + '/' + extension
				if os.path.exists(new_path):
					if file.endswith(extension):
						try:
							shutil.move(path + '/' + file, new_path)
						except shutil.Error as e:
							if 'already exists' in str(e):
								print(e)
								pass
							else:
								print(e)
				
				else:
					os.mkdir(new_path)
					try:
						shutil.move(path + '/' + file, new_path)
					except shutil.Error as e:
						if 'already exists' in str(e):
							pass
						else:
							print(e)
			except IndexError:
				new_path = path + '/others'
				if os.path.exists(new_path):
					if file.endswith(extension):
						try:
							shutil.move(path + '/' + file, new_path)
						except shutil.Error as e:
							if 'already exists' in str(e):
								print(e)
								pass
							else:
								print(e)
				
				else:
					os.mkdir(new_path)
					try:
						shutil.move(path + '/' + file, new_path)
					except shutil.Error as e:
						if 'already exists' in str(e):
							pass
						else:
							print(e)
			
except Exception as e:
	print(e)
	
else:
	print('Task Done')
