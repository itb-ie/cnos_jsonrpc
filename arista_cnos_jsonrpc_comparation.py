#!/usr/bin/python2.7
import json
import pandas
from devices import *
from jsonrpclib import Server

def add_header(f):
    header = open("header.txt", "r")
    for line in header:
        f.write(line)


def beautify (elem, indent, f):
    f.write(json.dumps(elem, indent=4, sort_keys=True).replace('\n', '<br>').replace(' ', "&nbsp"))

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
writer.save()

f = open("info.html", "w")
add_header(f)
print("Calling beautify!")
for command in output["arista"].keys():
    f.write("<tr style=\"text-align: left;\">\n")
    f.write("<th>")
    f.write(command)
    f.write("</th>\n")
    f.write("<th>")
    beautify(output['arista'][command], indent=0, f=f)
    f.write("</th>\n")
    f.write("<th>")
    beautify(output['cnos'][command], indent=0, f=f)
    f.write("</th>\n")
    f.write("</tr>\n")
f.close()
