import subprocess
import multiprocessing
import os

def run_monitoring_script(script_name):
    """运行给定的 Python 监控脚本"""
    try:
        # 获取当前目录的绝对路径
        current_directory = os.getcwd()
        print(current_directory)
        # 将文件夹路径与文件名组合
        script_directory = os.path.join(current_directory, "related-to-deepseek")
        script_path = os.path.join(script_directory, script_name)
        
        print(f"启动监控脚本：{script_path}")
        subprocess.run(["python", script_path], check=True)
    except Exception as e:
        print(f"运行脚本 {script_name} 时出错: {e}")

if __name__ == "__main__":

    script_names = ["aiweb.py",  "coversation.py"]

    processes = []
    for script in script_names:
        process = multiprocessing.Process(target=run_monitoring_script, args=(script,))
        processes.append(process)
        process.start()

    # 等待所有进程结束
    for process in processes:
        process.join()

    print("所有文件监控程序已启动。")
