#!/usr/bin/python2.7
import json

import pandas
from jsonrpclib import Server

cnos_url = 'http://10.241.8.40:8080'
arista_url = 'http://admin:admin@192.168.10.2/command-api'


def cmd_run(cnos, arista, output, cmd):
    print "Running \"%s\" command on cnos." % cmd
    cnos_output = cnos.runCmds(cmd)
    print "Running \"%s\" command on arista." % cmd
    arista_output = arista.runCmds(1, cmd)
    # output[cmd]={}
    # output[cmd]['cnos']=cnos_output
    # output[cmd]['arista']=arista_output
    output['arista'][str(cmd)] = arista_output
    output['cnos'][str(cmd)] = cnos_output


cnos = Server(cnos_url)
arista = Server(arista_url)

output = {"arista": {}, "cnos": {}}

with open('command_list.txt', 'r') as cmd_file:
    for line in cmd_file:
        cmd = line.rstrip()
        if len(cmd) < 1 or cmd.startswith('#'):
            continue
        if cmd.startswith('['):
            cmd = eval(cmd)
        else:
            cmd = [cmd]
        print '%s %s' %(type(cmd), cmd)
        cmd_run(cnos, arista, output, cmd)

print json.dumps(output, indent=4, sort_keys=True)
f = open("json_rpc.json", 'w')
f.write(json.dumps(output, indent=4, sort_keys=True))
f.close()

df = pandas.DataFrame(output)
writer = pandas.ExcelWriter('test.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')

# wrap_format = writer.book.add_format({'text_wrap': True})

# worksheet = writer.sheets['Sheet1']
# worksheet.add_table('E10:G12', {'data':[['A', 10], ['B', 11]]})


# worksheet.set_column('B:B', 100, wrap_format)
# worksheet.set_column('B:B', None, wrap_format)
# worksheet.set_column('C:C', None, wrap_format)

writer.save()
