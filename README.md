# ELAN_tools
Utility scripts for updating the elabjournal


# How to run

## Virtual environment

### Create new venv
If you need to create a new virtual environment
```
> virtualenv venv_3.6 -p /hpc/local/CentOS7/common/lang/python/3.6.1/bin/python
```

### Load venv
Before you run ELAN_tools, you need load the virtual environment
```
> . /hpc/pmc_vanboxtel/tools/ELAN_tools/venv_3.6/bin/activate
```

### Install python modules
If you created a new virtual environment, install the required modules
```
> pip install -r requirements.txt
```

## Run ELAN_tools
Run ELAN_tools
```
> python elan_tools.py update sample

```
### Add raw data information
It looks recursively for *.fastq.gz files in the given folder. It will extract the sample name ( everything before the first "_" in the filename ).
For each sample with this sample name in ELAB, the `Raw Data` field will be updated by this folder.
```
>  python elan_tools.py update sample --raw /path/to/raw_data/run

```
### Add processed data information
It looks recursively for *.dedup.bam files in the given folder. It will extract the sample name ( everything before the first "_" in the filename ).
For each sample with this sample name in ELAB, the `Processed Data` field will be updated by this folder.
```
>  python elan_tools.py update sample --processed /path/to/processed/run

```
### Add data backup information
It looks recursively for *.dedup.bam files in the given folder. It will extract the sample name ( everything before the first "_" in the filename ).
For each sample with this sample name in ELAB, the `Data Backup` field will be updated by this folder.
```
>  python elan_tools.py update sample --backup /path/to/backup/run

```
### Add data analysis information
For each sample within the study name or with this sample name in ELAB, the `Data Analysis` field will be updated by this folder. 
Note; Study and/or sample can be used multiple times.
```
>  python elan_tools.py update sample --analysis /path/to/analysis/run --project <PROJECT_NAME> ( --study <STUDY_NAME> or --sample <SAMPLE_NAME> ) 

```
### Add surfdrive information
For each sample within the study name or with this sample name in ELAB, the `Surfdrive` field will be updated by this folder. 
Note; Study and/or sample can be used multiple times.
```
>  python elan_tools.py update sample --surfdrive ~/surfdrive/path/to/folder --project <PROJECT_NAME> ( --study <STUDY_NAME> or --sample <SAMPLE_NAME> ) 

```
## Cronjob
Examples of different cronjobs:
Create/edit (your) crontab file
```
crontab -e
```
### Raw data
Check every day at 0:00 (`0 0 * * *`) in the raw data folder
```
0 0 * * * . /hpc/pmc_vanboxtel/tools/ELAN_tools/venv_3.6/bin/activate && python /hpc/pmc_vanboxtel/tools/ELAN_tools/elan_tools.py update sample --raw /hpc/pmc_vanboxtel/raw_data --force >> /hpc/pmc_vanboxtel/raw_data/elan_tools.log
```

### Processed data
Check every day at 0:00 (`0 0 * * *`)  in the processed folder for a mapping folder less than a day old (`-mtime -1`)
```
0 0 * * * find /hpc/pmc_vanboxtel/processed/ -type d -mtime -1 -name "mapping" | xargs -I {} sh -c ". /hpc/pmc_vanboxtel/tools/ELAN_tools/venv_3.6/bin/activate && python /hpc/pmc_vanboxtel/tools/ELAN_tools/elan_tools.py update sample --processed {} --force >> /hpc/pmc_vanboxtel/processed/elan_tools.log"
```

### Data backup
Check every day at 0:00 (`0 0 * * *`)  in the backup folder for a mapping folder less than a day old (`-mtime -1`)
```
0 0 * * * find /data/isi/p/pmc_research/pmc_vanboxtel/general/bams/ -type d -mtime -1 -name "mapping" | xargs -I {} sh -c ". /hpc/pmc_vanboxtel/tools/ELAN_tools/venv_3.6/bin/activate && python /hpc/pmc_vanboxtel/tools/ELAN_tools/elan_tools.py update sample --backup {} --force >> /data/isi/p/pmc_research/pmc_vanboxtel/general/bams/elan_tools.log"
```
