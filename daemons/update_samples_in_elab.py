from pathlib import Path
import sys
from datetime import datetime
import getpass

def updateSamples( elan, samplenames, key, force, add ):
    elan_samples = elan.get_samples_for_names( samplenames.keys() )
    for sample in elan_samples:
        if not force and not add:
            if next((item for item in sample['meta'] if item['key'] == key and item['value'] != ''), False):
                continue
        meta_fields = elan.get_meta_field_from_sample_type_by_key(sample['sampleType']['sampleTypeID'], key)
        meta_params = {}
        meta_params['key'] = meta_fields[0]['key']
        meta_params['sampleTypeMetaID'] = meta_fields[0]['sampleTypeMetaID']
        meta_params['sampleDataType'] = meta_fields[0]['sampleDataType']
        if add:
            sample_meta_fields = elan.get_sample_meta_fields_by_key(sample['sampleID'], key )
            values = sample_meta_fields[0]['value'].split("\n")
            if samplenames[sample['name']] not in values:
                meta_params['value'] = sample_meta_fields[0]['value'] + "\n" + samplenames[sample['name']]
            else:
                continue
        else:
            meta_params['value'] = samplenames[sample['name']]
        response = elan.put_meta(sample['sampleID'], meta_params)
        if response == 200:
            username = getpass.getuser()
            project_id = next((item['value'] for item in sample['meta'] if item['key'] == 'Project ID'))
            study_name = next((item['value'] for item in sample['meta'] if item['key'] == 'Study Name'))
            print( "".join([str(datetime.now()),"\tUPDATE SAMPLE\tUser=",username,";Sample=", sample['name'], ";Project=", project_id, ";Study=",study_name,";",meta_params['key'],"=",meta_params['value']]) )

def updateSampleWithRawData( elan, raw_data, force, add ):
    samplenames = {}
    for fastq in Path(raw_data).rglob('*.fastq.gz'):
        filename = Path(fastq).name
        samplename = filename.split("_")[0]
        samplenames[samplename] = str(Path(fastq).parent)
    updateSamples( elan, samplenames, "Raw Data", force, add )

def updateSampleWithProcessedData( elan, processed_data, force, add ):
    samplenames = {}
    for bam in Path(processed_data).rglob('*dedup.bam'):
        filename = Path(bam).name
        samplename = filename.split("_")[0]
        samplenames[samplename] = bam
        # str(Path(bam).parent)
    updateSamples( elan, samplenames, "Processed Data", force, add )

def updateSampleWithDataBackup( elan, bam, force, add ):
    samplenames = {}
    filename = Path(bam).name
    samplename = filename.split("_")[0]
    samplenames[samplename] = bam
    # str(Path(bam).parent)
    updateSamples( elan, samplenames, "Data Backup", force, add )

def updateSampleWithDataAnalysis( elan, data_analysis, project_name, study_names, sample_names, force, add ):
    samplenames = {}
    if study_names:
        for study_name in study_names:
            samples = elan.get_samples_by_study_name( study_name )
            for sample in samples:
                samplenames[sample['name']] = data_analysis
    if sample_names:
        for sample_name in sample_names:
            samplenames[sample_name] = data_analysis
    updateSamples( elan, samplenames, "Data Analysis", force, add )

def updateSampleWithSurfdrive( elan, data_analysis, project_name, study_names, sample_names, force, add ):
    samplenames = {}
    if study_names:
        for study_name in study_names:
            samples = elan.get_samples_by_study_name( study_name )
            for sample in samples:
                samplenames[sample['name']] = data_analysis
    if sample_names:
        for sample_name in sample_names:
            samplenames[sample_name] = data_analysis
    updateSamples( elan, samplenames, "Surfdrive", force, add )

def run(elan, args):
    if not ( args.raw or args.processed or args.analysis or args.backup or args.surfdrive):
        sys.exit("No action requested, add --raw, --processed, --analysis, --surfdrive and/or --backup")
    if ((args.analysis or args.surfdrive) and not ( args.project and (args.study or args.sample))):
        sys.exit("No action requested, add --project and --study or --sample together with --analysis and/or --surfdrive")
    if ( args.add and not (args.analysis or args.surfdrive)):
        sys.exit("No action requested, add --analysis and/or --study together with --add")
    if args.raw:
        updateSampleWithRawData( elan, args.raw, args.force, args.add )
    if args.processed:
        updateSampleWithProcessedData( elan, args.processed, args.force, args.add )
    if args.backup:
        updateSampleWithDataBackup( elan, args.backup, args.force, args.add )
    if args.analysis:
        if args.project:
            args.project = ' '.join(args.project)
        if args.study:
            args.study = list( map(lambda x: ' '.join(x), args.study))
        if args.sample:
            args.sample = list( map(lambda x: ' '.join(x), args.sample))
        updateSampleWithDataAnalysis( elan, args.analysis, args.project, args.study, args.sample, args.force, args.add )
    if args.surfdrive:
        if args.project:
            args.project = ' '.join(args.project)
        if args.study:
            args.study = list( map(lambda x: ' '.join(x), args.study))
        if args.sample:
            args.sample = list( map(lambda x: ' '.join(x), args.sample))
        updateSampleWithSurfdrive( elan, args.surfdrive, args.project, args.study, args.sample, args.force, args.add )
