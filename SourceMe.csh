#!/bin/sh

#Set Paths
TOP_DIR_VAR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
export TOP_DIR TOP_DIR_VAR

#Set Alias for Scripts
alias newd="python3 ${TOP_DIR_VAR}/scripts/CreatePostContainer.py -dir "
alias flickr="python3 ${TOP_DIR_VAR}/scripts/flickr.py"
alias posts="cd ${TOP_DIR_VAR}/content/posts; pwd"
alias copy="/bin/sh ${TOP_DIR_VAR}/scripts/CopyPosts.csh"