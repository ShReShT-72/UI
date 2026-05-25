import json
import os
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv


class ConfigReader:
    REQUIRED_KEYS = ("base_url", "browser", "timeout")
    CREDENTIAL_KEYS = ("username", "password", "locked_user", "invalid_user", "invalid_password")

    def __init__(self, env: str | None = None) -> None:
        self.base_dir = Path(__file__).resolve().parent.parent
        self._load_dotenv()
        self.env = env or os.environ.get("ENV", "default")
        self.config = self._load_config()
        self._apply_environment_overrides()
        self._validate()

    def _load_dotenv(self) -> None:
        dotenv_path = self.base_dir / "config" / ".env"
        if dotenv_path.exists():
            load_dotenv(dotenv_path=dotenv_path)

    def _load_config(self) -> Dict[str, Any]:
        base_file = self.base_dir / "config" / "config.json"
        if not base_file.exists():
            raise FileNotFoundError(f"Base config not found: {base_file}")
        with base_file.open("r", encoding="utf-8") as f:
            config = json.load(f)

        if self.env != "default":
            overlay_file = self.base_dir / "config" / f"config.{self.env}.json"
            if not overlay_file.exists():
                raise FileNotFoundError(f"Environment config not found: {overlay_file}")
            with overlay_file.open("r", encoding="utf-8") as f:
                config.update(json.load(f))

        return config

    # Windows reserves USERNAME as a system env var — use prefixed keys to avoid collision
    _ENV_KEY_MAP = {
        "username": "APP_USERNAME",
        "password": "APP_PASSWORD",
        "locked_user": "APP_LOCKED_USER",
        "invalid_user": "APP_INVALID_USER",
        "invalid_password": "APP_INVALID_PASSWORD",
    }

    def _apply_environment_overrides(self) -> None:
        for key, value in self.config.items():
            env_key = self._ENV_KEY_MAP.get(key, key.upper())
            env_value = os.environ.get(env_key)
            if env_value is not None:
                self.config[key] = self._convert_value(env_value, value)
        for key in self.CREDENTIAL_KEYS:
            env_key = self._ENV_KEY_MAP.get(key, key.upper())
            env_value = os.environ.get(env_key)
            if env_value is not None:
                self.config[key] = env_value

    def _validate(self) -> None:
        missing = [k for k in self.REQUIRED_KEYS if not self.config.get(k)]
        if missing:
            raise KeyError(f"Missing required config keys: {missing}")

    @staticmethod
    def _convert_value(env_value: str, original_value: Any) -> Any:
        if isinstance(original_value, bool):
            return env_value.strip().lower() in ("1", "true", "yes", "on")
        if isinstance(original_value, int):
            try:
                return int(env_value)
            except ValueError:
                return original_value
        return env_value

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def get_browser(self) -> str:
        return self.get("browser", "chromium").lower()
