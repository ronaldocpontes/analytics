#### DEPENDENCIES ###
# - XCode
# - HomeBrew

echo "Installing python"
brew install python
brew install pip

brew tap samueljohn/python
brew tap homebrew/science

echo "virtualenv"
pip install virtualenv
pip install nose

echo "Installing gfortran"
brew install gfortran

echo "Installing numpy, scipy"
brew install numpy
brew install scipy

echo "Installing matplotlib"
pip install pyparsing
pip install python-dateutil
brew install matplotlib

echo "Create QSTK directory"
mkdir ~/QSTK
cd ~/QSTK
# virtualenv env --distribute --system-site-packages
# source ~/QSTK/env/bin/activate


echo "Install pandas, scikits"
pip install pandas
pip install scikits.statsmodels
pip install scikit-learn
pip install QSTK

echo "Install Optional Dependencies"

echo "Install Excel Optional Dependencies"

#pip install xlrd
#pip install xlrd
#pip install openpyxl
#pip install XlsxWriter
