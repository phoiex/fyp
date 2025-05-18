import time
import os
import sys
import django
import json
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 添加 Django 项目路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')
django.setup()

from projects.models import Task, User, Project


def load_json_with_comments(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
        data = re.sub(r'#.*', '', data)
        data = re.sub(r'```json|```', '', data)
        data = data.replace("'", '"')
        return json.loads(data)


def update_task_from_txt(file_path):
    print(f"Detected update in {file_path}, processing...")
    try:
        task_data = load_json_with_comments(file_path)
    except Exception as e:
        print(f"Failed to load JSON: {e}")
        return

    operation = task_data.get("operation")
    task_info = task_data.get("tasks")
    task_id = task_data.get("task_id")

    if operation == 'create' and task_info:
        for task_data in task_info:
            task_name = task_data.get("task_name")
            project_id = task_data.get("project_id")
            assigned_user_ids = task_data.get("assigned_user_ids", [])
            status = task_data.get("status")
            due = task_data.get("due")
            task_description = task_data.get("task_description", "")
            due_date = task_data.get("due_date", "")
            start_date = task_data.get("start_date", "")

            try:
                project = Project.objects.get(id=project_id)
                users = User.objects.filter(id__in=assigned_user_ids)

                new_task = Task.objects.create(
                    task_name=task_name,
                    project=project,
                    status=status,
                    due=due,
                    task_description=task_description,
                    due_date=due_date,
                    start_date=start_date
                )
                new_task.assign.set(users)
                new_task.save()
                print(f"Task '{task_name}' created successfully.")
            except Project.DoesNotExist:
                print(f"Project with id {project_id} not found.")
            except User.DoesNotExist:
                print(f"One or more users with the specified ids were not found.")

    elif operation == 'update' and task_id:
        try:
            task = Task.objects.get(id=task_id)
            task.task_name = task_info.get("task_name", task.task_name)
            task.status = task_info.get("status", task.status)
            task.due = task_info.get("due", task.due)
            task.task_description = task_info.get("task_description", task.task_description)
            task.due_date = task_info.get("due_date", task.due_date)
            task.start_date = task_info.get("start_date", task.start_date)

            assigned_user_ids = task_info.get("assigned_user_ids", [])
            users = User.objects.filter(id__in=assigned_user_ids)
            task.assign.set(users)

            task.save()
            print(f"Task '{task_id}' updated successfully.")
        except Task.DoesNotExist:
            print(f"Task with id {task_id} not found.")
        except User.DoesNotExist:
            print(f"One or more users with the specified ids were not found.")

    elif operation == 'delete' and task_id:
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            print(f"Task '{task_id}' deleted successfully.")
        except Task.DoesNotExist:
            print(f"Task with id {task_id} not found.")
    else:
        print(f"Invalid operation: {operation}")


class TaskFileEventHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = os.path.abspath(file_path)

    def on_modified(self, event):
        if os.path.abspath(event.src_path) == self.file_path:
            update_task_from_txt(self.file_path)


if __name__ == "__main__":
    file_to_watch = 'assistant_reply1.txt'
    path = os.path.dirname(os.path.abspath(file_to_watch))
    event_handler = TaskFileEventHandler(file_to_watch)
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()
    print(f"Watching for changes in {file_to_watch}...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
