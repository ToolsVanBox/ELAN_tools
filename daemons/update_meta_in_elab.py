from pathlib import Path
import sys
from datetime import datetime
import getpass

def updateMetaField( elan, sample_type_name, metadata):
    sampleTypeID = elan.get_sampleTypeID( sample_type_name )
    with open( metadata ) as f:
        for line in f:
            line = line.rstrip()
            metafield_name, optionvalue = line.split("\t")
            metafield = elan.get_meta_field_from_sample_type_by_key( sampleTypeID, metafield_name )
            sampleTypeMetaID = metafield[0]['sampleTypeMetaID']
            meta_params = {'sampleDataType': "COMBO"}
            meta_params['optionValues'] = metafield[0]['optionValues']
            if optionvalue not in meta_params['optionValues']:
                meta_params['optionValues'].append(optionvalue)

            if metafield[0]['notes'] == ' ':
                meta_params['notes'] = ''
            else:
                meta_params['notes'] = ' '
            elan.patch_meta( sampleTypeID, sampleTypeMetaID, meta_params)

def run(elan, args):
    if not ( args.sampletype and args.metadata):
        sys.exit("No action requested, add --sampletype and --metadata")
    if type(args.sampletype) is list:
        args.sampletype = ' '.join(args.sampletype)
    args.metadata = ' '.join(args.metadata)
    updateMetaField(elan, args.sampletype, args.metadata)
