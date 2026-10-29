---
name: bdd-runner
description: >-
  Herramienta de ejecución y diagnóstico para la suite Behave BDD (UI, API, Allure y Rerun)
  de este proyecto. Úsala para correr pruebas, diagnosticar fallos y generar reportes.
---

# BDD Runner Skill

Esta skill define el procedimiento para ejecutar pruebas automatizadas en este repositorio y analizar los resultados generados.

## 1. Entorno Virtual

Todas las herramientas de prueba se encuentran en el entorno virtual `./venv/`:
- Python: `./venv/bin/python`
- Behave: `./venv/bin/behave`
- Pip: `./venv/bin/pip`

## 2. Comandos Principales

### Ejecutar un feature específico:
```bash
./venv/bin/behave features/login.feature
./venv/bin/behave features/api_users.feature
./venv/bin/behave features/login.feature:8 # Por número de línea
```

### Ejecutar todas las pruebas con Allure y Rerun:
```bash
./venv/bin/behave -f allure -o allure-results -f rerun -o rerun.txt
```

### Ejecutar solo pruebas de UI (SauceDemo):
```bash
./venv/bin/behave --tags=@ui -f allure -o allure-results
```

### Ejecutar solo pruebas de API (ReqRes):
```bash
./venv/bin/behave --tags=@api -f allure -o allure-results
```

### Cambiar de navegador en caliente:
```bash
# Chrome Headless
./venv/bin/behave --tags=@ui -D browser=chrome -D headless=true

# Firefox
./venv/bin/behave --tags=@ui -D browser=firefox -D headless=true
```

### Re-ejecutar solo escenarios fallidos:
```bash
./venv/bin/behave @rerun.txt
```

### Generar reporte Allure estático:
```bash
allure generate allure-results -o allure-report --clean
```

## 3. Diagnóstico de Fallos

1. Revisar los logs detallados en `logs/automation.log`.
2. Inspeccionar capturas de pantalla de fallos en `screenshots/`.
3. Revisar el archivo `rerun.txt` para identificar los escenarios específicos que fallaron.

