from pathlib import Path
import os

class Entity(object):
    def __init__(self, data, work_root):
        self.__dict__ = data
        self.work_root = None
        self.id = None
        self.name = None
        self.work_dir = None

    def createDir(self):
        existing_dir = self._getDir()
        current_dir = Path(f'{self.work_root}/{self.name}')
        id_file = Path(f'{self.work_root}/{self.name}/.ID-{self.id}')
        self.work_dir = current_dir
        if not existing_dir :
            current_dir.mkdir(exist_ok=True)
            current_dir.chmod(0o750)
            #os.chown(current_dir.resolve(),10619,12964) #sboymans:cuppen
            id_file.touch()
            id_file.chmod(0o700)
            #os.chown(id_file.resolve(),10619,12964) #sboymans:cuppen
        elif existing_dir != current_dir:
            existing_dir.rename(current_dir)

        return current_dir

    def _getDir(self):
        #print("_GETDIR")
        p = Path(self.work_root)
        for d in p.iterdir():
            id_file = Path(f'{d}/.ID-{self.id}')
            if id_file.exists(): return d
            # (id,name) = d.name.split(':',1)
            # if int(id) == int(self.id): return d
        return None
