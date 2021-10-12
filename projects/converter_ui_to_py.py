import getopt
import os
import sys

def main(argv):
    opts, args = getopt.getopt(argv, "i:")
    for o, a in opts:
        if o in ("-i", "--ifile"):
            ui_file = a + '.ui'
            py_file = 'converted/' + a + '.py'
            run(ui_file, py_file)


def run(ui_file, py_file):
    print("Converting " + ui_file)
    os.system('pyuic5 -x ' + ui_file + ' -o ' + py_file)
    # os.startfile(py_file)
    print("Converted")
if __name__ == '__main__':  # program starts executing from here
    main(sys.argv[1:])