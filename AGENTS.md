# AGENTS.md - Directrices de Arquitectura y Estándares para Agentes de IA

Este repositorio implementa un framework empresarial de automatización de pruebas BDD con **Behave**, **Selenium 4**, **Requests** y **Allure Reports**.
Cualquier agente que trabaje en este código debe adherirse estrictamente a las siguientes directrices:

## 1. Arquitectura y Capas

- **Features (`features/`)**:
  - Toda prueba de interfaz gráfica debe tener la etiqueta `@ui`.
  - Toda prueba de servicio REST/API debe tener la etiqueta `@api`.
  - Agrupar por tags de suite: `@smoke`, `@regression`.
- **Hooks (`features/environment.py`)**:
  - El ciclo de vida de Selenium (`driver`) es condicional. NUNCA abras el navegador en escenarios `@api`.
  - Si un step falla en una prueba `@ui`, captura la evidencia gráfica y adjúntala a Allure.
- **Steps (`features/steps/`)**:
  - Para pasos con parámetros entre comillas, usar `use_step_matcher("re")` con grupos nombrados (`(?P<var>[^"]*)`) para compatibilidad total con la indexación y navegación de PyCharm/IntelliJ.
- **Page Object Model (`pages/`)**:
  - Todas las páginas deben heredar de `BasePage`.
  - Los localizadores (`By.ID`, `By.CSS_SELECTOR`, etc.) se declaran como atributos de clase tipo tupla.
  - NUNCA instanciar elementos web con `find_element` en el `__init__`.
  - Usar los métodos de espera explícita de `BasePage` (`click`, `send_text`, `is_visible`).
  - NUNCA usar `time.sleep()`.
- **Configuración y Secretos (`utils/config_reader.py`)**:
  - Las credenciales y variables se manejan vía `python-dotenv` (`.env`).
  - Nunca hardcodear URLs o contraseñas en los steps ni comitear `.env`.
  - La precedencia de configuración es: CLI flags (`-D`) > `.env` > `config.json`.
- **Logging (`utils/logger.py`)**:
  - Utilizar siempre `get_logger(__name__)` para registrar navegación, acciones y peticiones HTTP.

## 2. Comandos de Ejecución

- Pruebas UI: `make test-ui` o `./venv/bin/behave --tags=@ui -f allure -o allure-results`
- Pruebas API: `make test-api` o `./venv/bin/behave --tags=@api -f allure -o allure-results`
- Re-ejecución de fallos: `make rerun` o `./venv/bin/behave @rerun.txt`
- Generar reporte Allure: `make report` o `allure serve allure-results`

