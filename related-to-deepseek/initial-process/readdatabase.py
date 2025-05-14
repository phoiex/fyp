import os
import sys
import django
from django.apps import apps

# 将项目根目录添加到 sys.path 中，确保 Django 可以找到 manager/settings.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# 设置 Django 的 settings 模块路径
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')

# 初始化 Django 环境
django.setup()

# 定义我们关心的模型名称（只关心 'Project' 和 'Task'）
target_models = [
    'projects.project',  # Project 模型
    'projects.ProjectDetails'  # Task 模型
]

# 保存所有模型数据到txt文件（覆盖旧文件）
def save_data_to_txt(data):
    with open("classproject.txt", "w", encoding="utf-8") as file:
        for record in data:
            file.write(str(record) + "\n")
    print("Data saved to classproject.txt")

# 查询所有模型数据并保存到文件
def check_for_updates():
    all_data = []
    for model_name in target_models:
        try:
            # 获取模型
            model = apps.get_model(model_name)
            print(f"Checking updates for Model: {model.__name__}")

            # 获取模型的所有数据
            data = model.objects.all().values()
            if data:
                all_data.extend(data)  # 将所有数据添加到 all_data 列表中
            else:
                print(f"No data found in model {model.__name__}")

        except LookupError:
            print(f"Model '{model_name}' not found.")
    
    # 保存所有模型的数据到 txt 文件
    if all_data:
        save_data_to_txt(all_data)


# 程序启动后立即执行数据库检查
if __name__ == "__main__":
    check_for_updates()