# git checkout master
cd bootstrap
grunt dist
cp dist/css/bootstrap.min.css ../../simorgh/static/css
cd ..
cp dist/css/bootstrap-rtl.min.css ../simorgh/static/css


