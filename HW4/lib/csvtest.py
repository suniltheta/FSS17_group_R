import sys
import os.path
from tbl import Tbl
import time
from csv import CSV

def main(src):
    file_name = "../data/" + src
    if not os.path.exists(file_name):
        print("File {} does not exist in current path\n".format(file_name))
        return
    print("File {} exist in current path\n".format(file_name))
    CSV(src, print)


if __name__ == "__main__":
    if len(sys.argv) > 1:
         main(sys.argv[1])
    else:
         print("Please enter the .csv file name")