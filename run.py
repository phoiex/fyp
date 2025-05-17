import time
import os
import sys
import django
from django.apps import apps
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

# Add the project root directory to sys.path to ensure Django can find manager/settings.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set Django's settings module path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')

# Initialize the Django environment
django.setup()

# Define the name of the model we care about (only 'ProjectDetails')
target_model = 'projects.projectdetails'  # ProjectDetails Model

# Monitor SQLite database file changes
class SQLiteChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('db.sqlite3'):  # Monitor changes to database files
            print(f"Database file {event.src_path} changed, checking for updates...")
            check_for_updates()

# Check if the 'ProjectDetails' model has been updated
def check_for_updates():
    try:
        # Get model
        model = apps.get_model(target_model)
        print(f"Checking updates for Model: {model.__name__}")

        # Get the latest ProjectDetails data
        data = model.objects.all().values()

        if data:
            print(f"ProjectDetails model has been updated. Running run-2.py...")
            run_script()  # If there is an update, run run-2.py
        else:
            print(f"No data found in model {model.__name__}")

    except LookupError:
        print(f"Model '{target_model}' not found.")

# Run the run-2.py script
def run_script():
    try:
        subprocess.run(['python', 'run-2.py'], check=True)
        subprocess.run(['python', 'relate-to-deepseek/ditdatabase.py'], check=True)
        
        print("run-2.py script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running script: {e}")
    
    # Stop listening
    stop_observer()

# Start the file system watcher
def start_observer():
    event_handler = SQLiteChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)  # Listen to the current directory
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Stop file monitoring
def stop_observer():
    print("Stopping file observer.")
    observer.stop()
    observer.join()

# Start file monitoring
start_observer()
