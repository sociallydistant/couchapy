if [ "${INCLUDE_UTIL_FUNCTIONS:=false}" = false ]; then
  echo 'functions_utility.sh is intended as an include and not executed directly.'
  exit 1
fi

function print {
  local INCLUDE_NEW_LINE=$2
  #echo $2
  echo -en "  ${1}${TEXT_DEFAULT}"
  if [ ! "$2" = false ]; then
    echo -en "\n"
  fi
}

function activate_virtual_environment {
  source ./$VENV_DIR/bin/activate
}

function clear_line {
  ceol=$(tput el)
  echo -en "\r${ceol}"
}
