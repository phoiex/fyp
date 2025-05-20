import time
import traceback
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# File path
html_file_path = "aiweb.html"
txt_file_path = "assistant_reply2.txt"

def clear_html_file():
    try:
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write('<start>\n\n<finish>')  # Clear and insert <start> and <finish> tags
        print("File cleared.")
    except Exception as e:
        print(f"An error occurred while flushing the file:{e}")
        traceback.print_exc()

# Create a file system event handling class
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Check if it is the target file
        if event.src_path.endswith(txt_file_path):
            print(f"{txt_file_path} Modified, update HTML files...")
            clear_html_file()  # Clear the contents of the txt file
            try:
                # Read the contents of a txt file
                with open(txt_file_path, "r", encoding="utf-8") as txt_file:
                    txt_content = txt_file.read()

                # Read HTML file
                with open(html_file_path, "r", encoding="utf-8") as html_file:
                    html_content = html_file.read()

                # Find the position of <start> and <finish>
                start_pos = html_content.find('<start>')
                finish_pos = html_content.find('<finish>')

                # Make sure to find the <start> and <finish> tags and replace them
                if start_pos != -1 and finish_pos != -1:
                    html_content = html_content.replace("<start>", f"<start>{txt_content}")

                    # Save the modified HTML file
                    with open(html_file_path, "w", encoding="utf-8") as html_file:
                        html_file.write(html_content)

                    print("HTML File update successful!")
                else:
                    print("The <start> and <finish> tags were not found, unable to update the HTML file.")
            except Exception as e:
                print(f"Error occurs：{e}")
                traceback.print_exc()

# Initialize file change observer
def start_watching():
    clear_html_file()
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    print("Start monitoring file changes...")

    try:
        while True:
            time.sleep(1)  # Keep the program running
    except KeyboardInterrupt:
        observer.stop()
        print("Stop monitoring a file.")
    observer.join()

# Start file monitoring
start_watching()
