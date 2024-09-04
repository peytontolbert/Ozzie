from utils.logger import Logger
from utils.error_handler import ErrorHandler

class DataReconciliation:
    def __init__(self, primary_store, secondary_store):
        self.primary_store = primary_store
        self.secondary_store = secondary_store
        self.logger = Logger("DataReconciliation")
        self.error_handler = ErrorHandler()

    def reconcile(self, key):
        try:
            primary_data = self.primary_store.load(key)
            secondary_data = self.secondary_store.load(key)

            if primary_data is None and secondary_data is None:
                self.logger.info(f"Key {key} not found in either store")
                return None

            if primary_data is None:
                self.logger.warning(f"Key {key} missing from primary store, copying from secondary")
                self.primary_store.save(key, secondary_data)
                return secondary_data

            if secondary_data is None:
                self.logger.warning(f"Key {key} missing from secondary store, copying from primary")
                self.secondary_store.save(key, primary_data)
                return primary_data

            if primary_data != secondary_data:
                self.logger.warning(f"Data mismatch for key {key}, using primary store data")
                self.secondary_store.save(key, primary_data)
                return primary_data

            self.logger.info(f"Data for key {key} is consistent across stores")
            return primary_data

        except Exception as e:
            self.error_handler.handle_error(e, f"Error during data reconciliation for key {key}")
            return None

    def full_reconciliation(self):
        all_keys = set(self.primary_store.list_keys() + self.secondary_store.list_keys())
        for key in all_keys:
            self.reconcile(key)
        self.logger.info("Full data reconciliation completed")