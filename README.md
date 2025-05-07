# pygit
create executable:
- 
```bash
pyinstaller --onefile pygit.py
```
it will create executable in dist directory.
then run with 'dist/pygit ...'

optional: add dir to $PATH
```bash
mkdir -p ~/bin
cp dist/hello ~/bin/
export PATH="$HOME/bin:$PATH"
source ~/.bashrc
pygit
```

add linter:
```bash
pip install flake8
flake8 .
```
add type hinst:
```bash
pip install mypy
mypy .
```

commands:
1. init
    pre-condition 
        there is no .pygit
    post-condition
        there is a .pygit     
   create 
   .storage 
        index
        objects?
        branches        
            branch1
                commites
                    commit1
                    commit2
            branch2
        set default branch
            
2. status
    pre-condition
        there is a .pygit
    post-condition
        no changes
3. add <file>
    pre-condition
        there is a .pygit
        the <file> exists in work dir
        the <file> is not in index
        the <file> is not in objects
    post-condition
        there is a .pygit
        the <file> is not in index
        the <file> is not in objects
4. branch
    pre-condition
        there is a .pygit
    post-condition
        no changes
5. commit
    pre-condition
        there is a .pygit
        there is a comment
        there is a file in index
        there is a file in objects
    post-condition
        
6. checkout <branch> <>
7. 

next:
    commit
    reset --HEAD / unstage / untrack 
    /restore? --staged <file> /revert?

next:
    should commit command check and say if there are unstaged changes?
    update git status command 
    add comment to commit    

to refactor:
    # replace by target.equals to index. in add.py:40
    check how index entries equals / diff in add/commit commands. is it ok to compare by mod_time. for just pulled repository/commit. what about sha1 and file size 

global:
    commit dir name - timestamp? hash?    

next:
    support "add ."
    support "status"     
    refactor: remove single line functions from file_util
    move some methods into commands.base class

next:
    same routine for 'status' command and 'add .'
    code review ai
    fix exe
    fix project path
    add exclude .git / .pygit in work dir - validation
    fix logs

next:
    merge
    cherry-pick
    reset head
    change home_dir path
    tests
    storage hosting server
    objects structure 

- flatten head commit
```bash
git ls-tree -r HEAD
100644 blob 8baef1b4abc478178b004d62031cf7fe6db6f903	bbb.txt
100644 blob 7fd09feec7c0f3ec48a758e9b14c1597e6c19401	myp1/m.txt
100644 blob 9b6eaba6b4c8440e39a39db36de19f08c0a7f7e3	myp1/m2.txt
100644 blob 1a52584b7fb352fc19c3b1937cddc22015308c38	sec.txt
```
- show index file:
```bash
git ls-files --stage
100644 8baef1b4abc478178b004d62031cf7fe6db6f903 0	bbb.txt
100644 7fd09feec7c0f3ec48a758e9b14c1597e6c19401 0	myp1/m.txt
100644 9b6eaba6b4c8440e39a39db36de19f08c0a7f7e3 0	myp1/m2.txt
100644 1a52584b7fb352fc19c3b1937cddc22015308c38 0	sec.txt
```

- commit object:
```bash
git cat-file -p c78d5cd435a97cf00939c453a500c3b3712b7616

tree b2a6bc2d5b6175ca82adbce1eea8a0df4fd12b14
parent cf53306bf948ebc45fa114bc3cfbccae8a9cecc6
author Arkady <orkasha@gmail.com> 1746481341 +0300
committer Arkady <orkasha@gmail.com> 1746481341 +0300

swtich fixed
```

- tree object:
```bash
git cat-file -p 07fbb54a88b2d5297ebbd4609eb9f748bd838208

100644 blob 8baef1b4abc478178b004d62031cf7fe6db6f903	bbb.txt
040000 tree e183545695a5d1e4fdc4f3a9a9c78eca572a95c2	myp1
100644 blob 1a52584b7fb352fc19c3b1937cddc22015308c38	sec.txt
```

