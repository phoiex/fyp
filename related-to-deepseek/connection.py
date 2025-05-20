import time
import os
import sys
import django
from django.apps import apps
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add the project root directory to sys.path to ensure Django can find manager/settings.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set Django's settings module path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')

# Initialize the Django environment
django.setup()

# Define the model name we care about
target_models = [
    'projects.project',
    'projects.task',
    'projects.ProjectDetails'
]

# Save all model data to txt file (overwrite old file)
def save_data_to_txt(data):
    with open("update_log.txt", "w", encoding="utf-8") as file:
        for record in data:
            file.write(str(record) + "\n")
    print("Data saved to update_log.txt")

# Monitor SQLite database file changes
class SQLiteChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('db.sqlite3'):  # Monitor changes in database files
            print(f"Database file {event.src_path} changed, checking for updates...")
            check_for_updates()

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
                all_data.extend(data)  # Add all data to the all_data list
            else:
                print(f"No data found in model {model.__name__}")

        except LookupError:
            print(f"Model '{model_name}' not found.")
    
    # Save all model data to txt file
    if all_data:
        save_data_to_txt(all_data)

# Start the file system watcher
def start_observer():
    event_handler = SQLiteChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Start file monitoring
start_observer()
