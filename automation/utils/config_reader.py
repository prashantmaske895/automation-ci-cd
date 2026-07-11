# -*- coding: utf-8 -*-
"""
utils/config_reader.py

Loads environment-specific settings (base_url, browser, timeouts, viewport,
storage_state path) from config/environments.yaml.

Usage:
    from utils.config_reader import get_config
    config = get_config()             # uses ENV env var, defaults to "qa"
    config = get_config("staging")    # explicit environment
"""
import os
import yaml

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "environments.yaml")


def get_config(env: str = None) -> dict:
    """
    Returns the configuration dict for the requested environment.
    Falls back to the ENV environment variable, then to "qa".
    """
    env_name = env or os.getenv("ENV", "qa")

    with open(CONFIG_PATH, "r") as f:
        all_envs = yaml.safe_load(f)

    if env_name not in all_envs:
        raise ValueError(
            f"Environment '{env_name}' not found in environments.yaml. "
            f"Available environments: {list(all_envs.keys())}"
        )

    cfg = all_envs[env_name]
    cfg["env_name"] = env_name

    # Resolve storage_state_path to an absolute path so it works
    # regardless of which directory pytest is invoked from.
    cfg["storage_state_path"] = os.path.join(PROJECT_ROOT, cfg["storage_state_path"])

    return cfg


if __name__ == "__main__":
    # Quick manual check: python utils/config_reader.py
    import json
    print(json.dumps(get_config(), indent=2))
