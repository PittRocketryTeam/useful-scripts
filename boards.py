#!/usr/bin/python3

import os
import sys

""" GLOBAL VARS """

# lockfile fn
LOCKFILE = ".lock"
# temporary file directory
DIR = "/tmp/soar"
# list of all teensy boards plugged in
BOARDS = []
# username
USER = ""
# users currently logged in
ACTIVE = []

""" USEFUL METHODS """

def lockfile_fn():
    return os.path.join(DIR, LOCKFILE)

def board_lockfile_fn(index):
    return os.path.join(DIR, ".{}".format(BOARDS[index]))

# grab the latest info
def refresh():
    global BOARDS
    global USER
    global ACTIVE

    BOARDS = os.popen("ls /dev | grep \"ttyACM\"").read().split("\n")
    USER = os.environ.get("USER")
    ACTIVE = list(set(os.popen("w | awk \'NR>2 {print$1;}\'").read().split("\n")))
 
    if not os.path.isdir(DIR):
        os.mkdir(DIR)

# set environment variable for the user
def export(board):
    os.environ["BOARD"] = os.path.join("/dev", board)

""" TO BE IMPLEMENTED """

# enter the critical section, or busy wait until it is available
def lock():
    pass

# delete lockfile and leave critical section
def unlock():
    pass

# if a user logged out and didn't "put their board back", delete the board specific lockfile
def synchronize():
    pass

# reserve a board for use, index of -1 means pick any available board, otherwise, pick BOARDS[index]
def get_board(index=-1):
    pass

# stop using a board
def put_board():
    pass

""" BORING SETUP STUFF + MAIN METHOD """

def print_usage():
    print("\nusage: board.py <verb> [args]\n\nexamples:\n\tboard.py get\n\tboard.py put\n")

def main():
    refresh()

    if len(sys.argv) < 2:
        print_usage()
        return

    verb = sys.argv[1]
    index = -1
    if len(sys.argv) > 2:
        try:
            index = int(sys.argv[2])
        except:
            print("index must be an integer")
            return

    if verb == "get":
        get_board(index)
    elif verb == "put":
        put_board(index)

if __name__ == "__main__":
    main()
