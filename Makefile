VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
BEHAVE = $(VENV)/bin/behave

.PHONY: help install test-ui test-api test-all rerun report serve-report clean

help:
	@echo "Comandos disponibles:"
	@echo "  make install      - Crea el virtualenv e instala dependencias"
	@echo "  make test-ui      - Ejecuta pruebas de UI con reporte Allure"
	@echo "  make test-api     - Ejecuta pruebas de API con reporte Allure"
	@echo "  make test-all     - Ejecuta todas las pruebas (UI + API) con Allure y Rerun"
	@echo "  make rerun        - Re-ejecuta únicamente los tests fallidos en rerun.txt"
	@echo "  make report       - Genera el reporte HTML de Allure en allure-report/"
	@echo "  make serve-report - Abre el servidor web interactivo de Allure"
	@echo "  make clean        - Limpia temporales, screenshots, logs y reportes"

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@if [ ! -f .env ]; then cp .env.example .env; echo "Creado .env desde .env.example"; fi

test-ui:
	$(BEHAVE) --tags=@ui -f allure -o allure-results -f rerun -o rerun.txt

test-api:
	$(BEHAVE) --tags=@api -f allure -o allure-results

test-all:
	$(BEHAVE) -f allure -o allure-results -f rerun -o rerun.txt

rerun:
	@if [ -s rerun.txt ]; then \
		$(BEHAVE) @rerun.txt -f allure -o allure-results; \
	else \
		echo "No hay pruebas fallidas registradas en rerun.txt"; \
	fi

report:
	allure generate allure-results -o allure-report --clean
	@echo "Reporte generado en allure-report/index.html"

serve-report:
	allure serve allure-results

clean:
	rm -rf allure-results allure-report screenshots logs rerun.txt __pycache__ .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

