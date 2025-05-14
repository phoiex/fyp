import time
import os
import sys
import django
import json
import re
from django.apps import apps

# 将项目根目录添加到 sys.path 中，确保 Django 可以找到 manager/settings.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# 设置 Django 的 settings 模块路径
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')

# 初始化 Django 环境
django.setup()
from projects.models import Task, User, Project

# 处理并加载 JSON 文件，删除注释并替换为合法的 JSON 格式
def load_json_with_comments(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
        
        # 删除所有的注释部分（#后面的内容）
        data = re.sub(r'#.*', '', data)
        data = re.sub(r'```json|```', '', data)
        # 替换单引号为双引号，确保 JSON 格式合法
        data = data.replace("'", '"')
        
        # 解析为字典
        return json.loads(data)

def update_task_from_txt(file_path):
    # 读取并处理txt文件内容
    task_data = load_json_with_comments(file_path)
    
    # 获取操作类型和任务信息
    operation = task_data.get("operation")
    task_info = task_data.get("tasks")  # 将 tasks 改为 tasks 列表
    task_id = task_data.get("task_id")

    if operation == 'create' and task_info:
        # 批量创建任务
        for task_data in task_info:
            task_name = task_data.get("task_name")
            project_id = task_data.get("project_id")
            assigned_user_ids = task_data.get("assigned_user_ids")
            status = task_data.get("status")
            due = task_data.get("due")
            
            try:
                project = Project.objects.get(id=project_id)
                users = User.objects.filter(id__in=assigned_user_ids)
                
                new_task = Task.objects.create(
                    task_name=task_name,
                    project=project,
                    status=status,
                    due=due
                )
                new_task.assign.set(users)  # 多对多字段赋值
                new_task.save()
                print(f"Task '{task_name}' created successfully.")
            except Project.DoesNotExist:
                print(f"Project with id {project_id} not found.")
            except User.DoesNotExist:
                print(f"One or more users with the specified ids were not found.")

    elif operation == 'update' and task_id:
        # 更新任务
        try:
            task = Task.objects.get(id=task_id)
            task.task_name = task_info.get("task_name", task.task_name)
            task.status = task_info.get("status", task.status)
            task.due = task_info.get("due", task.due)
            
            # 更新分配的用户
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
        # 删除任务
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            print(f"Task '{task_id}' deleted successfully.")
        except Task.DoesNotExist:
            print(f"Task with id {task_id} not found.")
    else:
        print(f"Invalid operation: {operation}")


# 调用方法
update_task_from_txt('assistant_reply1.txt')
