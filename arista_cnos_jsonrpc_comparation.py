#!/usr/bin/python
from jsonrpclib import Server
import json
import pandas

def cmd_run(cnos, arista, output, cmd):
    print "Running \"%s\" command on cnos." %cmd
    cnos_output=cnos.runCmd(cmd)
    print "Running \"%s\" command on arista." %cmd
    arista_output=arista.runCmds(1, ['enable', 'configure terminal', cmd])
    #output[cmd]={}
    #output[cmd]['cnos']=cnos_output
    #output[cmd]['arista']=arista_output
    output['arista'][cmd]=arista_output
    output['cnos'][cmd]=cnos_output

cnos=Server('http://10.241.8.40:8080')
arista=Server('http://admin:admin@192.168.10.2/command-api')

output = {"arista":{},"cnos":{}}

cmd_run(cnos, arista, output, 'show boot')
cmd_run(cnos, arista, output, 'show vlan')
cmd_run(cnos, arista, output, 'vlan 3')
cmd_run(cnos, arista, output, 'show vlan id 3')
cmd_run(cnos, arista, output, 'no vlan 3')


print json.dumps(output, indent=4, sort_keys=True)
f = open("json_rpc.json", 'w')
f.write(json.dumps(output, indent=4, sort_keys=True))
f.close()

df = pandas.DataFrame(output)
writer = pandas.ExcelWriter('test.xlsx')
df.to_excel(writer, sheet_name='Sheet1')
writer.save()

