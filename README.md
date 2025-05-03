# pygit

commands
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