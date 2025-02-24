import json
import os
import sys
import csv

class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        """Handles reading files of different types and converting them into a uniform format (dict or list)"""
        file_extension = self.get_file_extension()

        try:
            if file_extension == 'json':
                return self.read_json()
            elif file_extension == 'txt':
                return self.read_txt()
            elif file_extension == 'csv':
                return self.read_csv()
            elif file_extension == 'xml':
                return self.read_xml()
            elif file_extension == 'yaml' or file_extension == 'yml':
                return self.read_yaml()
            else:
                print(f"Unsupported file type: {file_extension}")
                sys.exit(1)
        except Exception as e:
            print(f"Error reading file {self.file_path}: {str(e)}")
            sys.exit(1)

    def get_file_extension(self):
        """Helper function to extract the file extension"""
        _, file_extension = os.path.splitext(self.file_path)
        return file_extension.lower()[1:]  # Strip the dot

    def read_json(self):
        """Reads a JSON file and returns it as a dictionary"""
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def read_txt(self):
        """Reads a plain text file and returns it as a list of lines"""
        with open(self.file_path, 'r') as file:
            return {"content": file.readlines()}  # Treat as list of lines

    def read_csv(self):
        """Reads a CSV file and returns it as a list of dictionaries"""
        with open(self.file_path, 'r') as file:
            reader = csv.DictReader(file)  # CSV to list of dictionaries
            return list(reader)

    def read_xml(self):
        """Reads an XML file and returns it as a dictionary"""
        import xml.etree.ElementTree as ET
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        
        # Convert XML tree to a dictionary (simplified)
        return self.xml_to_dict(root)

    def xml_to_dict(self, element):
        """Recursively converts an XML element and its children to a dictionary"""
        result = {}
        for child in element:
            result[child.tag] = self.xml_to_dict(child) if len(child) > 0 else child.text
        return result

    def read_yaml(self):
        """Reads a YAML file and returns it as a dictionary"""
        import yaml
        with open(self.file_path, 'r') as file:
            return yaml.safe_load(file)

# Example usage
file_path = 'data.json'  # Replace with your actual file path
file_handler = FileHandler(file_path)
data = file_handler.read_file()

print(data)
