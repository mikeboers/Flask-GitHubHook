

_self="$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)"
_venv="$_self/var/venv"

if [[ ! -f "$_venv/bin/python" ]]; then
    virtualenv --no-site-packages "$_venv"
fi

. "$_venv/bin/activate"

pip install -r requirements-app.txt
pip install -e "$self"


