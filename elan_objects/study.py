from elan_objects.entity import Entity
from pathlib import Path
import os

class Study(Entity):
    def __init__(self, data,work_root):
        self.__dict__ = data
        self.work_root = work_root
        self.id = self.studyID
        self.name = self.name.strip().replace('/','-')
        self.name = self.name.strip().replace(' ','_')
    def createDir(self):
        study_dir = super(Study, self).createDir()
        # study_dir.chmod(0o750)
        sub_dirs = ['backup','raw', 'processed', 'analysis']
        for d in sub_dirs:
            new_dir = Path(f'{study_dir}/{d}')
            new_dir.mkdir(exist_ok=True)
            new_dir.chmod(0o770)
            #os.chown(new_dir.resolve(),10619,12964)#sboymans:cuppen

        # backup_dir = Path(f'{study_dir}/backup')
        # raw_dir = Path(f'{study_dir}/raw')
        # processed_dir = Path(f'{study_dir}/processed')
        # analysis_dir = Path(f'{study_dir}/analysis')
        # backup_dir.mkdir(exist_ok=True)
        # raw_dir.mkdir(exist_ok=True)
        # processed_dir.mkdir(exist_ok=True)
        # analysis_dir.mkdir(exist_ok=True)
        # backup_dir.chmod(0o770)
        # raw_dir.chmod(0o770)
        # processed_dir.chmod(0o770)
        # analysis_dir.chmod(0o770)
        # backup_dir
        # raw_dir
        # processed_dir
        # analysis_dir

        return study_dir
# StudyLarge {
# studyStatus (StudyStatus, optional),
# experimentCount (integer, optional),
# meta (Array[StudyMeta], optional),
# studyID (integer, optional),
# projectID (integer, optional),
# groupID (integer, optional),
# subgroupID (integer, optional),
# userID (integer, optional),
# name (string),
# statusChanged (string, optional),
# description (string, optional),
# notes (string, optional),
# approve (string, optional) = ['NOTREQUIRED', 'BYSTUDYMANAGER']stringEnum:"NOTREQUIRED", "BYSTUDYMANAGER",
# created (string, optional),
# deleted (boolean, optional)
# }StudyStatus {
# studyStatusID (integer, optional),
# groupID (integer, optional),
# color (string, optional),
# status (string, optional),
# studyStatusType (string, optional) = ['INIT', 'POSTINIT', 'PENDING', 'PROGRESS', 'OVERDUE', 'OTHER', 'COMPLETED']stringEnum:"INIT", "POSTINIT", "PENDING", "PROGRESS", "OVERDUE", "OTHER", "COMPLETED"
# }
# StudyMeta {
# studyMetaID (integer, optional),
# metaType (string, optional) = ['TEXT', 'FILE']stringEnum:"TEXT", "FILE",
# name (string, optional),
# value (string, optional),
# studyFileID (integer, optional),
# order (integer, optional)
# }
