import os

def update_pydantic_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace orm_mode with from_attributes
    updated_content = content.replace('orm_mode = True', 'from_attributes = True')
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                update_pydantic_config(file_path)

if __name__ == '__main__':
    schemas_dir = os.path.join('app', 'schemas')
    process_directory(schemas_dir)