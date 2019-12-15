if [ "${INCLUDE_SETUP_FUNCTIONS:=false}" = false ]; then
  echo 'functions_utility.sh is intended as an include and not executed directly.'
  exit 1
fi

function display_script_header {
  clear
  print '\n'
  print $SEPARATOR_LINE
  print '      Relaxed development environment setup script'
  print $SEPARATOR_LINE
  print "\tVersion: ${TEXT_GREEN}${VERSION}"
  print "\tGithub:  ${TEXT_GREEN}${GIT_URL}"
  print "\tAuthor:  ${TEXT_GREEN}${AUTHOR} (${AUTHOR_URL})"
  print '\n' $SKIP_NEW_LINE
  print $SEPARATOR_LINE
}

function display_script_info {
  print "Starting virtual environment installation and configuration..."
  print '\n' $SKIP_NEW_LINE
}

function check_environment {
  print "Environment:"
  print "\tWorking directory:   ${TEXT_GREEN}$(pwd)"
  print "\tVirtual environment: ${TEXT_GREEN}${VENV_DIR}"
  print "\tDetailed log:        ${TEXT_GREEN}${LOG_FILE}"
  print '\n' $SKIP_NEW_LINE

  if ( ! check_requirements ); then
    print '\n' $SKIP_NEW_LINE
    print $SEPARATOR_LINE
    print "${TEXT_RED}It appears that some required tools are not installed or not accessible."
    print '\n' $SKIP_NEW_LINE
    exit 1
  fi

  print '\n' $SKIP_NEW_LINE
  print $SEPARATOR_LINE

}

function check_requirements {
  print "\tPython 3.x+..." $SKIP_NEW_LINE
  PYTHON_CMD=$(type -p python3)
  if [[ -z $PYTHON_CMD ]]; then
    print "${TEXT_RED}[NOT FOUND]"
    REQUIREMENTS_MET=false
  else
    print "${TEXT_GREEN}[FOUND]"
  fi

  print "\tPip3...       " $SKIP_NEW_LINE
  PIP3_CMD=$(type -p pip3)
  if [[ -z $PIP3_CMD ]]; then
    print "${TEXT_RED}[NOT FOUND]"
    REQUIREMENTS_MET=false
  else
    print "${TEXT_GREEN}[FOUND]"
  fi

  if ("${REQUIREMENTS_MET:=true}" = true); then
    return 0
  else
    return 1
  fi

}
