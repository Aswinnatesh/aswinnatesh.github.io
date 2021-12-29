#Set Paths
TOP_DIR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)

#Set Alias for Scripts
alias newd="python3 ${TOP_DIR}/scripts/CreatePostContainer.py -dir "
alias flickr="python3 ${TOP_DIR}/scripts/flickr.py"