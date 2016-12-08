# eavesdrop
A sniffing app to pull redundant copied of submission forms or 
other Ethernet traffic. Part of Unhackable Server Project. 

Eavesdrop, at this point just sits and sniffs. Once you run it,
 it will keep sniffing and putting data into a text file until you kill it or until it captures 
 50 packets.
 To change the limit, edit:
        cap.sniff(packet_count=50) 
 by changing 50 to whatever limit you want.
  It is programmed to get everything that is on "en0". There is no filter so everything
 is written in the text file. 
 The text file is named "Eavesdrop_Data.txt". Every time you run the program, if you do not change the file name,
 the file will be overwritten with the new data.
 I will try and write a user interface to give the user some options