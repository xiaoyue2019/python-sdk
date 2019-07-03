'''
  bcosliteclientpy is a python client for FISCO BCOS2.0 (https://github.com/FISCO-BCOS/FISCO-BCOS)
  bcosliteclientpy is free software: you can redistribute it and/or modify it under the terms of the MIT License as published by the Free Software Foundation
  This project is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE
  Thanks for authors and contributors of eth-abi，eth-account，eth-hash，eth-keys，eth-typing，eth-utils，rlp, eth-rlp , hexbytes ...and relative projects
  @author: kentzhang
  @date: 2019-06
'''
from client.bcosclient import (
    BcosClient,
    BcosError
)
import os
from eth_utils import to_checksum_address
from client.datatype_parser import DatatypeParser

client = BcosClient()
info = client.init()
print(info)


#从文件加载abi定义
abi_file  ="contracts/SimpleInfo.abi"
data_parser = DatatypeParser()
data_parser.load_abi_file(abi_file)
contract_abi = data_parser.contract_abi

#部署合约
print("\n>>Deploy:---------------------------------------------------------------------")
with open("contracts/SimpleInfo.bin", 'r') as load_f:
    contract_bin = load_f.read()
    load_f.close()
result = client.deploy(contract_bin)
print("deploy",result)
print("new address : ",result["contractAddress"])
contract_name =  os.path.splitext(os.path.basename(abi_file))[0]
memo = "tx:"+result["transactionHash"]
#把部署结果存入文件备查
from client.contractnote import ContractNote
ContractNote.save_address(contract_name, result["contractAddress"], int(result["blockNumber"], 16), memo)


#发送交易，调用一个改写数据的接口
print("\n>>sendRawTransaction:----------------------------------------------------------")
to_address = result['contractAddress'] #use new deploy address
args = ['simplename', 2024, to_checksum_address('0x7029c502b4F824d19Bd7921E9cb74Ef92392FB1c')]

receipt = client.sendRawTransactionGetReceipt(to_address,contract_abi,"set",args)
print("receipt:",receipt)

#解析receipt里的log
print("\n>>parse receipt and transaction:----------------------------------------------------------")
txhash = receipt['transactionHash']
print("transaction hash: " ,txhash)
logresult = data_parser.parse_event_logs(receipt["logs"])
i = 0
for log in logresult:
    if 'eventname' in log:
        i = i + 1
        print("{}): log name: {} , data: {}".format(i,log['eventname'],log['eventdata']))
#获取对应的交易数据，解析出调用方法名和参数

txresponse = client.getTransactionByHash(txhash)
inputresult = data_parser.parse_transaction_input(txresponse['input'])
print("transaction input parse:",txhash)
print(inputresult)

#解析该交易在receipt里输出的output,即交易调用的方法的return值
outputresult  = data_parser.parse_receipt_output(inputresult['name'], receipt['output'])
print("receipt output :",outputresult)


#调用一下call，获取数据
print("\n>>Call:------------------------------------------------------------------------")
res = client.call(to_address,contract_abi,"getbalance")
print("call getbalance result:",res)
res = client.call(to_address,contract_abi,"getbalance1",[100])
print("call getbalance1 result:",res)
res = client.call(to_address,contract_abi,"getname")
print("call getname:",res)
res = client.call(to_address,contract_abi,"getall")
print("call getall result:",res)


#以下是查询类的接口，大部分是返回json，可以根据对fisco bcos rpc接口json格式的理解，进行字段获取和转码
'''
useful helper:
int(num,16)  hex -> int
hex(num)  : int -> hex
'''

doQueryTest =False
if doQueryTest:
    print("\n>>---------------------------------------------------------------------")
    res = client.getNodeVersion()
    print("\n>>---------------------------------------------------------------------")
    print("getClientVersion",res)
    print("\n>>---------------------------------------------------------------------")
    try:
        res = client.getBlockNumber()
        print("getBlockNumber",res)
    except BcosError as e:
        print("bcos client error,",e.info())
    print("\n>>---------------------------------------------------------------------")
    print("getPeers",client.getPeers())
    print("\n>>---------------------------------------------------------------------")
    print("getBlockByNumber",client.getBlockByNumber(50))
    print("\n>>---------------------------------------------------------------------")
    print("getBlockHashByNumber",client.getBlockHashByNumber(50))
    print("\n>>---------------------------------------------------------------------")
    print("getBlockByHash",client.getBlockByHash("0xe7588bf4ee5a6fb5aae9bdcc2c4f3c58cf7a789b15a4daa6617ed594b5ba3951"))
    print("\n>>---------------------------------------------------------------------")
    print("getTransactionByHash",client.getTransactionByHash("0x41fa9a0ce36d486ee2bf6d2219b68b44ca300ec7aeb07f8f2aa9c225655d2b61"))
    print("\n>>---------------------------------------------------------------------")
    print("getTransactionByBlockHashAndIndex",client.getTransactionByBlockHashAndIndex("0xe7588bf4ee5a6fb5aae9bdcc2c4f3c58cf7a789b15a4daa6617ed594b5ba3951",0))
    print("\n>>---------------------------------------------------------------------")
    print("getTransactionByBlockNumberAndIndex",client.getTransactionByBlockNumberAndIndex(50,0))
    print("\n>>---------------------------------------------------------------------")
    print("getTransactionReceipt",client.getTransactionReceipt("0x41fa9a0ce36d486ee2bf6d2219b68b44ca300ec7aeb07f8f2aa9c225655d2b61"))
    print("\n>>---------------------------------------------------------------------")
    print("getPendingTransactions",client.getPendingTransactions())
    print("\n>>---------------------------------------------------------------------")
    print("getPendingTxSize",client.getPendingTxSize())
    print("\n>>---------------------------------------------------------------------")
    print("getCode",client.getCode("0x83592a3cf1af302612756b8687c8dc7935c0ad1d"))
    print("\n>>---------------------------------------------------------------------")
    print("getTotalTransactionCount",client.getTotalTransactionCount())
    print("\n>>---------------------------------------------------------------------")
    print("getSystemConfigByKey",client.getSystemConfigByKey("tx_count_limit"))
    print("\n>>---------------------------------------------------------------------")

    print("getPbftView",int(client.getPbftView(),16))
    print("\n>>---------------------------------------------------------------------")
    print("getSealerList",client.getSealerList())
    print("\n>>---------------------------------------------------------------------")
    print("getObserverList",client.getObserverList())
    print("\n>>---------------------------------------------------------------------")
    print("getConsensusStatus",client.getConsensusStatus())
    print("\n>>---------------------------------------------------------------------")
    print("getSyncStatus",client.getSyncStatus())
    print("\n>>---------------------------------------------------------------------")
    print("getGroupPeers",client.getGroupPeers())
    print("\n>>---------------------------------------------------------------------")
    print("getNodeIDList",client.getNodeIDList())
    print("\n>>---------------------------------------------------------------------")
    print("getGroupList",client.getGroupList())
