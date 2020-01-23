#!/usr/bin/python2.7
import json
import pandas
from devices import *
from jsonrpclib import Server

def beautify (output, f):

    def add_header(f):
        header = open("header.txt", "r")
        for line in header:
            f.write(line)

    add_header(f)
    f.write("<tbody>\n")
    for i in range(len(output["arista"])):
        command = list(output["arista"][i].keys())[0]
        f.write("<tr style=\"text-align: left;\">\n")
        f.write("<th>")
        f.write(command)
        f.write("</th>\n")
        f.write("<td>")
        f.write(json.dumps(output['arista'][i][command], indent=4, sort_keys=True).replace('\n', '<br>').replace(' ', "&nbsp"))
        f.write("</td>\n")
        f.write("<td>")
        f.write(json.dumps(output['cnos'][i][command], indent=4, sort_keys=True).replace('\n', '<br>').replace(' ', "&nbsp"))
        f.write("</td>\n")
        f.write("</tr>\n")
    f.write("</tbody>\n")
    f.write("</table>\n")


def cmd_run(cnos, arista, output, cmd):
    print "Running \"%s\" command on cnos." % cmd
    cnos_output = cnos.runCmds(cmd)
    print "Running \"%s\" command on arista." % cmd
    arista_output = arista.runCmds(1, cmd)
    output['arista'].append({str(cmd) : arista_output})
    output['cnos'].append({str(cmd) : cnos_output})


cnos = Server(cnos_url)
arista = Server(arista_url)

#changed to list so that the order of command lines stays the same when printing
output = {"arista": [], "cnos": []}

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
beautify(output, f)
f.close()
