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