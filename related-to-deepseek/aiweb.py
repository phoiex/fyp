import time
import traceback
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 文件路径
html_file_path = "aiweb.html"
txt_file_path = "assistant_reply2.txt"

def clear_html_file():
    try:
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write('<start>\n\n<finish>')  # 清空并插入 <start> 和 <finish> 标签
        print("文件已清除。")
    except Exception as e:
        print(f"清空文件时发生错误：{e}")
        traceback.print_exc()

# 创建文件系统事件处理类
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # 检查是否是目标文件（.txt文件）
        if event.src_path.endswith(txt_file_path):
            print(f"{txt_file_path} 被修改，更新 HTML 文件...")
            clear_html_file()  # 清空 txt 文件内容
            try:
                # 读取 txt 文件内容
                with open(txt_file_path, "r", encoding="utf-8") as txt_file:
                    txt_content = txt_file.read()

                # 读取 HTML 文件
                with open(html_file_path, "r", encoding="utf-8") as html_file:
                    html_content = html_file.read()

                # 找到 <start> 和 <finish> 的位置
                start_pos = html_content.find('<start>')
                finish_pos = html_content.find('<finish>')

                # 确保找到 <start> 和 <finish> 标签并进行替换
                if start_pos != -1 and finish_pos != -1:
                    html_content = html_content.replace("<start>", f"<start>{txt_content}")  # 插入 .txt 内容

                    # 保存修改后的 HTML 文件
                    with open(html_file_path, "w", encoding="utf-8") as html_file:
                        html_file.write(html_content)

                    print("HTML 文件更新成功！")
                else:
                    print("未找到 <start> 和 <finish> 标签，无法更新 HTML 文件。")
            except Exception as e:
                print(f"发生错误：{e}")
                traceback.print_exc()

# 初始化文件变更观察者
def start_watching():
    clear_html_file()  # 清空 txt 文件内容
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
