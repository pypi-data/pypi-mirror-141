pip uninstall conquest -y
rm dist/*
python setup.py sdist
python setup.py install
tox 
