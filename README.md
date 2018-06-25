This should work with stqandard Python libraries. You will need to enable SNMP on the Cisco ASA

USAGE
=====

        usage: asausers.py [-h] -f FIREWALL [-i IGNORE] -c COMMUNITY_STRING
                           [-o OUTPUT]

        Get connected users from ASA via SNMP

        optional arguments:
          -h, --help            show this help message and exit
          -f FIREWALL, --firewall FIREWALL
                                Address of the Cisco ASA
          -i IGNORE, --ignore IGNORE
                                Comma separated list of IP addresses to ignore
          -c COMMUNITY_STRING, --community_string COMMUNITY_STRING
                                SNMP community string
          -o OUTPUT, --output OUTPUT
                                Output type, option are json and text. Defaults to json'


OUTPUTS
========

Default output - json format:

{'users': {'user1': {'Private IP': '10.12.13.14', 'Public IP': '100.100.100.101'}, 'user2': {'Private IP': '10.12.13.15', 'Public IP': '100.100.100.102'}}}

Text output format:

users:
  user1:
    Private IP: 10.12.13.14
    Public IP: 100.100.100.101
  user2:
    Private IP: 10.12.13.15
    Public IP: 100.100.100.102
  user3:
    Private IP: 10.12.13.16
    Public IP: 50.50.40.90
