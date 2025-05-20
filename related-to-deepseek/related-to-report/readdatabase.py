import os
import sys
import django
from django.apps import apps

# Add the project root directory to sys.path to ensure Django can find manager/settings.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Set Django's settings module path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')

# Initialize the Django environment
django.setup()

# Define the model names we care about (only 'Project' and 'Task')
target_models = [
    'projects.project',  
    'projects.ProjectDetails',
    'projects.Task',
    'projects.ProjectedInfo'  
]

# Save all model data to txt file (overwrite old file)
def save_data_to_txt(data):
    with open("classproject.txt", "w", encoding="utf-8") as file:
        for record in data:
            file.write(str(record) + "\n")
    print("Data saved to classproject.txt")

# Query all model data and save to file
def check_for_updates():
    all_data = []
    for model_name in target_models:
        try:
            # Get the model
            model = apps.get_model(model_name)
            print(f"Checking updates for Model: {model.__name__}")

            # Get all the data of the model
            data = model.objects.all().values()
            if data:
                all_data.extend(data)
            else:
                print(f"No data found in model {model.__name__}")

        except LookupError:
            print(f"Model '{model_name}' not found.")
    
    # Save all model data to txt file
    if all_data:
        save_data_to_txt(all_data)


# Perform a database check immediately after the program starts
if __name__ == "__main__":
    check_for_updates()