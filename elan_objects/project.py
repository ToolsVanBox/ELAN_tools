from elan_objects.entity import Entity
# from pathlib import Path

class Project(Entity):

    def __init__(self, data, work_root):
        self.__dict__ = data
        self.work_root = work_root
        self.id = self.projectID
        self.name = self.name.strip().replace('/','-')
        self.name = self.name.strip().replace(' ','_')

    def createDir(self):
        project_dir = super(Project, self).createDir()
        project_dir.chmod(0o750)

        return project_dir

# ProjectLarge {
# groupName (string, optional),
# numStudies (integer, optional),
# projectID (integer, optional),
# groupID (integer, optional),
# userID (integer, optional),
# creatorID (integer, optional),
# name (string),
# longName (string, optional),
# description (string, optional),
# notes (string, optional),
# created (string, optional),
# active (boolean, optional),
# deleted (boolean, optional)
# }
