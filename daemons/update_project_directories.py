from pathlib import Path

def buildDirs(elan,project_workdir):
    projects = elan.get_projects(project_workdir)
    for p in projects:
        project_dir = p.createDir()
        studies = elan.get_studies(project_dir, project_id=p.projectID)

        for s in studies:
            study_dir = s.createDir()



def run(elan,project_workdir):
    buildDirs(elan,project_workdir)
