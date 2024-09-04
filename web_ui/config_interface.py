import yaml
import os
from typing import Dict, Any

class ConfigInterface:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        with open(self.config_path, 'r') as config_file:
            return yaml.safe_load(config_file)

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        self.config[key] = value
        self.save_config()

    def save_config(self):
        with open(self.config_path, 'w') as config_file:
            yaml.dump(self.config, config_file)

    def get_environment_specific_config(self, env: str) -> Dict[str, Any]:
        env_config = self.config.get('environments', {}).get(env, {})
        return {**self.config, **env_config}

    def validate_config(self, schema: Dict[str, Any]) -> bool:
        # Implement config validation logic here
        # This is a simple example, you might want to use a library like jsonschema for more complex validations
        for key, value_type in schema.items():
            if key not in self.config or not isinstance(self.config[key], value_type):
                return False
        return True

# Usage example
if __name__ == "__main__":
    config = ConfigInterface("config.yaml")
    
    print("Database URL:", config.get("database_url"))
    
    config.set("log_level", "DEBUG")
    
    prod_config = config.get_environment_specific_config("production")
    print("Production database URL:", prod_config.get("database_url"))
    
    schema = {
        "database_url": str,
        "log_level": str,
        "max_connections": int
    }
    
    is_valid = config.validate_config(schema)
    print("Config is valid:", is_valid)