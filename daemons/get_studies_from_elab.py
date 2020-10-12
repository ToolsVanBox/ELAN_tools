from pathlib import Path
import sys
from datetime import datetime
import getpass

def getStudies( elan, project_name):
    if project_name:
        project_id = elan.get_project_id( project_name )
        studies = elan.get_studies( project_id)
    else:
        studies = elan.get_studies( )
    for study in studies:
        print( study )
        print( study['name'] )


def run( elan, args):
    if args.project:
        args.project = ' '.join(args.project)
    getStudies(elan, args.project)
