import subprocess
import multiprocessing
import os

def run_monitoring_script(script_name):
    """Runs the given Python monitoring script"""
    try:
        # Get the absolute path of the current directory
        current_directory = os.getcwd()
        print(current_directory)
        # Combine folder path with file name
        script_directory = os.path.join(current_directory, "related-to-deepseek")
        script_path = os.path.join(script_directory, script_name)
        
        print(f"Start the monitoring script:{script_path}")
        subprocess.run(["python", script_path], check=True)
    except Exception as e:
        print(f"run script {script_name} error: {e}")

if __name__ == "__main__":

    script_names = ["aiweb.py",  "coversation.py"]

    processes = []
    for script in script_names:
        process = multiprocessing.Process(target=run_monitoring_script, args=(script,))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    print("All file monitoring programs are enabled.")
