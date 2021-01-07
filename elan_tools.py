import sys
import argparse
import daemons
import requests
from config import elan_key,elan_uri
from elan_objects import Elan
#Daemons
def updateSamplesInElab(args):
    daemons.update_samples_in_elab.run( elan, args )

def getStudiesFromElab(args):
    daemons.get_studies_from_elab.run( elan, args )

def getProjectsFromElab(args):
    daemons.get_projects_from_elab.run( elan, args )

def getSampleTypeFromElab(args):
    daemons.get_sampletype_from_elab.run( elan, args )

def updateMetaInElab(args):
    daemons.update_meta_in_elab.run( elan, args )

if __name__ == "__main__":

    elan = Elan(elan_uri, elan_key)

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    parser_update = subparser.add_parser('update', help='Update scripts: sample, meta')
    parser_get = subparser.add_parser('get', help='Get scripts: study, project, sampletype')
    subparser_update = parser_update.add_subparsers()
    subparser_get = parser_get.add_subparsers()

    parser_update_sample = subparser_update.add_parser('sample', help='Update samples with data information in the elabjournal')
    parser_update_sample.add_argument('--raw', help='Update samples with raw data information')
    parser_update_sample.add_argument('--processed', help='Update samples with processed data information')
    parser_update_sample.add_argument('--backup', help='Update samples with data backup information')
    parser_update_sample.add_argument('--analysis', help='Update samples with data analysis information')
    parser_update_sample.add_argument('--surfdrive', help='Update samples with surfdrive information')
    parser_update_sample.add_argument('--project', nargs='+', help='Update samples within this project with data analysis|surfdrive information')
    parser_update_sample.add_argument('--study', action='append', nargs='+', help='Update samples within this study with data analysis and/or surfdrive information')
    parser_update_sample.add_argument('--sample', action='append', nargs='+', help='Update samples with this name with data analysis and/or surfdrive information')
    parser_update_sample.add_argument('--force', action='store_true', help='Forcing sample update, ignore existing sample information')
    parser_update_sample.add_argument('--add', action='store_true', help='Add data analysis and/or surfdrive information to samples')
    parser_update_sample.set_defaults(func=updateSamplesInElab)

    parser_update_meta = subparser_update.add_parser('meta', help='Update sample type meta fieds properties')
    parser_update_meta.add_argument('--sampletype', nargs='+', default='Sample For WGS', help='Updata meta fields for this sample type')
    parser_update_meta.add_argument('--metadata',nargs='+', help='Update sample type meta fields with this metadata file')
    parser_update_meta.set_defaults(func=updateMetaInElab)

    parser_get_study = subparser_get.add_parser('study', help='Get studies from the elabjournal')
    parser_get_study.add_argument('--project', nargs='+', help='Get studies within this project from the elabjournal')
    parser_get_study.set_defaults(func=getStudiesFromElab)

    parser_get_project = subparser_get.add_parser('project', help='Get projects from the elabjournal')
    parser_get_project.set_defaults(func=getProjectsFromElab)

    parser_get_sampletype = subparser_get.add_parser('sampletype', help='Get sampletype from the elabjournal')
    parser_get_sampletype.add_argument('--name', nargs='+', help='Get sampleType with this name from the elabjournal')
    parser_get_sampletype.set_defaults(func=getSampleTypeFromElab)


    args = parser.parse_args()
    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)
