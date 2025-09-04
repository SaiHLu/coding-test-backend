# Virtual environment paths
VENV = venv
PYTHON = $(VENV)/bin/python
ALEMBIC = $(VENV)/bin/alembic

install:
	@$(PYTHON) -m pip install -r requirements.txt

start:
	@$(PYTHON) -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

test:
	@$(PYTHON) -m pytest . -s -v

gui:
	@$(PYTHON) -m streamlit run src/streamlit_app.py --server.port 8501

create-migration:
	@if [ -z "$(MSG)" ]; then \
		echo "Usage: make create-migration MSG=\"Your migration message\""; \
		echo "Example: make create-migration MSG=\"Add user table\""; \
		exit 1; \
	fi
	@$(ALEMBIC) revision --autogenerate -m "$(MSG)"

migration-up:
	@if [ -n "$(TARGET)" ]; then \
		echo "Upgrading to revision: $(TARGET)"; \
		$(ALEMBIC) upgrade $(TARGET); \
	else \
		echo "Upgrading to latest revision"; \
		$(ALEMBIC) upgrade head; \
	fi

migration-down:
	@if [ -n "$(TARGET)" ]; then \
		echo "Downgrading to revision: $(TARGET)"; \
		$(ALEMBIC) downgrade $(TARGET); \
	elif [ -n "$(STEPS)" ]; then \
		echo "Downgrading $(STEPS) step(s)"; \
		$(ALEMBIC) downgrade -$(STEPS); \
	else \
		echo "Downgrading 1 step"; \
		$(ALEMBIC) downgrade -1; \
	fi

.PHONY: install create-migration migration-up migration-down test