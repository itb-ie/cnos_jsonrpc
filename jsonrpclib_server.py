#!/usr/bin/python

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import yaml

from jsonrpclib_params_conv import *

import systemApi
import bootinfoApi
import vlanApi


cmd_tree=yaml.safe_load(open('jsonrpclib_handlers.yaml', 'r'))


def get_handler(cmd):
    global cmd_tree
    split_cmd=cmd.split(' ')
    cmd_index=0
    handler=cmd_tree
    for word in split_cmd:
        if word in handler:
            handler = handler[word]
            cmd_index += 1
        else:
            break;
    return (eval(handler["func"]), eval(handler["param"])(split_cmd[cmd_index:]) if handler["param"] else None)

def runCmd(x):
    print "New command: %s" %x
    
    (function, params) = get_handler(x)
    print "Calling function %s(%s)" %(function, params)

    systemApi.client_connect()
    if params:
        response=function(params)
    else:
        response=function()
    systemApi.client_disconnect()

    return response
  

server = SimpleJSONRPCServer(('0.0.0.0', 8080))
server.register_function(pow)
server.register_function(runCmd, 'runCmd')
server.serve_forever()
