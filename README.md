# jsonrpc for Lenovo CNOS

## Description
Server-client application fo configuring Lenovo CNOS switches using python jsonrpclib



## Get the sources
	git clone http://10.240.32.214:8080/gabi/cnos_jsonrpclib.git
        or
        git clone git@10.240.32.214:gabi/cnos_jsonrpclib.git

## Dependencies
### Client
jsonrpclib xmlrpclib xlsxwriter lxml openpyxl pandas

### Server
jsonrpclib xmlrpclib

## How to install on the switch:
    scp -r gabi@10.241.7.195:/home/gabi/veos/jsonrpclib_src/jsonrpclib-0.1.7 . 
    scp -r gabi@10.241.7.195:/home/gabi/veos/jsonrpclib_src/xmlrpclib-1.0.1 .
    cd jsonrpclib-0.1.7
    python setup.py install
    cd xmlrpclib-1.0.1
    python setup.py install
    scp -r gabi@10.241.7.195:/usr/lib/python2.7/SimpleXMLRPCServer.py /usr/lib/python2.7/SimpleXMLRPCServer.py
    export PYTHONPATH="/lib/nos_apis:/nosx/script/python_api"
    scp -r gabi@10.241.7.195:/home/gabi/veos/gabi_jsonrpclib_server.py .
    python gabi_jsonrpclib_server.py


