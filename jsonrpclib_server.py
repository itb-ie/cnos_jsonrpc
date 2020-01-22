#!/usr/bin/python

import bgpApi
import systemApi
import yaml
import bootinfoApi
import vlanApi
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from jsonrpclib_params_conv import *

cmd_tree = yaml.safe_load(open('jsonrpclib_handlers.yaml', 'r'))

def show_ip_bgp_neighbors():
    peers = bgpApi.BGP().python_show_ip_bgp_neighbors()
    json_peers = []
    for p in peers:
        json_peers.append(dict(p))
    return {"peerList": json_peers}

class LenovoJSONRPCServer():
    def __init__(self):
        self.state = 0

    def got_to_enable(self):
        self.state = 1

    def go_to_conf(self):
        self.state = 2

    def get_handler(self, cmd):
        global cmd_tree
        split_cmd = cmd.lstrip().split(' ')
        print split_cmd
        cmd_index = 0
        handler = cmd_tree
        for word in split_cmd:
            print word
            if word in handler:
                handler = handler[word]
                cmd_index += 1
            else:
                break;
        return eval(handler["func"]), eval(handler["param"])(split_cmd[cmd_index:]) if handler.get("param") else None

    def exec_cmd(self, cmd):
        (function, params) = self.get_handler(cmd)
        print "Calling function %s(%s)" % (function, params)

        if params:
            response = function(params)
        else:
            response = function()

        if type(response) is list:
            return response
        return {}

def run_cmd(x):
    global cmd_tree
    print cmd_tree
    print "New command: %s" % x
    tranz = LenovoJSONRPCServer()

    systemApi.client_connect()
    resp = []

    for cmd in x:
        resp.append(tranz.exec_cmd(cmd))

    systemApi.client_disconnect()

    return resp


server = SimpleJSONRPCServer(('0.0.0.0', 8080))
server.register_function(pow)
server.register_function(run_cmd, 'runCmds')
server.serve_forever()
