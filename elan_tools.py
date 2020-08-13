import sys
import argparse
import daemons
import requests
from config import elan_key,elan_uri,project_workdir,project_backup,admin_mail
from elan_objects import Elan
#Daemons
def updateSamplesInElab(args):
    daemons.update_samples_in_elab.run( elan, args )

if __name__ == "__main__":

    elan = Elan(elan_uri, elan_key)

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    parser_update = subparser.add_parser('update', help='Update scripts: sample')
    subparser_update = parser_update.add_subparsers()

    parser_update_sample = subparser_update.add_parser('sample', help='Update samples with data information in the elabjournal')
    parser_update_sample.add_argument('--raw', help='Update samples with raw data information')
    parser_update_sample.add_argument('--processed', help='Update samples with processed data information')
    parser_update_sample.add_argument('--backup', help='Update samples with data backup information')
    parser_update_sample.add_argument('--analysis', help='Update samples with data analysis information')
    parser_update_sample.add_argument('--project', nargs='+', help='Update samples within this project with data analysis information')
    parser_update_sample.add_argument('--study', action='append', nargs='+', help='Update samples within this study with data analysis information')
    parser_update_sample.add_argument('--sample', action='append', nargs='+', help='Update samples with this name with data analysis information')
    parser_update_sample.set_defaults(func=updateSamplesInElab)

    args = parser.parse_args()
    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)
