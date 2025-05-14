import time
import os
import sys
import django
from django.apps import apps
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

# 将项目根目录添加到 sys.path 中，确保 Django 可以找到 manager/settings.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 设置 Django 的 settings 模块路径
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')

# 初始化 Django 环境
django.setup()

# 定义我们关心的模型名称（只关心 'ProjectDetails'）
target_model = 'projects.projectdetails'  # ProjectDetails 模型

# 监听 SQLite 数据库文件变动
class SQLiteChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('db.sqlite3'):  # 监听数据库文件的变动
            print(f"Database file {event.src_path} changed, checking for updates...")
            check_for_updates()

# 查询 'ProjectDetails' 模型是否有更新
def check_for_updates():
    try:
        # 获取模型
        model = apps.get_model(target_model)
        print(f"Checking updates for Model: {model.__name__}")

        # 获取最新的 ProjectDetails 数据
        data = model.objects.all().values()

        if data:
            print(f"ProjectDetails model has been updated. Running run-2.py...")
            run_script()  # 如果有更新，运行 run-2.py
        else:
            print(f"No data found in model {model.__name__}")

    except LookupError:
        print(f"Model '{target_model}' not found.")

# 运行 run-2.py 脚本
def run_script():
    try:
        subprocess.run(['python', 'run-2.py'], check=True)
        subprocess.run(['python', 'relate-to-deepseek/ditdatabase.py'], check=True)
        
        print("run-2.py script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running script: {e}")
    
    # 停止监听
    stop_observer()

# 启动文件系统观察者
def start_observer():
    event_handler = SQLiteChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)  # 监听当前目录
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# 停止文件监听
def stop_observer():
    print("Stopping file observer.")
    observer.stop()
    observer.join()

# 启动文件监听
start_observer()
