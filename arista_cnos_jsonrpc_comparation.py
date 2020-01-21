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

with open('command_list.txt', 'r') as cmd_file:
    for line in cmd_file:
        cmd_run(cnos, arista, output, line.rstrip())

print json.dumps(output, indent=4, sort_keys=True)
f = open("json_rpc.json", 'w')
f.write(json.dumps(output, indent=4, sort_keys=True))
f.close()

df = pandas.DataFrame(output)
writer = pandas.ExcelWriter('test.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')

#wrap_format = writer.book.add_format({'text_wrap': True})

#worksheet = writer.sheets['Sheet1']
#worksheet.add_table('E10:G12', {'data':[['A', 10], ['B', 11]]})


#worksheet.set_column('B:B', 100, wrap_format)
#worksheet.set_column('B:B', None, wrap_format)
#worksheet.set_column('C:C', None, wrap_format)

writer.save()
