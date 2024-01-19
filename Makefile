env:
	micromamba create -f env.yaml -y
check:
	ruff check --preview --fix .

format:
	ruff format --preview .

typecheck:
	pyright .

all: format check typecheck
