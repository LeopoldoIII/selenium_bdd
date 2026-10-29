import os
import json
from dotenv import load_dotenv

# Load .env file automatically on import
load_dotenv()

_CONFIG_CACHE = None


def get_config():
    global _CONFIG_CACHE
    if _CONFIG_CACHE is None:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as file:
                    _CONFIG_CACHE = json.load(file)
            except Exception:
                _CONFIG_CACHE = {}
        else:
            _CONFIG_CACHE = {}
    return _CONFIG_CACHE


def _parse_value(val):
    if isinstance(val, str):
        lower_val = val.strip().lower()
        if lower_val == "true":
            return True
        if lower_val == "false":
            return False
        if lower_val.isdigit():
            return int(lower_val)
    return val


def get_property(key, context=None, default=None):
    """
    Resolution hierarchy:
    1. CLI parameters via Behave userdata: `behave -D key=value`
    2. Environment variables (.env or OS environment)
    3. JSON configuration in config/config.json
    4. Default value
    """
    # 1. Behave CLI -D flags
    if context and hasattr(context, "config") and hasattr(context.config, "userdata"):
        if key in context.config.userdata:
            return _parse_value(context.config.userdata[key])
        if key.lower() in context.config.userdata:
            return _parse_value(context.config.userdata[key.lower()])

    # 2. Environment variables (.env / OS)
    env_key = key.upper()
    env_val = os.getenv(env_key)
    if env_val is None:
        env_val = os.getenv(key)
    if env_val is not None:
        return _parse_value(env_val)

    # 3. JSON Configuration
    config = get_config()
    if key in config:
        return config[key]

    # Nested config support (e.g. ui.url, api.base_url)
    if "." in key:
        parts = key.split(".")
        current = config
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                current = None
                break
        if current is not None:
            return current

    # 4. Fallback default
    return default
