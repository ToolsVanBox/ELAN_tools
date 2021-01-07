from pathlib import Path
import sys
from datetime import datetime
import getpass

def getSampleType( elan, sample_type_name):
    sampleTypeID = elan.get_sampleTypeID( sample_type_name )
    metafields = elan.get_meta_field_from_sample_type( sampleTypeID )
    for metafield in metafields:
        print( metafield )


def run( elan, args):
    if args.name:
        args.name = ' '.join(args.name)
    getSampleType(elan, args.name)
