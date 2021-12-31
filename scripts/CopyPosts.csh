#!/bin/sh

#Posts to Copy over from AutoGen Directory

ROOT_DIR=$1
POST_NAME=$2 

# ROOT_DIR="California-Through-My-Lens"
# POST_NAME="santana-row" 

cp ${TOP_DIR_VAR}/scripts/output/${POST_NAME}.md ${TOP_DIR_VAR}/content/posts/${ROOT_DIR}/${POST_NAME}.md
cp ${TOP_DIR_VAR}/scripts/images/${POST_NAME}.png ${TOP_DIR_VAR}/static/images/sections/posts/${POST_NAME}.png  