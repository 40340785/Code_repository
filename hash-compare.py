#Welcome to this program, its purpose is to verify is a hash matches a files hash.
#This will be useful if you download a file and a website has the hash of what the file should be.
#This is used to verify is a file has not been tampered with.

import hashlib
import sys
import os

def main():

    try:

        hash = sys.argv[1].lower()  #First argument, the hash to compare to the file.
        file = sys.argv[2]  #Second argument is the file path.
        buffer = 65536  #Buffer size (64kb), to make the program not a memory hog.
        if(os.path.exists(file)):   #Check is file exists.
            if(len(hash) == 32):    #Checks hash length, if 32 characters it is an MD5
                print("MD5")    #Prints the hash type
                md5Func(hash, file, buffer) #Passes the hash, file and buffer size to correct function.
            elif(len(hash) == 40):  #Checks hash length, if 40 characters it is an SHA1
                print("SHA1")   #Prints the hash type
                sha1Func(hash, file, buffer)
            elif(len(hash) == 64): #Checks hash length, if 64 characters it is an SHA256
                print("SHA256") #Prints the hash type
                sha256(hash, file, buffer)
            else:
                print("Error unknown hash length")
        else:
            print("Error file does not exist/invalid, or input order incorrect! \nFormat: \nArgument 1 = Hash, \nArgument 2 = File path")
    except IndexError:
        print("Error, program expects 2 arguments, use the format: \nArgument 1 = Hash, \nArgument 2 = File path.")

def md5Func(hash, file, buffer):    #Function recieves the variables hash, file and buffer.

    md5hasher = hashlib.md5()   #Loads hashlib MD5
    with open(file, 'rb') as open_file: #Opens the file as read only
        while True:
            content = open_file.read(buffer)    #Opens the file in 64kb chunks.
            if not content: #If not content end.
                break
            md5hasher.update(content)   #Updates the hashlib MD5
    md5output = (md5hasher.hexdigest()) #Changes the MD5 into hexidecmal format.

    if (hash == md5output): #Checks if the hash inputted is the same as the files hash
        print("They are the same")
    else:
        print("They no match")

def sha1Func(hash, file, buffer):

    sha1hasher = hashlib.sha1()
    with open(file, 'rb') as open_file:
        while True:
            content = open_file.read(buffer)
            if not content:
                break
            sha1hasher.update(content)
    sha1output = (sha1hasher.hexdigest())

    if (hash == sha1output):
        print("They are the same")
    else:
        print("They no match")

def sha256(hash, file, buffer):

    sha256hasher = hashlib.sha256()
    with open(file, 'rb') as open_file:
        while True:
            content = open_file.read(buffer)
            if not content:
                break
            sha256hasher.update(content)
    sha256output = (sha256hasher.hexdigest())

    if (hash == sha256output):
        print("They are the same")
    else:
        print("They no match")


if __name__=="__main__": main()