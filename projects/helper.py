import argparse, os, time

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--function", dest="function", help="Function you want help of.")
    options = parser.parse_args()
    if options.function:
        return options
    else:
        parser.exit(message='\n[-] -f is compulsory. Type -h for more info\n')

options = get_arguments()
os.system('python help.py %s > help.txt'%options.function)
# time.sleep(1)
f = open('help.txt', 'r')
text = f.read()
f.close()
if not 'No Python documentation found for' in text:
    new_text = ''
    for i in text.split('\n'):
        if 'http' in i:
            new_text += f'<a href="{i}" target="blank">{i}</a><br>'
            continue
        new_text += i + '<br>'

    html = '''<!doctype html>
    <html lang="en">
    <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

        <title>Help</title>
    </head>
    <body>
    <div class="container">
    <br><br>
        <p>{}</p>
        </div>
        <!-- Optional JavaScript; choose one of the two! -->

        <!-- Option 1: Bootstrap Bundle with Popper -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>

        <!-- Option 2: Separate Popper and Bootstrap JS -->
        <!--
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js" integrity="sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF" crossorigin="anonymous"></script>
        -->
    </body>
    </html>'''.format(new_text)
    f = open('help.txt', 'w')
    f.write(html)
    f.close()
    os.rename('help.txt', 'help.html')

    os.startfile("help.html")
    time.sleep(2)
    while True:
        try:
            os.remove("help.html")
        except PermissionError:
            time.sleep(1)
        except FileNotFoundError:
            break
else:
    print('\n[-] No Python documentation found for %s\n'%(options.function))