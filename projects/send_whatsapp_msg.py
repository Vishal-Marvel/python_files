import pywhatkit, time
from datetime import datetime

while True:
	now_h, now_m = int(datetime.now().strftime('%H')), int(datetime.now().strftime('%M'))
	check = [
	now_m == 30,
	now_m == 40,
	now_m == 50]
	if now_h == 15 and any(check):
		pywhatkit.sendwhatmsg('+919551264344', 'Submit answer papers', now_h, now_m+1)
		time.sleep(10)
	else:
		time.sleep(10)		
