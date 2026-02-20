VENV = venv
PYTHON = python3
VENV_PYTHON = $(VENV)/bin/python
VENV_PIP = $(VENV)/bin/pip
NAME = ./mazegen/a_maze_ing.py
ARG = ./config.txt
REQUIEREMENTS = ./requirements.txt

.PHONY: install run debug clean lint

#make install
install:
	rm -rf $(VENV)
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -r $(REQUIEREMENTS)	


#make run
run:
	$(VENV)/bin/python $(NAME) $(ARG)


#make debug
debug:
	$(VENV)/bin/python -m pdb $(NAME) $(ARG)

#make clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.swp" -delete
#make lint
lint:
	./venv/bin/python -m flake8 $(NAME)
	./venv/bin/python -m mypy $(NAME) \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs
