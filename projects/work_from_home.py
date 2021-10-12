import pyautogui, time
pyautogui.FAILSAFE = False
while True:
	i = 0
	for i in range(5, 101):
		pyautogui.moveTo(25, i*5)

	for i in range(5, 101):
		pyautogui.moveTo(i*5, 500)

	for i in range(100, 4, -1):
		pyautogui.moveTo(500, i*5)

	for i in range(100, 4, -1):
		pyautogui.moveTo(i*5, 25)

	# for i in range(3):
	# 	pyautogui.press('shift')
	time.sleep(5)
