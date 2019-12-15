

INCLUDE_CONSTANTS="true"
INCLUDE_SETUP_CONSTANTS="true"
INCLUDE_UTIL_FUNCTIONS="true"
INCLUDE_SETUP_FUNCTIONS="true"

source include/constants.sh
source include/constants_setup.sh
source include/functions_utility.sh
source include/functions_setup.sh


display_script_header
display_script_info
check_environment

cd ..

print "Removing existing virtual environment, if it exists." $SKIP_NEW_LINE
if [ $? -eq 0 ] && ( rm -rf $VENV_DIR ); then print "${TEXT_GREEN}[OK]"; else print "${TEXT_RED}[FAILED]"; fi

print "Creating new virtual environment at ${TEXT_BLUE}$(pwd)/${VENV_DIR}" $SKIP_NEW_LINE
if [ $? -eq 0 ] && ( python3 -m venv $VENV_DIR ); then print "${TEXT_GREEN}[OK]"; else print "${TEXT_RED}[FAILED]"; fi

print "Activating virtual environment..." $SKIP_NEW_LINE
activate_virtual_environment
if [ $? -eq 0 ]; then print "${TEXT_GREEN}[OK]"; else print "${TEXT_RED}[FAILED]"; fi

print "Installing python packages..." $SKIP_NEW_LINE
pip3 install -r bin/requirements.txt --log $LOG_FILE > /dev/null 2>&1
if [ $? -eq 0 ] ; then print "${TEXT_GREEN}[OK]"; else print "${TEXT_RED}[FAILED]"; fi

print "\n"
print "Finished!\n\n"

print "To start the development environment:"
print "\t${TEXT_GREEN}cd $(pwd)"
print "\t${TEXT_GREEN}source ${VENV_DIR}/bin/activate"

exit 0
