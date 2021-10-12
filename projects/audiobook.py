import pyttsx3, PyPDF2, os
from tkinter import filedialog
file = filedialog.askopenfilename(title='Choose', filetypes=(('PDF Files', '*.pdf'),))
book = open(file, 'rb')
pdfreader = PyPDF2.PdfFileReader(book)
pages = pdfreader.numPages
print('Total Pages = ' + str(pages))
f = int(input('From Page: '))
t = int(input('To Page: '))
speaker = pyttsx3.init()
os.startfile(file)
for i in range(f, t+1):
	page = pdfreader.getPage(i)
	text = page.extractText()
	speaker.say(text)
	speaker.runAndWait()

# speaker.say('Hey, I can talk')
