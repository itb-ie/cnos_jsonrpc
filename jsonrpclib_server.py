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
        self.state = []

    def go_to_enable(self):
        self.state.append('enable')

    def go_to_conf(self):
        self.state.append('configure terminal')

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
        return eval(handler["func"]), eval(handler["param"])(split_cmd[cmd_index:]) if handler.get("param") else split_cmd[cmd_index:]

    def exec_cmd(self, cmd):
        (function, params) = self.get_handler(cmd)
        print "Calling function %s(%s)" % (function, params)

        if params:
            response = function(params)
        else:
            response = function()

        print "state = %s" %self.state

        if isinstance(response, list) or isinstance(response, dict):
            return response
        return {}

    def name(self, name):
        print "____NAME___%s %s" %(type(name), name)

    def vlan(self, id):
        print "*****id=%s" %id
        print id[0]
        print int(id[0])
        print vlanApi.VlanSystem().python_create_vlan(one_param_to_vlan_dict(id))
        self.state.append({'vlan':id[0]})

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
