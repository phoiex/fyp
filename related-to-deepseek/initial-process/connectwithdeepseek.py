from openai import OpenAI
import time
import traceback
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 初始化 OpenAI API 客户端
client = OpenAI(api_key="sk-ac745008ee204352b31db43a04f483a3", base_url="https://api.deepseek.com")
import os



# 获取并打印当前工作目录
current_directory = os.getcwd()
print(f"当前工作目录是: {current_directory}")

# 要监听的文件路径
file_path = "classproject.txt"  # 替换为你想监听的文件路径

# 初始化消息历史列表
messages = []

# 向 messages 中添加初始化的系统消息
messages.append({
    "role": "system",
    "content": (
        "你是一个 Django 数据库助手，目标是根据用户提供的项目（project）信息生成一条或者多条数据库中的任务（task）信息。"
        "一般来说，一个项目由多个任务共同完成。记住，只返回符合格式的数据，不要其他任何内容。"
        "每个任务之间用逗号隔开。\n\n"
        "返回数据应该包含以下内容：\n"
        "{\n"
        "  \"operation\": \"create\",  # 或者 'update' 或 'delete'，根据用户要求进行相应的操作\n"
        "  \"tasks\": [\n"
        "    {\n"
        "      \"task_name\": \"New Task Name\",  # 任务名称\n"
        "      \"project_id\": 1,                # 项目ID\n"
        "      \"assigned_user_ids\": [1, 2],    # 分配给哪些用户（用户ID列表）\n"
        "      \"status\": \"2\",                # 任务状态：\"1\" => \"Stuck\", \"2\" => \"Working\", \"3\" => \"Done\"\n"
        "      \"due\": \"1\"                   # 截止日期状态：\"1\" => \"On Due\", \"2\" => \"Overdue\", \"3\" => \"Done\"\n"
        "    },\n"
        "    {\n"
        "      \"task_name\": \"Another Task\",  # 第二个任务的任务名称\n"
        "      \"project_id\": 1,                # 项目ID\n"
        "      \"assigned_user_ids\": [3, 4],    # 第二个任务的分配用户ID列表\n"
        "      \"status\": \"3\",                # 第二个任务的状态\n"
        "      \"due\": \"3\"                    # 第二个任务的截止日期状态\n"
        "    }\n"
        "  ],\n"
        "  \"task_id\": 1  # 仅在 'update' 或 'delete' 操作时需要（任务ID）\n"
        "}\n"
        "注意：\n"
        "- 如果是 'create' 操作，请返回任务信息列表，每个任务是一个字典。\n"
        "- 如果是 'update' 操作，请返回需要更新的任务及其 ID。\n"
        "- 如果是 'delete' 操作，请返回要删除任务的 ID。\n"
    )
})


# 与 DeepSeek API 交互的函数
def interact_with_deepseek(messages):
    try:
        print("调用 DeepSeek API 获取模型的回答...")  # 添加调试输出
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )

        assistant_reply = response.choices[0].message.content
        print(f"DeepSeek Assistant: {assistant_reply}")

        messages.append({"role": "assistant", "content": assistant_reply})

        try:
            with open("assistant_reply1.txt", "w", encoding="utf-8") as file:
                file.write(assistant_reply)
            print(f"助手的回复已保存为 'assistant_reply1.txt'")
        except Exception as e:
            print(f"保存文本时出错: {e}")
            traceback.print_exc()

        return messages
    except Exception as e:
        print(f"与 DeepSeek API 交互时出错: {e}")
        traceback.print_exc()  # 打印详细错误信息

import os

# 创建文件系统事件处理类
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"检测到文件修改: {event.src_path}")
        
        # 检查 event.src_path 是否为文件，以及是否是目标文件
        if os.path.isfile(event.src_path) and event.src_path.endswith(file_path):
            # 文件被修改时，读取新的内容
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    file_content = file.read().strip()
                    if file_content:
                        print(f"文件内容: {file_content}")  # 打印文件内容
                        # 将新的内容作为用户消息添加到消息历史
                        messages.append({"role": "user", "content": file_content})
                        print(f"文件内容已发送给 DeepSeek: {file_content}")
                        interact_with_deepseek(messages)
                    else:
                        print("文件内容为空，未发送到 DeepSeek。")
            except Exception as e:
                print(f"读取文件时出错: {e}")
                traceback.print_exc()
        else:
            print()



# 初始化文件变更观察者
def start_watching():
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)  # 监视当前目录
    observer.start()
    print("开始监视文件变化...")

    try:
        while True:
            time.sleep(1)  # 保持程序运行
    except KeyboardInterrupt:
        observer.stop()
        print("停止监视文件。")
    observer.join()

# 启动文件监控
start_watching()
