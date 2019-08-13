#!/usr/bin/env python3
__author__ = 'Christoffer Claesson (Christoffer.Claesson@Securitybits.io)'
__copyright__ = 'Copyright (c) 2019 Christoffer Claesson'
__license__ = 'GNU General Public Liscence v3.0'
__vcs_id__ = '$Id$'
__version__ = '0.1' #Versioning: http://www.python.org/dev/peps/pep-0386/

#Statics
prog_desc = '''
CLI Client to help administration of hashlists and jobs in hashtopolis
'''

#TODO: Hash identifier

#TODO: list jobs
#TODO: list hashlists
#TODO: list agents
#TODO: list cracked

#TODO: parse Hashes

import sys
import argparse
import lib.config as config
import lib.check as check
import lib.search as search
import lib.list as list

def main():
    parser = argparse.ArgumentParser(prog='hashpuppy', description=prog_desc)

    parser.add_argument('--version', action='version',
                    version='%(prog)s {version}'.format(version=__version__))

    subparsers = parser.add_subparsers(dest='command',
                                       title='Arguments',
                                       description='List of sub arguments to pass to hashpuppy',
                                       help='sub-command help')

    parser_check = subparsers.add_parser('check',
                                       help='Check the connection to server and api.conf')

    parser_search = subparsers.add_parser('search', help='Search for cracked hash in database')
    parser_search.add_argument('HASH', help='single hash to search for cracked password')

    parser_list = subparsers.add_parser('list', help='Subsection for listing various things')
    parser_list.add_argument('CMD', help='list [jobs, cracked, agents, hashlists]')

    args = parser.parse_args()

    if args.command == 'check':
        if (check.Auth(config.url, config.token)) == True:
            print('Authentication Complete')
        else:
            sys.exit()
    elif args.command == 'search':
        if (check.Auth(config.url, config.token)) == True:
            search.search(config.url, config.token, args.HASH)
        else:
            sys.exit()
    elif args.command == 'list':
        if (check.Auth(config.url, config.token)) == True:
            if (args.CMD == 'cracked'):
                list.print_cracked(config.url, config.token)
            elif (args.CMD == 'jobs'):
                print('list jobs')
            elif (args.CMD == 'agents'):
                print('list agents')
            elif (args.CMD == 'hashlists'):
                list.print_hashlists(config.url, config.token)
            elif (args.CMD == 'wordlists'):
                print('list wordlists')

        else:
            sys.exit()

    else:
        return
    return

if __name__ == "__main__":
    main()
