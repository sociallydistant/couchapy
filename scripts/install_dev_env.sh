#!/bin/bash
DEFAULT=`echo "\033[39m"`
GREEN=`echo "\033[32m"`
RED=`echo "\033[31m"`
DEEP_RED=`echo "\033[41m"`
LIGHT_RED=`echo "\033[91m"`
YELLOW=`echo "\033[33m"`
BLUE=`echo "\033[36m"`

SKIP_NEW_LINE=false

VENV_DIR="venv"
LOG_FILE="$(pwd)/.setup.log"

function print {
  echo -en "${1}${DEFAULT}"
  if [ ! "$2" = false ]; then
    echo -en "\n"
  fi
}

# Borrowed with love from https://stackoverflow.com/a/20369590
function spinner {
  local pid=$!
  local delay=0.25
  local spinstr='|/-\'
  while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
    local temp=${spinstr#?}
    printf "[%c]  " "$spinstr"
    local spinstr=$temp${spinstr%"$temp"}
    sleep $delay
    printf "\b\b\b\b\b"
  done
  printf "    \b\b\b\b"
}

print "  ${BLUE}Checking for Python 3 interpreter...\t\t" $SKIP_NEW_LINE
PYTHON_CMD=$(type -p python3)
if [[ -z $PYTHON_CMD ]]; then
  print "  ${RED}[NOT FOUND]"
  print "  ${YELLOW}This is usually because you do not have a" $SKIP_NEW_LINE
  print "${YELLOW} Python 3 interpreter installed or your \$PATH" $SKIP_NEW_LINE
  print "${YELLOW} is not set correct."
  print "  ${YELLOW}Your \$PATH is:"
  print "    $PATH"
  exit 1
else
  print "${GREEN}[FOUND]"
fi

print "  ${BLUE}Checking Python 3 version...\t\t\t" $SKIP_NEW_LINE
PYTHON_VERSION=`$PYTHON_CMD -c 'import sys; version=sys.version_info[:3]; print("{0}.{1}.{2}".format(*version))'`
if [[ "$PYTHON_VERSION" < "3.6" ]]; then
  print "${RED}[${PYTHON_VERSION}]"
  print "  ${YELLOW}Minimum supported version is 3.6.x. "
  print "  ${YELLOW}Detected version ${PYTHON_VERSION}"
  exit 1
else
  print "${GREEN}[${PYTHON_VERSION}]"
fi

print "  ${BLUE}Checking for pip3...\t\t\t\t" $SKIP_NEW_LINE
PIP3_CMD=$(type -p pip3)
if [[ -z $PIP3_CMD ]]; then
  print "${RED}[NOT FOUND]"
  exit 1
else
  print "${GREEN}[FOUND]"
fi


print "  ${BLUE}Removing existing virtual environment...\t" $SKIP_NEW_LINE
rm -rf "$VENV_DIR"
if [ $? -eq 0 ]; then
  print "${GREEN}[DONE]"
else
  print "${RED}[FAILED]"
  exit 1
fi

print "  ${BLUE}Creating new virtual environment...\t\t" $SKIP_NEW_LINE
if [ $? -eq 0 ] && ( python3 -m venv $VENV_DIR & spinner); then
  print "${GREEN}[DONE]"
  print "    ${YELLOW}New virtual environment created at: ${DEFAULT}$(pwd)/${VENV_DIR}"
else
  print "${RED}[FAILED]"
  exit 1
fi

print "  ${BLUE}Activating virtual environment...\t\t" $SKIP_NEW_LINE
source ./$VENV_DIR/bin/activate
if [ $? -eq 0 ]; then
  print "${GREEN}[DONE]"
else
  print "${RED}[FAILED]"
  exit 1
fi

print "  ${BLUE}Installing project dependencies...\t\t" $SKIP_NEW_LINE
python3 -m pip install -r requirements.txt --log $LOG_FILE > /dev/null 2>&1 & spinner
if [ $? -eq 0 ] ; then
  print "${GREEN}[DONE]"
  INSTALL_OK=true
else
  print "${RED}[FAILED]"
  INSTALL_OK=false
fi

print "    ${YELLOW}Installation report written to: ${DEFAULT}${LOG_FILE}"

if [ "$INSTALL_OK" = false ]; then
  print "\n  ${RED}The installation of project dependencies failed with errors.  Consule installation report."
  exit 1
fi

print "\n  ${GREEN}The development environment has been set up successfully.\n\n"

print "  To start the development environment:"
print "\t${YELLOW}cd $(pwd)"
print "\t${YELLOW}source ${VENV_DIR}/bin/activate"

exit 0
