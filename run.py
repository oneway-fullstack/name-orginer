import sys, getopt

from utils.parser import Parser

def main(argv):
    try:
        options, reminder = getopt.getopt(argv, "f:s:",['file', 'name'])
    except getopt.GetoptError:
        print('Standard command >>> run.py -f c:/mock.txt ||  run.py -s "james, wangwei"')
        sys.exit(2)

    opt, arg = options[0]
    Parser.run(opt, arg)

if __name__ == "__main__":
    main(sys.argv[1:])
