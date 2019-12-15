if [ "${INCLUDE_CONSTANTS:=false}" = false ]; then
  echo 'constants.sh is intended as an include and not executed directly.'
  exit 1
fi

TEXT_DEFAULT="\e[39m"
TEXT_GREEN="\e[32m"
TEXT_RED="\e[31m"
TEXT_LIGHTRED="\e[91m"
TEXT_YELLOW="\e[33m"
TEXT_BLUE="\e[34m"

SKIP_NEW_LINE=false
