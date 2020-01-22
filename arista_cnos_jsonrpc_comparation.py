#!/usr/bin/python2.7
import json

import pandas
from jsonrpclib import Server

cnos_url = 'http://10.241.7.145:8080'
arista_url = 'http://admin:admin@192.168.10.3/command-api'

def add_header(f):
    header = open("header.txt", "r")
    for line in header:
        f.write(line)


def beautify (elem, indent, f):
    if isinstance(elem, list):
        f.write("&nbsp"*3*indent + "[<br>\n")
        for i in elem:
            beautify(i, indent+1,f)
        f.write("&nbsp"*3*indent + "]<br>\n")
    elif isinstance(elem, dict):
        f.write("&nbsp"*3*indent + "{<br>\n")
        for k,val in elem.items():
            if not isinstance(val, list) and not isinstance(val, dict):
                f.write("&nbsp"*3*indent + "\""+ k + "\"" + " : " + str(val) + "<br>\n")
            else:
                f.write("&nbsp"*3*indent + "\""+ k + "\"" + " :<br>\n" )
                beautify(val, indent+1, f)

        f.write("&nbsp"*3*indent + "}<br>\n")
    else:
        f.write("&nbsp"*3*indent + str(elem) + "<br>\n")

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
