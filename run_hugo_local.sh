#RUN PYTHON SCRIPTS FOR FLICKR - TRAVEL PAGE
cd script/travelogue/automa; python3 flickr.py; cd -;

#GENERATE HTML PAGES BY HUGO
cd script/homepage; hugo; cd -;
cd script/myresume; hugo; cd -;
cd script/travelogue; hugo; cd -;

#CLEAR AND COPY OVER GENERATED HTML CONTENT
cp -rf script/homepage/public/* .; rm -rf script/homepage/public/*;
rm -rf ./resume/*;  cp -rf script/myresume/public/* ./resume; rm -rf script/myresume/public/*
rm -rf ./travel/*; cp -rf script/travelogue/public/* ./travel; rm -rf script/travelogue/public/*

echo [INFO] All Task Done