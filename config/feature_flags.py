from config.config_manager import ConfigManager

class FeatureFlags:
    def __init__(self, config_path):
        self.config_manager = ConfigManager(config_path)

    def is_feature_enabled(self, feature_name):
        return self.config_manager.get(f'feature_{feature_name}', False)

    def enable_feature(self, feature_name):
        self.config_manager.set(f'feature_{feature_name}', True)

    def disable_feature(self, feature_name):
        self.config_manager.set(f'feature_{feature_name}', False)

    def get_all_features(self):
        return {key[8:]: value for key, value in self.config_manager.config.items() if key.startswith('feature_')}

    def reset_all_features(self):
        for key in list(self.config_manager.config.keys()):
            if key.startswith('feature_'):
                del self.config_manager.config[key]
        self.config_manager.save_config()