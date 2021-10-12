import math
from os import system
import datetime


class Calculate:

    def title(self):
        system('cls')
        now = datetime.datetime.now()
        print("\n\t\033[1;34;40m======================================================================\033[0;30;40m")
        print("\t\t\033[1;37;43m W  E  L  C  O  M  E     T  O     P  Y  T  H  O  N \033[0;30;40m #")
        print(
            "\t\033[1;34;40m==\033[1;32;40m====\033[1;34;40m================\033[1;32;40m===\033[1;34;40m==========\033[1;32;40m==\033[1;34;40m=========================\033[1;32;40m=====\033[1;34;40m===\033[1;32;40m")
        print("\t /  __)  ___    __   / __) _     _|  |     ___  _______ ____ |  _  \ ")
        print("\t|  |    /\  \  |  | | |   | |   | |  |    /\  \|_    __/ __ \| (_)  | ")
        print("\t|  |   /__\  \ |  | | |_  | |   | |  |   /__\  \ |  | | /  \ |     /")
        print("\t|  |__/    \  \|  |__\___)| |___| |  |__/_   \  \|  | | \__/ |  |\ \ ")
        print("\t \____)     \__\________|  \_____/ \______|   \__|__|  \____/|__| \_\ \033[1;34;40m")
        print("\t======================================================================\033[0;30;40m#")
        print(
            "\n    \033[1;37;41m[***]THIS IS A BASIC PYTHON CALCULATOR \033[1;37;46mBY VISHAL\033[1;37;41m THANK YOU FOR USING THIS[***]\033[0;30;40m #")
        print("\n\033[0;30;47mCurrent date and time :\033[1;37;40m", now.strftime("%d-%m-%y ; %H:%M:%S"), "")
        print("\n\033[1;32;40mOerations available:")
        print(
            "\t\033[1;37;40m>> To do multiple operations like \033[1;37;45madd.,sub.,mul.,div., in an expression\033[1;37;40m,enter ... '1'")
        print(
            "\t>> To find \033[1;37;45mfactorial\033[1;37;40m of set of numbers, enter ................................... '2'")
        print(
            "\t>> To find \033[1;37;45mpercentage\033[1;37;40m of set of numbers, enter .................................. '3'")
        print(
            "\t>> To find \033[1;37;45m'powerof'\033[1;37;40m of a number, enter ......................................... '4'")
        print(
            "\t>> To find the \033[1;37;45msquare root\033[1;37;40m of set of numbers, enter ............................. '5'")
        print(
            "\t>> To find the \033[1;37;45mcube root\033[1;37;40m of set of numbers, enter ............................... '6'")
        print(
            "\t>> To find the given year is \033[1;37;45mleap year\033[1;37;40m or not, enter ............................ '7'")
        print(
            "\t>> To find the \033[1;37;45mgcd\033[1;37;40m of given numbers, enter ...................................... '8'")
        print(
            "\t>> To find the \033[1;37;45mlcm\033[1;37;40m of given numbers, enter ...................................... '9'")
        print(
            "\t>> To check whether the given numbers are \033[1;37;45mprime\033[1;37;40m or not, enter ................... '10'")
        print(
            "\t>> To find the \033[1;37;45mfactors\033[1;37;40m of a set of number, enter ................................ '11'")
        print(
            "\t>> To find the \033[1;37;45mlogarithm\033[1;37;40m of a number, enter ..................................... '12'")
        print(
            "\t>> To find the \033[1;37;45msine\033[1;37;40m of a number, enter .......................................... '13'")
        print(
            "\t>> To find the \033[1;37;45mcosine\033[1;37;40m of a number, enter ........................................ '14'")
        print(
            "\t>> To find the \033[1;37;45mtangent\033[1;37;40m of a number, enter ....................................... '15'")
        print(
            "\t>> To print \033[1;37;45mfibonacci series\033[1;37;40m, enter ............................................. '16'")
        print(
            "\t>> To find the given number is \033[1;37;45mpalindrome\033[1;37;40m or not , enter ........................ '17'")
        print(
            "\t>> To find \033[1;37;45myour age\033[1;37;40m, enter ...................................................... '18'")
        print(
            "\t>> To \033[0;37;41mexit\033[1;37;40m, enter ............................................................... '19'")

    def eval_str(self):
        i = r = 0
        expression = ""
        while True:
            try:
                while i == 0:
                    expression = input("\n\033[1;32;40m>>> Enter an expression for calculation ==> ")
                    r = eval(expression)
                    while True:
                        try:
                            print(
                                "\033[1;37;41m\nIf you want to retain the values press, \033[1;37;40m '1' \033[1;37;41mElse if you want to change the values press, \033[1;37;40m '0' \n\033[1;37;40m==>",
                                end='')
                            i = int(input())
                            break
                        except ValueError:
                            print("\n\033[0;37;41m\a[-] ENTER A VALUE\033[0;30;40m #")
                # system('cls')
                # self.title()
                print("\n\t\033[0;30;47m[***]RESULT[***]\033[0;30;40m#")
                print("\n\033[1;37;44m>>> ENTERED EXPRESSION=\033[1;37;40m", expression)
                print("\n\033[0;30;46m>>> RESULT =\033[1;37;40m", r)

                break
            except ValueError:
                print("\n\033[0;37;41m\a[-] ENTER AN EXPRESSION\033[0;30;40m #")
            except SyntaxError:
                print("\n\033[0;37;41m\a[-] ENTER A VALID EXPRESSION\033[0;30;40m #")
            except NameError:
                print("\n\033[0;37;41m\a[-] ENTERED FUNCTION UNAVAILABLE\033[0;30;40m #")
            except ZeroDivisionError:
                print("\n\033[0;37;41m\a[-] DIVISION BY ZERO IS INVALID\033[0;30;40m #")
            except TypeError:
                print("\n\033[0;37;41m\a[-] INVALID BRACES POSITION\033[0;30;40m #")
        pass

    def log(self):
        i = base = j = log_value = 0
        while True:
            try:
                while j == 0:
                    i = float(input("\n\033[1;32;40m>>>Enter the value for calculating log ==> "))
                    base = input("\n\033[1;32;40m>>>Enter a base value ==>\033[1;32;40m ")
                    if base == 'e':
                        log_value = math.log(i)
                    else:
                        log_value = math.log(i, float(base))
                    while True:
                        try:
                            print(
                                "\033[1;37;41m\nIf you want to retain the values press, \033[1;37;40m '1' \033[1;37;41mElse if you want to change the values press, \033[1;37;40m '0' \n\033[1;37;40m==>",
                                end='')
                            j = int(input())
                            break
                        except ValueError:
                            print("\n\033[0;37;41m\a[-] ENTER A VALUE\033[0;30;40m #")
                # system('cls')
                # self.title()
                print("\n\t\033[0;30;47m[***]RESULT[***]\033[0;30;40m#")
                print("\n\033[0;30;46m>>>The log of", i, "with base of", base, "=\033[1;37;40m", log_value)
                break
            except ValueError:
                print("\n\033[0;37;41m\a[-] ENTER A VALID VALUE\033[0;30;40m #")
            except ZeroDivisionError:
                print("\n\033[0;37;41m\a[-] BASE VALUE SHOULD BE GREATER THAN ONE\033[0;;30;40m #")
        pass

    def power_of(self):
        expo = base = j = 0
        while True:
            try:
                while j == 0:
                    base = int(input("\n\033[1;32;40m>>>Enter a base value ==> "))
                    expo = int(input("\n\033[1;32;40m>>>Enter a exponent value ==>\033[1;32;40m "))
                    while True:
                        try:
                            print(
                                "\033[1;37;41m\nIf you want to retain the values press, \033[1;37;40m '1' \033[1;37;41mElse if you want to change the values press, \033[1;37;40m '0' \n\033[1;37;40m==>",
                                end='')
                            j = int(input())
                            break
                        except ValueError:
                            print("\n\033[0;37;41m\a[-] ENTER A VALUE\033[0;30;40m #")
                # system('cls')
                # self.title()
                print("\n\t\033[0;30;47m[***]RESULT[***]\033[0;30;40m#")
                print("\n\033[0;30;46m>>>The result of", base, "raised to the powerof", expo, "=\033[1;37;40m",
                      base ** expo)
                break
            except ValueError:
                print("\n\033[0;37;41m\a[-] ENTER A VALID VALUE\033[0;30;40m #")

    def fibo(self):
        while True:
            a, b, c = -1, 1, 0
            try:
                n = int(input("\n\033[1;32;40m>>>Enter the number of terms for fibonacci series ==> "))
                # system('cls')
                # self.title()
                print("\n\t\033[0;30;47m[***]RESULT[***]\033[0;30;40m#")
                print("\n")
                if n > 0:
                    print("\033[0;30;46m>>>FIBONACCI SERIES FOR %d TERMS\033[1;37;40m" % n, end=" = ")
                    for i in range(1, n + 1):
                        c = a + b
                        print(c, end=' ')
                        a, b = b, c
                    break
                else:
                    print("\033[0;37;41m[-] ENTER A POSITIVE VALUE\033[0,30,40m#")
            except ValueError:
                print("\033[0;37;41m[-] ENTER A VALUE\033[0;30;40m#")
        pass

    def calculate_age(self):
        print("\n\t\t\033[1;37;42m[+]ENTER YOUR DOB IN THE BELOW ORDER \033[0;30;40m #")
        j = 0
        n = datetime.date.today()
        today = datetime.date.today()
        while True:
            try:
                while j == 0:
                    print("")
                    n = datetime.date(int(input("\033[1;32;40m>>>ENTER YEAR 'YYYY'==> ")),
                                      int(input(">>>ENTER MONTH 'MM'==> ")), int(input(">>>ENTER DATE 'DD'==> ")))
                    if n.year >= today.year:
                        print("\n\033[1;37;41m\a[-] YEAR MUST BE LESS THAN THE CURRENT YEAR\033[0;30;40m#")
                    else:
                        while True:
                            try:
                                print(
                                    "\033[1;37;41m\nIf you want to retain the values press, \033[1;37;40m '1' \033[1;37;41mElse if you want to change the values press, \033[1;37;40m '0'\033[1;37;40m\n==>",
                                    end='')
                                j = int(input())
                                break
                            except ValueError:
                                print("\n\033[0;37;41m\a[-] ENTER A VALUE\033[0;30;40m #")
                # system('cls')
                # self.title()
                print("\n\t\033[0;30;47m[***]RESULT[***]\033[0;30;40m#")
                print("\n")
                print("\033[1;37;44m>>>DOB =\033[1;37;40m %d-%d-%d" % (n.day, n.month, n.year))
                print("", end='')
                age_year = today.year - n.year - ((today.month, today.day) < (n.month, n.day))
                if today.month in (2, 4, 6, 8, 9, 11, 1):
                    days = 31
                elif today.month == 3:
                    days = 28
                elif today.month == 3 and self.leap(today.year):
                    days = 29
                else:
                    days = 30
                if n.month in (1, 2, 4, 6, 8, 9, 11):
                    rem_days = 31
                elif n.month == 3:
                    rem_days = 28
                elif n.month == 3 and self.leap(today.year):
                    rem_days = 29
                else:
                    rem_days = 30
                if today.month == n.month and today.day == n.day:
                    print("\n\033[0;30;46m>>>Age =\033[1;37;40m", age_year, "years")
                    print("\n\t\033[1;37;44m[***] H A P P Y   B I R T H D A Y   T O   Y O U [***]\033[0;30;40m #")
                elif today.month > n.month and today.day > n.day:
                    age_month = today.month - n.month
                    age_day = today.day - n.day
                    rem_month = (n.month + 12) - today.month - 1
                    rem_day = (rem_days - today.day) + n.day
                    print("\n\033[0;30;46m>>>Age =\033[1;37;40m", age_year, "years", age_month, "month(s)", age_day,
                          "day(s)")
                    print("\n\033[0;30;46m>>>Next Birthday comes in\033[1;37;40m", rem_month, "month(s)", rem_day,
                          "day(s)")
                elif today.month == n.month and today.day > n.day:
                    age_day = today.day - n.day
                    rem_month = 11
                    rem_day = (rem_days - today.day) + n.day + 1
                    print("\n\033[0;30;46m>>>Age =\033[1;37;40m", age_year, "years", age_day, "day(s)")
                    print("\n\033[0;30;46m>>>Next Birthday comes in\033[1;37;40m", rem_month, "month(s)", rem_day,
                          "day(s)")
                elif today.month > n.month and today.day == n.day:
                    age_month = today.month - n.month
                    rem_month = (n.month + 12) - today.month
                    print("\n\033[0;30;46m>>>Age =\033[1;37;40m", age_year, "years", age_month, "month(s)")
                    print("\n\033[0;30;46m>>>Next Birthday comes in\033[1;37;40m", rem_month, "month(s)")
                elif today.month < n.month and today.day == n.day:
                    age_month = (today.month + 12) - n.month
                    rem_month = n.month - today.month
                    print("\n\033[0;30;46m>>>Age =\033[1;37;40m", age_year, "years", age_month, "month(s)")
                    print("\n\033[0;30;46m>>>Birthday comes in\033[1;37;40m", rem_month, "month(s)")
                elif today.month < n.month and today.day < n.day:
                    age_month = (today.month + 11) - n.month
                    age_day = (days - n.day) + today.day
                    rem_month = n.month - today.month
                    rem_day = n.day - today.day
                    print("\n\033[0;30;46m>>>Age =\033[1;37;40m", age_year, "years", age_month, "month(s)", age_day,
                          "day(s)")
                    print("\n\033[0;30;46m>>>Birthday comes in\033[1;37;40m", rem_month, "month(s)", rem_day,
                          "day(s)")
                elif today.month == n.month and today.day < n.day:
                    age_month = (today.month + 11) - n.month
                    age_day = (days - n.day) + today.day
                    rem_day = n.day - today.day
                    print("\n\033[0;30;46m>>>Age =\033[1;37;40m", age_year, "years", age_month, "month(s)", age_day,
                          "day(s)")
                    print("\n\033[0;30;46m>>>Birthday comes in\033[1;37;40m", rem_day, "day(s)")
                elif today.month > n.month and today.day < n.day:
                    age_month = today.month - n.month - 1
                    age_day = (days - n.day) + today.day
                    rem_month = n.month + 12 - today.month
                    rem_day = n.day - today.day
                    if age_month:
                        print("\n\033[0;30;46m>>>Age =\033[1;37;40m", age_year, "years", age_month, "month(s)",
                              age_day, "day(s)")

                    else:
                        print("\n\033[0;30;46m>>>Age =\033[1;37;40m", age_year, "years", age_day, "day(s)")
                    print("\n\033[0;30;46m>>>Next Birthday comes in\033[1;37;40m", rem_month, "month(s)", rem_day,
                          "day(s)")
                elif today.month < n.month and today.day > n.day:
                    age_month = (today.month + 12) - n.month
                    age_day = today.day - n.day
                    rem_month = n.month - today.month - 1
                    rem_day = (rem_days - today.day) + n.day
                    print("\n\033[0;30;46m>>>Age =\033[1;37;40m", age_year, "years", age_month, "month(s)", age_day,
                          "day(s)")
                    if rem_month:
                        print("\n\033[0;30;46m>>>Birthday comes in\033[1;37;40m", rem_month, "month(s)", rem_day,
                              "day(s)")
                    else:
                        print("\n\033[0;30;46m>>>Birthday comes in\033[1;37;40m", rem_day, "day(s)")
                break
            except ValueError:
                print("\n\033[0;37;41m\a[-] INVALID DATE\033[0;30;40m #")
        pass

    def factorial(self, values):
        print("\n")
        for i in values:
            f = 1
            i = int(i)
            for j in range(1, i + 1):
                f = f * j
            print("\033[0;30;46m>>>FACTORIAL OF", i, "=\033[1;37;40m", f)
        pass

    def percentage(self, values):
        print("\n")
        count = value = 0
        per = ""
        for i in values:
            count += 1
            per += str(i) + ","
            value += i
        print("\033[0;30;46m>>>PERCENTAGE OF %s =\033[1;37;40m" % per, value / count)

    def sq_rt(self, values):
        print("\n")
        for i in values:
            print("\033[0;30;46m>>>SQUARE ROOT OF ", i, "=\033[1;37;40m", i ** (1 / 2))

    def cube_rt(self, values):
        print("\n")
        for i in values:
            print("\033[0;30;46m>>>CUBE ROOT OF ", i, "=\033[1;37;40m", i ** (1 / 3))

    def maxi(self, values):
        max_value = values[0]
        for x in values:
            if x > max_value:
                max_value = x
        return max_value

    def leap(self, i):
        if i % 4 == 0 and i % 100 != 0 or i % 400 == 0:
            return True
        else:
            return False

    def gcd(self, values):
        print("\n")
        gcd_value = values[0]
        for i in values[1:]:
            def gcdof(a, b):
                if b == 0:
                    return a
                else:
                    return gcdof(b, a % b)

            gcd_value = gcdof(gcd_value, i)
        print("\033[0;30;46m>>>GCD =\033[1;37;40m", gcd_value)

    def lcm(self, values):
        max_value = self.maxi(values)
        vals = []
        deci = 0
        while True:
            for j in values:
                j = str(j)
                if '.' in j:
                    deci = len(j.split('.')[1])
                    for i in values:
                        i *= (10 ** deci)
                        vals.append(i)
                    max_value = self.maxi(vals)
                    values.clear()
            break
        while True:
            for i in vals:
                i = int(i)
                if max_value % i != 0:
                    max_value += 1
                    break
            else:
                break
        while True:
            for i in values:
                if max_value % i != 0:
                    max_value += 1
                    break
            else:
                break
        print("\033[0;30;46m>>>LCM =\033[1;37;40m", max_value // (10 ** deci))

    def chk_prime(self, values):
        print("\n")
        for num in values:
            num = int(num)
            if num > 1:
                for i in range(2, num):
                    if (num % i) == 0:
                        print("\033[0;30;46m>>>", num, "\033[1;37;40m is not a prime number")
                        break
                else:
                    print("\033[0;30;46m>>>", num, "\033[1;37;40m is a prime number")
            else:
                print("\033[0;30;46m>>>", num, "\033[1;37;40m is neither a prime nor composite")
        pass

    def factors(self, values):
        print("\n")
        for i in values:
            i = int(i)
            print("\033[0;30;46m>>>The factors of", i, "are:\033[1;37;40m", end=" ")
            for j in range(1, int(i + 1)):
                if i % j == 0:
                    print(j, end=" ")
            print("\n")
        print("\n")

    def sin(self, values):
        print("\n")
        for i in values:
            j = math.radians(i)
            print("\033[0;30;46m>>>SINE OF", i, "=\033[1;37;40m", math.sin(j))

    def cos(self, values):
        print("\n")
        for i in values:
            j = math.radians(i)
            print("\033[0;30;46m>>>COSINE OF", i, "=\033[1;37;40m", math.cos(j))

    def tang(self, values):
        print("\n")
        for i in values:
            j = math.radians(i)
            print("\033[0;30;46m>>>TANGENT OF", i, "=\033[1;37;40m", math.tan(j))

    def palindrome(self, values):
        for n in values:
            num = n
            s = 0
            while n:
                d = n % 10
                s = s * 10 + d
                n = n // 10
            print("\n\033[0;30;46m>>>Reverse of %d =\033[1;37;40m %d" % (num, s))
            if num == s:
                print("\033[0;30;46m%d is a Palindrome\033[0;30;40m#" % num)
            else:
                print("\n\033[0;30;46m%d is not a Palindrome\033[0;30;40m#" % (num))
        pass

    pass
