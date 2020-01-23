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
        global cmd_tree
        print
        self.state = []
        systemApi.client_connect()

    def __del__(self):
        systemApi.client_disconnect()

    def pop(self):
        if len(self.state) > 0:
            self.state.pop()

    def go_to_enable(self):
        self.state.append('enable')

    def go_to_conf(self):
        self.state.append('configure')
        self.state.append('terminal')

    def go_to_vlan(self, vlan):
        self.state.append({'vlan':vlan})

    def go_to_bgp(self, bgp):
        self.state.append({'router bgp': bgp})

    def get_handler(self, cmd):
        if cmd == 'exit':
            self.pop()
            return None, None, None
        global cmd_tree
        split_cmd = cmd.lstrip().split(' ')
        cmd_index = 0
        handler = cmd_tree
        for state in self.state:
            if isinstance(state, str):
                handler = handler[state]
            if isinstance(state, dict):
                handler = handler[list(state)[0]]
        for word in split_cmd:
            if word in handler:
                handler = handler[word]
                cmd_index += 1
            else:
                break;
        print handler
        func = eval(handler["func"]) if handler.get("func") else None
        params = eval(handler["param"])(split_cmd[cmd_index:]) if handler.get("param") else split_cmd[cmd_index:]
        tranz = eval('self.'+ handler['tranz']) if handler.get("tranz") else None
        return func, params, tranz

    def exec_cmd(self, cmd):
        print "\n\nExecuting: %s" % cmd
        (function, params, tranz) = self.get_handler(cmd)
        print "State: %s" %self.state

        response = {}

        if function:
            print "Calling function %s(%s)" % (function, params)
            if params:
                if isinstance(params, tuple):
                    resp = function(*params)
                else:
                    resp = function(params)
            else:
                resp = function()
            if isinstance(resp, list) or isinstance(resp, dict):
                response = resp

        if tranz:
            print "Tranz: %s" %tranz
            if params:
                tranz(params)
            else:
                tranz()

        return response

    def vlan_name(self, x):
        vlan_id = self.state[-1]['vlan']['vlan_id']
        name = str(x[0])
        return vlan_id, name
    def name(self, name):
        if len(self.state) == 0:
            raise Exception("Command not allowed")
        last_state = self.state[-1]
        if isinstance(last_state, dict):
            if 'vlan' in last_state:
                vlanApi.VlanSystem().python_update_vlan_name(last_state['vlan'], str(name[0]))
                return
        raise Exception("Command not allowed")

    def vlan(self, id):
        vlanApi.VlanSystem().python_create_vlan(one_param_to_vlan_dict(id))
        self.state.append({'vlan':int(id[0])})

def run_cmd(x):
    print "\n\n___________________"
    print "New command: %s" % x

    tranz = LenovoJSONRPCServer()
    resp = []
    for cmd in x:
        resp.append(tranz.exec_cmd(cmd))

    return resp


server = SimpleJSONRPCServer(('0.0.0.0', 8080))
server.register_function(pow)
server.register_function(run_cmd, 'runCmds')
server.serve_forever()
