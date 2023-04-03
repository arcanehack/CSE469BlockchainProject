from dataclasses import dataclass
from dis import dis
from genericpath import exists
import sys
import numpy
import datetime
import os
import uuid
import bchocOps

#bin_file = 'bchoc.bin'
bin_file = os.environ.get('BCHOC_FILE_PATH', 'bchoc.bin')
#bchocOps.open_bchoc(bin_file)

def main():
    if (len(sys.argv) >= 2 and sys.argv[1] == "add"):
        if (len(sys.argv) >= 6 and sys.argv[2] == "-c" and sys.argv[4] == "-i"):
            caseID = sys.argv[3] #caseId needs to be 128 bit
            print("Case: ", uuid.UUID(caseID))

            # Loop through all items
            i = 5
            while (i < len(sys.argv)):
                if (sys.argv[i - 1] != "-i"):
                    displayCorrectAdd(True)

                itemID = sys.argv[i]
                # use proper time library to get time
                presentDate = datetime.datetime.now()
                unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
                # check if itemid already exists here
                # build block and add to chain here
                if not bchocOps.checkInit(bin_file):
                    print("Blockchain has not been initialized!")
                    exit(9)
                
                prevBlock = bchocOps.get_prev_block(bin_file)
                bchocOps.add(bchocOps.get_hash(prevBlock), unix_timestamp, uuid.UUID(caseID), int(itemID), 'CHECKEDIN', 0)

                print("Added item: " + str(itemID))
                print("\tStatus: CHECKEDIN")
                print("\tTime of action: ", presentDate)

                i += 2
        else:
            # exit on invalid format
            # add exit to all places of invalid format
            displayCorrectAdd(True)
    elif (len(sys.argv) >= 2 and sys.argv[1] == "checkout"):
        if (len(sys.argv) == 4 and sys.argv[2] == "-i"):
            itemID = sys.argv[3]

            # do checkout here
            if  not bchocOps.checkoutBlock(int(itemID)):
                print("Error: Cannot check out a checked out item. Must check it in first.")
                displayCorrectCheckout(True)

            status = "CHECKEDOUT"
            presentDate = datetime.datetime.now()

            print("Checked out item: " + str(itemID))
            print("\tStatus: " + status)
            print("\tTime of action: ", presentDate)
        else:
            displayCorrectCheckout(True)
    elif (len(sys.argv) >= 2 and sys.argv[1] == "checkin"):
        if (len(sys.argv) == 4 and sys.argv[2] == "-i"):
            itemID = sys.argv[3]

            # maybe error check if item already checked in here

            # do checkin here
            if  not bchocOps.checkinBlock(int(itemID)):
                print("Error: Cannot check in a checked in item. Must check it out first.")
                displayCorrectCheckin(True)

            # correctly assign variables under
            # caseID = 0
            status = "CHECKEDIN"
            presentDate = datetime.datetime.now()

            print("Checked in item: " + str(itemID))
            print("\tStatus: " + status)
            print("\tTime of action: ", presentDate)
        else:
            displayCorrectCheckin(True)
    elif (len(sys.argv) >= 2 and sys.argv[1] == "log"):
        # multiple [] in arg so maybe change arg checks
        reverse = False
        num = -1
        caseID = -1
        itemID = -1
        # loop through args and store all optional values
        for i in range(0, len(sys.argv)):
            if (sys.argv[i] == "-r"):
                reverse = True
            elif (sys.argv[i] == "-n"):
                if (i + 1 < len(sys.argv)):
                    num = sys.argv[i + 1]
                else:
                    displayCorrectLog(True)
            elif (sys.argv[i] == "-c"):
                if (i + 1 < len(sys.argv)):
                    caseID = sys.argv[i + 1]
                else:
                    displayCorrectLog(True)
            elif (sys.argv[i] == "-i"):
                if (i + 1 < len(sys.argv)):
                    itemID = sys.argv[i + 1]
                else:
                    displayCorrectLog(True)

        # compare the values of var above to their default of -1
        # do proper log here based on difference
        # logs should use a loop
        # assign var under in loop and print
        bchocOps.log(caseID, itemID, num, reverse)
        '''tempCaseID = 0
        tempItemID = 1
        tempStatus = "CHECKEDIN"
        tempTime = "2022"

        print("Case: " + str(tempCaseID))
        print("Item: " + str(tempItemID))
        print("Action: " + tempStatus)
        print("Time: " + tempTime + "\n")'''
    elif (len(sys.argv) >= 2 and sys.argv[1] == "remove"):
        if (len(sys.argv) >= 6 and sys.argv[2] == "-i" and (sys.argv[4] == "-y" or sys.argv[4] == "--why")):
            itemID = sys.argv[3]
            reason = sys.argv[5]
            reasonReleased = False
            owner = "NULL"
            if (reason == "DISPOSED" or reason == "DESTROYED" or reason == "RELEASED"):
                if (reason == "RELEASED"):
                    reasonReleased = True
                    if (len(sys.argv) == 8 and sys.argv[6] == "-o"):
                        owner = sys.argv[7]
                    else:
                        displayCorrectRemove(True)
                elif (len(sys.argv) != 6):
                    displayCorrectRemove(True)
            else:
                displayCorrectRemove(True)

            # do remove here
            # assign var under
            caseID = 0
            status = "RELEASED"
            time = "2022"

            print("Case: " + str(caseID))
            print("Removed item: " + str(itemID))
            print("\tStatus: " + status)
            if (reasonReleased):
                print("\tOwner info: " + owner)
            print("\tTime of action: " + time)
        else:
            displayCorrectRemove(True)
    elif (len(sys.argv) >= 2 and sys.argv[1] == "init"):
        if (len(sys.argv) == 2):
            # check if blockchain file exists here
            # verify initial block here
            bchocOps.open_bchoc(bin_file)
        else:
            displayCorrectInit(True)
    elif (len(sys.argv) >= 2 and sys.argv[1] == "verify"):
        if (len(sys.argv) == 2):
            # verify block chain here
            # assign bad var under
            transactions = 0
            state = "ERROR"
            badParent = False
            badChecksum = False
            badState = False

            print("Transactions in blockchain: " + str(transactions))
            print("State of blockchain: " + state)
            if (badParent or badChecksum or badState):
                print("Bad block: " + "checksum here?")
                if (badParent):
                    print("Parent block: " + "checksum here?")
                    print("Two blocks were gound with the same parent.")
                elif (badChecksum):
                    print("Block contents do not match block checksum.")
                elif (badState):
                    print("Item checked out or checked in after removal from chain.")
        else:
            displayCorrectVerify(True)
    else:
        displayCorrectFormat()

def displayCorrectFormat():
    print("Usage of bchoc: ")
    displayCorrectAdd(False)
    displayCorrectCheckin(False)
    displayCorrectCheckout(False)
    displayCorrectLog(False)
    displayCorrectRemove(False)
    displayCorrectInit(False)
    displayCorrectVerify(False)

    exit(1)

def displayCorrectAdd(flag):
    print("\tbchoc add -c <case_id> -i <item_id> [-i <item_id>]")
    print("\t\tcase_id: 128-bit integer")
    print("\t\titem_id: 32-bit integer")
    print("\t\t[-i <item_id>] can be repeated, but there must be at least one instance it")
    print("")
    
    if flag: exit(2)
 
def displayCorrectCheckout(flag):
    print("\tbchoc checkout -i <item_id>")
    print("\t--Add new checkout entry to chain of custody that is already in blockchain--")
    print("\t\titem_id: 32-bit integer")
    print("")
    if flag: exit(3)  
    
def displayCorrectCheckin(flag):
    print("\tbchoc checkin -i <item_id>")
    print("\t--Add new checkin entry to chain of custody that is already in blockchain--")
    
    print("\t\titem_id: 32-bit integer")
    print("")
    if flag: exit(4)
       
def displayCorrectLog(flag):
    print("\tbchoc log [-r] [-n <num_entries>] [-c <case_id>] [-i <item_id>]")
    print("\t--shows the blockchain entries giving the oldest first--")
    
    print("\t\tnum_entries: 128-bit integer")
    print("\t\tcase_id: 128-bit integer")
    print("\t\titem_id: 32-bit integer")
    
    print("\t\t[-r, --reverse], shows order of block entreis from most recent entries first")
    print("\t\t[-n <num_entries>], shows <num_entries> block entries")
    print("\t\t[-c <case_id>] can be repeated, it is not necessary for the command to work")
    print("\t\t[-i <item_id>] can be repeated, it is not necessary for the command to work")
    print("")
    if flag: exit(5)
    
def displayCorrectRemove(flag):
    print("\tbchoc remove -i <item_id> -y <reason> [-o <owner>]")
    print("\t--Prevents further action on evidence item specifiec, must be checkedin--")
    
    print("\t\titem_id: 32-bit integer")
    print("\t\t-y, --why <reason>: <reason> for removal of evidence item")
    print("\t\t\t<reason>: must be DISPOSED, DESTROYED, or RELEASED")
    
    print("\t\t[-o <owner>]: must be specfied if <reason> is RELEASED")
    print("\t\t\t<owner>: Information about lawful owner to whom the evidence was released")
    print("")
    
    if flag: exit(6)
    
def displayCorrectInit(flag):
    print("\tbchoc init")
    print("\t--Starts up and checks for inital block--")
    print("")
    
    if flag: exit(7)

def displayCorrectVerify(flag):
    print("\tbchoc verify")
    print("\t--Validates all of the entries in the blockchain--")
    print("")
    
    if flag: exit(8)

if __name__ == "__main__":
    main()
