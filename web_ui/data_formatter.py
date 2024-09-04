import json
import xml.etree.ElementTree as ET
from typing import Dict, Any, Union

class DataFormatter:
    @staticmethod
    def to_json(data: Dict[str, Any]) -> str:
        return json.dumps(data, indent=2)

    @staticmethod
    def from_json(json_str: str) -> Dict[str, Any]:
        return json.loads(json_str)

    @staticmethod
    def to_xml(data: Dict[str, Any]) -> str:
        root = ET.Element("root")
        DataFormatter._dict_to_xml(root, data)
        return ET.tostring(root, encoding="unicode", method="xml")

    @staticmethod
    def from_xml(xml_str: str) -> Dict[str, Any]:
        root = ET.fromstring(xml_str)
        return DataFormatter._xml_to_dict(root)

    @staticmethod
    def _dict_to_xml(parent: ET.Element, data: Dict[str, Any]):
        for key, value in data.items():
            child = ET.SubElement(parent, key)
            if isinstance(value, dict):
                DataFormatter._dict_to_xml(child, value)
            else:
                child.text = str(value)

    @staticmethod
    def _xml_to_dict(element: ET.Element) -> Dict[str, Any]:
        result = {}
        for child in element:
            if len(child) == 0:
                result[child.tag] = child.text
            else:
                result[child.tag] = DataFormatter._xml_to_dict(child)
        return result

    @staticmethod
    def validate_data(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        # Implement data validation logic here
        # This is a simple example, you might want to use a library like jsonschema for more complex validations
        for key, value_type in schema.items():
            if key not in data or not isinstance(data[key], value_type):
                return False
        return True

# Usage example
if __name__ == "__main__":
    test_data = {
        "name": "John Doe",
        "age": 30,
        "skills": ["Python", "JavaScript", "Machine Learning"]
    }

    json_str = DataFormatter.to_json(test_data)
    print("JSON:", json_str)

    xml_str = DataFormatter.to_xml(test_data)
    print("XML:", xml_str)

    schema = {
        "name": str,
        "age": int,
        "skills": list
    }

    is_valid = DataFormatter.validate_data(test_data, schema)
    print("Data is valid:", is_valid)