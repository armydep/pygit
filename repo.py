class Repository:

    @staticmethod
    def work_dir() -> str:
        return "/tmp/pygit/repo_work_dir_root"

    @staticmethod
    def active_branch() -> str:
        return "active_branch"

    @staticmethod
    def branches() -> str:
        return "branches"

    @staticmethod
    def head() -> str:
        return "HEAD"

    @staticmethod
    def default_branch() -> str:
        return "main"

    @staticmethod
    def index() -> str:
        return "index"

    @staticmethod
    def storage_dir() -> str:
        return ".pygit"

    @staticmethod
    def objects() -> str:
        return "objects"
    
    @staticmethod
    def parent_branch() -> str:
        return "parent_branch"    