from pathlib import Path
import sys

def updateSamples( elan, samplenames, key ):
    elan_samples = elan.get_samples_for_names( samplenames.keys() )
    for sample in elan_samples:
        meta_fields = elan.get_meta_field_from_sample_type_by_key(sample['sampleType']['sampleTypeID'], key)
        meta_params = {}
        for m in meta_fields:
            meta_params['key'] = m['key']
            meta_params['sampleTypeMetaID'] = m['sampleTypeMetaID']
            meta_params['sampleDataType'] = m['sampleDataType']
        meta_params['value'] = samplenames[sample['name']]
        elan.put_meta(sample['sampleID'], meta_params)

def updateSampleWithRawData( elan, raw_data ):
    samplenames = {}
    for fastq in Path(raw_data).rglob('*.fastq.gz'):
        filename = Path(fastq).name
        samplename = filename.split("_")[0]
        samplenames[samplename] = str(Path(fastq).parent)
    updateSamples( elan, samplenames, "Raw Data" )

def updateSampleWithProcessedData( elan, processed_data ):
    samplenames = {}
    for bam in Path(processed_data).rglob('*dedup.bam'):
        filename = Path(bam).name
        samplename = filename.split("_")[0]
        samplenames[samplename] = str(Path(bam).parent)
    updateSamples( elan, samplenames, "Processed Data" )

def updateSampleWithDataBackup( elan, data_backup ):
    samplenames = {}
    for bam in Path(data_backup).rglob('*dedup.bam'):
        filename = Path(bam).name
        samplename = filename.split("_")[0]
        samplenames[samplename] = str(Path(bam).parent)
    updateSamples( elan, samplenames, "Data Backup" )

def updateSampleWithDataAnalysis( elan, data_analysis, project_name, study_names, sample_names ):
    samplenames = {}
    if study_names:
        for study_name in study_names:
            samples = elan.get_samples_by_study_name( study_name )
            for sample in samples:
                samplenames[sample['name']] = data_analysis
    if sample_names:
        for sample_name in sample_names:
            samplenames[sample_name] = data_analysis
    updateSamples( elan, samplenames, "Data Analysis" )


def run(elan, args):
    if not ( args.raw or args.processed or args.analysis or args.backup ):
        sys.exit("No action requested, add --raw, --processed, --analysis and/or --backup")
    if (args.analysis and not ( args.project and (args.study or args.sample))):
        sys.exit("No action requested, add --project and --study or --sample together with --analysis")
    if args.raw:
        updateSampleWithRawData( elan, args.raw )
    if args.processed:
        updateSampleWithProcessedData( elan, args.processed )
    if args.backup:
        updateSampleWithDataBackup( elan, args.backup )
    if args.analysis:
        if args.project:
            args.project = ' '.join(args.project)
        if args.study:
            args.study = list( map(lambda x: ' '.join(x), args.study))
        if args.sample:
            args.sample = list( map(lambda x: ' '.join(x), args.sample))
        updateSampleWithDataAnalysis( elan, args.analysis, args.project, args.study, args.sample )
    #updateSample(elan, sample_type_name)
    # buildDirs(elan,project_workdir)
