#!/usr/bin/env python
import argparse
import commands
import json
import time
import yaml

class ASAVpn():
    def __init__(self, firewall, ignore_list, community_string):
        self.firewall = firewall
        self.ignore_list = ignore_list
        self.cmd = 'snmpwalk -v1 -c%s %s 1.3.6.1.4.1.9.9.392.1.3.21.1.8' % (community_string, firewall)
        self.cmd1 = 'snmpwalk -v1 -c%s %s 1.3.6.1.4.1.9.9.392.1.3.21.1.10' % (community_string, firewall)

    def get_connected_users(self):
        output = commands.getoutput(self.cmd)
        output1 = commands.getoutput(self.cmd1)
        output = self._commands_output_to_list(output)
	output1 = self._commands_output_to_list(output1)
        output = self._get_ascii_codes(output, 8)
	output1 = self._get_ascii_codes(output1, 10)
        output = self._ascii_string_to_int(output)
	output1 = self._ascii_string_to_int(output1)
        output = self._convert_ascii_code_to_text(output)
	output1 = self._convert_ascii_code_to_text(output1)
        output = self._strip_ip_element(output)
	output1 = self._strip_ip_element(output1)
        output = self._remove_ignore_list(output)
	output1 = self._remove_ignore_list(output1)
        output = self._convert_to_json(output, output1)
        return output

    def _hasNumbers(self, inputString):
        return any(char.isdigit() for char in inputString)


    def _commands_output_to_list(self, output):
        """Take snmpwalk command output and turn it to a list
        based on \n and =  so format [[oid, result]]"""
        output = [x.split('=') for x in output.split('\n')]
	return output


    def _get_ascii_codes(self, output, oid):
        """Strip SNMP stuff from the oid, including whitespace
        and the first and last element of the list. This give us a
        list like this: ['105 97 110', ' STRING: "31.23.24.56"'] """
        if oid == 8:
		string_to_remove = 'SNMPv2-SMI::enterprises.9.9.392.1.3.21.1.8.'
        else:
		string_to_remove = 'SNMPv2-SMI::enterprises.9.9.392.1.3.21.1.10.'
	output = [[x[0].replace(string_to_remove,'').strip(' '), x[1]] for x in output]
        output = [[' '.join(x[0].split('.')[1:-1]), x[1]] for x in output if self._hasNumbers(x[1])]
        return output


    def _ascii_string_to_int(self, output):
        """turn the first element of ['105 97 110', ' STRING: "31.23.24.56"']
        into a list of integers: [[105 97 110], ' STRING: "31.23.24.56"']"""
        new = list()
        for x in output:
            split = x[0].split()
            to_int = [int(y) for y in split]
            new.append([to_int, x[1]])
        return new


    def _convert_ascii_code_to_text(self, output):
        """Now lets convert our ascii codes to a text name
        and return a new list object ['username': ' STRING: "31.23.24.56"']"""
        new = list()
        for x in output:
            username_as_ascii = x[0]
            username_as_text = ''.join(chr(i) for i in username_as_ascii)
            new.append([username_as_text, x[1]])
        return new


    def _strip_ip_element(self, output):
        """Clean up the second element and remove extraneous " and
        ' STRING: '"""
        return [[x[0], x[1].strip(' STRING: ').replace('"','')] for x in output]


    def _remove_ignore_list(self, output):
        """return us only VPN users and not the ignore list"""
        new = list()
        for x in output:
            if not x[0] in self.ignore_list:
                new.append(x)
        return new


    def _convert_to_json(self, output, output1):
	outputdict = dict(output)
	outputdict1 = dict(output1)
	combinedoutput = [(k, outputdict[k], outputdict1[k]) for k in sorted(outputdict)]

	out = {'users' : dict()}
        for i in combinedoutput:
            out['users'].update({i[0]:{'Private IP':i[1],'Public IP':i[2]}})
        return out


def parse_args():
    parser = argparse.ArgumentParser(description='Get connected users from ASA via SNMP')
    parser.add_argument('-f', '--firewall', action='store', required=True, help='Address of the Cisco ASA')
    parser.add_argument('-i', '--ignore', action='store', default='', help='Comma separated list of IP addresses to ignore')
    parser.add_argument('-c', '--community_string', action='store', required=True, help='SNMP community string')
    parser.add_argument('-o', '--output', action='store', default='json', help='Output type, option are json and text. Defaults to json')
    return parser.parse_args()

args = parse_args()


def main():
    asa = ASAVpn(args.firewall, args.ignore, args.community_string)
    users = asa.get_connected_users()
    if args.output == 'text':
	print yaml.dump(users, default_flow_style=False)
	"""print json.dumps(users, indent=5)
	for index, value in enumerate(users):
		print (index, value, users[value])
        for i in users['users']:
            print ('%s, %s, %s' % (i, users['users'][i]['Private IP']['Public IP']))"""
    else:
        print (users)


if __name__ == "__main__":
    main()
