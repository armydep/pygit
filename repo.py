
class Repository():
    def work_dir(self)-> str:
        return "/tmp/pygit/repo_work_dir_root"
    @staticmethod
    def storage_dir()-> str:
        return ".pygit"    