from collections import namedtuple
from fileinput import close
from genericpath import getsize
import hashlib
import struct
import datetime
import os
import sys
import uuid

#bin_f = "bchoc.bin"
bin_f = os.environ.get('BCHOC_FILE_PATH', 'bchoc.bin')

blockHeadF = struct.Struct('32s d 16s I 12s I')

bHead = namedtuple('Block_Head', 'hash timestamp caseID itemID state length')
bData = namedtuple('Block_Data', 'data')   
fd2 = 0

def initBlock(bin_file, mode):
    with open(bin_file, mode) as fout:
        currTime = datetime.datetime.now()
        currTime = datetime.datetime.timestamp(currTime)*1000
        packed = blockHeadF.pack(b'None', currTime, b'None', 0, b'INITIAL', 14)
        fout.write(packed)
        blockDataF = struct.Struct('14s')
        packed = blockDataF.pack(b'Initial Block')
        fout.write(packed)
        print("Blockchain file not found. Created INITIAL block.")

def checkInit(bin_file):
    flag = False
    with open(bin_file, 'rb') as fd:
        head = fd.read(blockHeadF.size)
                #if not head:
                 #   break
        block = bHead._make(blockHeadF.unpack(head))
        state = block.state.decode('utf-8')
        if (state[0:7] == 'INITIAL'):
            flag = True
        fd.close()
    return flag

def open_bchoc(bin_file):
    try:
        initBlock(bin_file, 'xb')
    except FileExistsError:
        flag = checkInit(bin_file)
        if flag:
            print("Blockchain file found with INITIAL block.")
        else:
            initBlock(bin_file, 'ab')
                
def get_prev_block(bin_file):
    lastBlock = None
    with open(bin_file, 'rb') as f:
        while True:
            head = f.read(blockHeadF.size)
            if not head:
                break
            block = bHead._make(blockHeadF.unpack(head))
            data = f.read(block.length)
            lastBlock = head
    return lastBlock


def save_bchoc(blockchain):
    for block in blockchain:
        #Method must convert blockchain to byte format
        pass
    if fd != None:
        fd.write(blockchain)
    else:
        print("File is not open or can not be written to!")

def add(hash, ts, caseID, itemID, state, length):
    fd1 = open(bin_f, 'ab')
    new_item = blockHeadF.pack(str.encode(hash), ts, caseID.bytes, itemID, str.encode(state), length)
    b = bHead._make(blockHeadF.unpack(new_item))
    fd1.write(new_item)
    blockDataF = struct.Struct('0s')
    data = blockDataF.pack(b'')
    fd1.write(data)
    pass
    

def get_hash(block):
    return hashlib.sha256(block).hexdigest()

def displayData(block):
    print("Previous Hash: " + block.hash.decode('utf-8'))
    print("Timestamp: " + str(datetime.datetime.fromtimestamp(block.timestamp/1000)))
    #print("Case ID: " + block.caseID.decode('utf-8'))
    print("Case ID: ", str(uuid.UUID(bytes=block.caseID)))
    print("Evidence Item ID: " + str(block.itemID))
    print("State: " + block.state.decode('utf-8'))
    print("Data Length: " + str(block.length))
    pass

def checkoutBlock(itemID):
    targetBlock = None
    flag = False
    with open(bin_f, 'rb') as f:
        while True:
            head = f.read(blockHeadF.size)
            if not head:
                break
            block = bHead._make(blockHeadF.unpack(head))
            blockDataF = struct.Struct(str(block.length) + 's')
            data = f.read(block.length)
            if (block.itemID == itemID):
                state = block.state.decode('utf-8')
                if (state[0:9] == 'CHECKEDIN'):
                    caseID = block.caseID
                    presentDate = datetime.datetime.now()
                    unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
                    
                    prevBlock = get_prev_block(bin_f)
                    add(get_hash(prevBlock), unix_timestamp, uuid.UUID(str(uuid.UUID(bytes = caseID))), int(itemID), 'CHECKEDIN', 0)
                    
                    print("Case: ", str(uuid.UUID(bytes = caseID)))
                    flag = True
                    break
                else:
                    break
    return flag

def checkinBlock(itemID):
    targetBlock = None
    flag = False
    with open(bin_f, 'rb') as f:
        while True:
            head = f.read(blockHeadF.size)
            if not head:
                break
            block = bHead._make(blockHeadF.unpack(head))
            blockDataF = struct.Struct(str(block.length) + 's')
            data = f.read(block.length)
            if (block.itemID == itemID):
                state = block.state.decode('utf-8')
                if (state[0:9] == 'CHECKEDOUT'):
                    caseID = block.caseID
                    presentDate = datetime.datetime.now()
                    unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
                    
                    prevBlock = get_prev_block(bin_f)
                    add(get_hash(prevBlock), unix_timestamp, uuid.UUID(str(uuid.UUID(bytes = caseID))), int(itemID), 'CHECKEDOUT', 0)
                    
                    print("Case: ", str(uuid.UUID(bytes = caseID)))
                    flag = True
                    break
                else:
                    break
    return flag

def log(caseID, itemID, num_entries, reverseFlag):
    blockList = []
    presentDate = datetime.datetime.now()
    unix_timestamp = datetime.datetime.timestamp(presentDate)*1000

    with open(bin_f, 'rb') as f:
        while True:
            try:
                head = f.read(blockHeadF.size)
                currBlock = bHead._make(blockHeadF.unpack(head))
                blockData = struct.Struct(str(currBlock.length) + 's')
                data = f.read(currBlock.length)
                currData = bData._make(blockData.unpack(data))
                blockList.append((currBlock,currData))
            except:
                break
    
    if str(caseID) != '-1' or int(itemID) != -1: #this will pretty much always be true unless only log argument is typed
        caseIDIndList = []
        itemIDIndList = []
        for i in range(0, len(blockList)):
            if str(uuid.UUID(bytes = blockList[i][0].caseID)) == caseID and str(caseID) != '-1':
                caseIDIndList.append(i)
            if int(blockList[i][0].itemID) == int(itemID) and int(itemID) != -1:
                itemIDIndList.append(i)
        combinedIndList = list(set(caseIDIndList) & set(itemIDIndList)) #intersect the list if both caseID and itemID are given, if only 1 it will be blank
    else: # if log is by itself with no args print everything
        combinedIndList = list(range(0, len(blockList)))

    if len(combinedIndList) == 0 and len(caseIDIndList) == 0: #since only caseID or itemID is needed, choose which one is not blank else use the intersected list from above
        length = itemIDIndList
    elif len(combinedIndList) == 0 and len(itemIDIndList) == 0:
        length = caseIDIndList
    else:
        length = combinedIndList
        
        
    if reverseFlag:
        length.reverse()
    if num_entries != -1:
        length = length[:int(num_entries)] #doesn't matter if num_entries is greater than the list size as it will just print everything

    for i in range(len(length)):
        print("Case: ", str(uuid.UUID(bytes = blockList[length[i]][0].caseID)))
        print("Item: ", int(blockList[length[i]][0].itemID))
        print("Action:", blockList[i][0].state.decode())
        print("Time: ", str(blockList[i][0].timestamp) + "\n")
