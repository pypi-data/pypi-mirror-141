# freehub
With one command, upload file to freehub , or download from freehub. Easy to use.

# install
```shell script
pip3 install freehub
``` 

# usage
```shell script
#upload
freehub upload path(can be file or directory) [key](key is optional,by default is the same as path)
 
#upload file
freehub upload a.jpg a 
#upload directory
freehub upload demo demo

# download
freehub download key(the key you use for uploading) [path](optional, default value: "./")

# download file
freehub download a ./downloads
# download directory
freehub download demo ./downloads
```

# roadmap
[] support for custom repository, e.g. `freehub set-repo gitee.com/Peiiii`
[] wrap it as a script repository, text store, json store , or database?.
[] support for running script by specifying script location, e.g. `freehub run OpenGitspace/meta/b`, `freehub pyrun OpenGitspace/c/d`
[] note-taking app building upon freehub
[] cloud functions