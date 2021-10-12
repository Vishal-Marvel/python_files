while True:
    y = int(input("Enter a year: "))

    if y%4==0 and y%100!=0 or y%400==0:
        print(f'{y} is a leap year')
    else:
        print(f'{y} is not a leap year')