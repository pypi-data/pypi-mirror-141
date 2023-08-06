import sys
import os
from modelify import run_server
from modelify.utils.constants import  APP_FOLDER


def main():
    print(os.getcwd())
    print("APP_FOLDER", APP_FOLDER)
    args = sys.argv[1:]
    if args[0] == "runserver":
        if len(args) > 1:
            run_server(port=int(args[1]), tunnel=False)
        else:
            run_server(tunnel=False)

if __name__ == '__main__':
    main()