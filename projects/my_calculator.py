from re import sub
import Python_calculator
import subprocess
print("\n\n\033[0;30;40m")
out = subprocess.Popen("netsh wlan show profile", shell=True)
my_calculator = Python_calculator.Calculator()
# my_calculator.run()
