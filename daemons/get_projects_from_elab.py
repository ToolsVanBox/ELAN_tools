from pathlib import Path
import sys
from datetime import datetime
import getpass

def getProjects( elan):
    projects = elan.get_projects( )
    for project in projects:
        print( project['name'] )


def run( elan, args):
    getProjects(elan)
