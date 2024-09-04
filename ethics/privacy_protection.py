import hashlib
from typing import Dict, Any, List
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

class PrivacyProtection:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)

    def encrypt_data(self, data: str) -> str:
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data: str) -> str:
        return self.fernet.decrypt(encrypted_data.encode()).decode()

    def anonymize_data(self, data: Dict[str, Any], sensitive_fields: List[str]) -> Dict[str, Any]:
        anonymized_data = data.copy()
        for field in sensitive_fields:
            if field in anonymized_data:
                anonymized_data[field] = self._hash_value(str(anonymized_data[field]))
        return anonymized_data

    def _hash_value(self, value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()

class UserConsentManager:
    def __init__(self):
        self.user_consents = {}

    def set_user_consent(self, user_id: str, consent_type: str, consented: bool):
        if user_id not in self.user_consents:
            self.user_consents[user_id] = {}
        self.user_consents[user_id][consent_type] = consented

    def get_user_consent(self, user_id: str, consent_type: str) -> bool:
        return self.user_consents.get(user_id, {}).get(consent_type, False)

    def revoke_all_consents(self, user_id: str):
        if user_id in self.user_consents:
            self.user_consents[user_id] = {}

class DataRetentionPolicy:
    def __init__(self):
        self.retention_periods = {}

    def set_retention_period(self, data_type: str, period_days: int):
        self.retention_periods[data_type] = period_days

    def get_retention_period(self, data_type: str) -> int:
        return self.retention_periods.get(data_type, 0)

    def should_retain_data(self, data_type: str, creation_date: datetime) -> bool:
        retention_period = self.get_retention_period(data_type)
        if retention_period == 0:
            return True  # Retain indefinitely if no period is set
        return (datetime.now() - creation_date) <= timedelta(days=retention_period)

class PrivacyImpactAssessment:
    def __init__(self):
        self.assessments = {}

    def add_assessment(self, process_name: str, impact_level: str, mitigation_steps: List[str]):
        self.assessments[process_name] = {
            "impact_level": impact_level,
            "mitigation_steps": mitigation_steps
        }

    def get_assessment(self, process_name: str) -> Dict[str, Any]:
        return self.assessments.get(process_name, {})

    def update_mitigation_steps(self, process_name: str, new_steps: List[str]):
        if process_name in self.assessments:
            self.assessments[process_name]["mitigation_steps"] = new_steps

# Usage example
if __name__ == "__main__":
    # Privacy Protection
    encryption_key = Fernet.generate_key()
    privacy_protector = PrivacyProtection(encryption_key)
    
    sensitive_data = "This is sensitive information"
    encrypted_data = privacy_protector.encrypt_data(sensitive_data)
    print("Encrypted data:", encrypted_data)
    decrypted_data = privacy_protector.decrypt_data(encrypted_data)
    print("Decrypted data:", decrypted_data)

    # User Consent Management
    consent_manager = UserConsentManager()
    consent_manager.set_user_consent("user123", "data_collection", True)
    print("User consent:", consent_manager.get_user_consent("user123", "data_collection"))

    # Data Retention Policy
    retention_policy = DataRetentionPolicy()
    retention_policy.set_retention_period("user_logs", 30)
    should_retain = retention_policy.should_retain_data("user_logs", datetime.now() - timedelta(days=15))
    print("Should retain data:", should_retain)

    # Privacy Impact Assessment
    pia = PrivacyImpactAssessment()
    pia.add_assessment("user_data_analysis", "medium", ["Anonymize data", "Limit access"])
    print("PIA for user data analysis:", pia.get_assessment("user_data_analysis"))