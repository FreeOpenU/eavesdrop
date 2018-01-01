# eavesdrop

 ## Synopsis
A sniffing app to pull redundant copies of submission forms or 
other Ethernet traffic. Part of Unhackable Server Project. 

## Code Information

Eavesdrop, sniffs the network, parses out text and saves it to a file.
    Using the command line, it initiates a packet capture that pipes the stdout into the python program.
    The capture pipes the ENTIRE packet but does not save it because it is not needed. 
    I will save the finished packet as a variable, do what needs to be done and overwrite the variable with the nest packet.
    The app is meant to be as small as possible.
##User Interface
   The user interface, at this point only allows the user (let's call him Dave) to chose with device he want't to sniff on.
   I mean to add some nore functionality:
 
  -[x] Dave can choose what type of payload he wants to save.
  
  -[ ] Dave can go in and see how many of each kind of requests and
       responses the device has been receiving.
       
  -[x] Dave can see how many total packets are passing through
  
  -[x] Dave can choose where the payload is being stored
  
  -[x] Dave can kill the sniff
  
  -[x] Dave can count/ see a graph of malformed packets to see if Hal is misbehaving
  
  -[x] Dave can choose which device to sniff on
  
 


## Packaging Eavesdrop:

    I used PyInstaller to package the program into a binary executable.
The drawback is that the binary file can only be used on the same type of
system it was created on.
To create the executable, change into the eavesdrop directory and
Use: ```pyinstaller --onefile UserInt.py```

This will create two folders, build and dist.The executable will be in
the dist folder.
## Using the binaries
There are two binaries, one for Mac and one for Linux. The Mac can only work on Mac O.S. but the Linux
version can  work on windows in addition to Linux if you install Cygwin.

## Running the application

The system must have tshark on it but that's it! 



