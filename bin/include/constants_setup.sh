if [ "${INCLUDE_SETUP_CONSTANTS:=false}" = false ]; then
  echo 'constants_setup.sh is intended as an include and not executed directly.'
  exit 1
fi

VERSION="0.0.1"
GIT_URL="https://github.com/llunn/relaxed"
AUTHOR='Lee Lunn'
AUTHOR_URL="https://github.com/llunn/"
SEPARATOR_LINE="$(head -c 60 /dev/zero |tr '\0' '=')\n"

LOG_FILE="$(pwd)/.setup.log"
ENV_FILE="src/.env"
ENV_TEMPLATE_FILE="src/.env.template"
VENV_DIR="venv"
