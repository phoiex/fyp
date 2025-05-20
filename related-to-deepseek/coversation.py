from openai import OpenAI
import time
import traceback
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Initialize the OpenAI API client
client = OpenAI(api_key="sk-ac745008ee204352b31db43a04f483a3", base_url="https://api.deepseek.com")
import os



# Get and print the current working directory
current_directory = os.getcwd()
print(f"The current working directory is: {current_directory}")

# The file path to monitor
file_path = "update_log.txt"

# Initialize the message history list
messages = []

# Add initialized system messages to messages
messages.append({
    "role": "system",
    "content": (
        "You are an HTML assistant, and your goal is to generate an HTML page of a software engineering management report based on the information provided by the user. Remember, only the HTML code format is returned, not any other content.\n"
        "The report should include the following:\n\n"
        "1. Page header: Contains the title <h1>Project Plan & Management> and is styled with a blue background and white text.\n"
        "2. Project planning section: includes project introduction, project timeline, project milestones, and deliverables list.\n"
        "3. Task table section: The table should list the task number, task description, responsible person, deadline and task status.\n"
        "4. Project management methods section: Provides a list of roles and responsibilities, communication and collaboration methods, and risk management and mitigation measures.\n"
        "5. Use mermaid charts: including Gantt charts, roles and responsibilities charts, risk management charts, system architecture charts, etc. You can choose to add a few images according to your specific data needs, and there is no need to force them.\n"
        "6. Page style: The page background color is light gray, the table border is thin gray, the header background color is blue, and the font is simple.\n\n"
        "Here is an example of a mermaid chart for reference:\n\n"
        "<div class='content'>\n"
        "    <section id='gantt-chart' style='display: block;'>\n"
        "        <h2>Project Timeline - Gantt Chart</h2>\n"
        "        <div class='mermaid'>\n"
        "            gantt\n"
        "                title Project planning timeline\n"
        "                dateFormat  YYYY-MM-DD\n"
        "                section Phase 1: Requirements and Design\n"
        "                Requirements gathering       :a1, 2025-03-01, 3d\n"
        "                Wireframe Design     :a2, after a1, 5d\n"
        "                section Phase 2: Development\n"
        "                Task creation function   :b1, 2025-03-04, 3d\n"
        "                Task management function   :b2, after b1, 4d\n"
        "                section Phase 3: Testing and Deployment\n"
        "                User acceptance testing   :c1, 2025-03-15, 4d\n"
        "                Bug Repair and deploy :c2, after c1, 3d\n"
        "                Documentation and Handover     :c3, 2025-03-22, 3d\n"
        "        </div>\n"
        "    </section>\n"
        "    <section id='roles'>\n"
        "        <h2>Roles and Responsibilities</h2>\n"
        "        <div class='mermaid'>\n"
        "            graph LR\n"
        "                A[project manager] --> B[Development manager]\n"
        "                A --> C[designer]\n"
        "                A --> D[QA testing]\n"
        "                B --> E[Front-end development]\n"
        "                B --> F[backend development]\n"
        "                C --> G[UI/UX Designer]\n"
        "                D --> H[test engineer]\n"
        "        </div>\n"
        "    </section>\n"
        "    <section id='risks'>\n"
        "        <h2>risk management</h2>\n"
        "        <div class='mermaid'>\n"
        "            graph TD\n"
        "                A[Risk 1: Design Delays] --> B[Mitigation: Start early and keep communicating]\n"
        "                A --> C[Mitigation: Cross-sector collaboration]\n"
        "                D[Risk 2: Local storage technology issues] --> E[Mitigation: Use open source libraries]\n"
        "                D --> F[Mitigation: Refer to the documentation]\n"
        "                G[Risk 3: Time constraints] --> H[Mitigation: Prioritize core functionality]\n"
        "                G --> I[Mitigation: Adopting Agile Methods]\n"
        "                J[Risk 4: UI does not meet expectations] --> K[Mitigation: Early User Feedback]\n"
        "                J --> L[Mitigation: Iterative Design]\n"
        "        </div>\n"
        "    </section>\n"
        "    <section id='architecture'>\n"
        "        <h2>System architecture</h2>\n"
        "        <div class='mermaid'>\n"
        "            graph TB\n"
        "                A[user interface] --> B[React]\n"
        "                B --> C[Node.js backend]\n"
        "                C --> D[MongoDB Database]\n"
        "                B --> E[JWT authentication]\n"
        "                E --> F[Secure session management]\n"
        "        </div>\n"
        "    </section>\n"
        "    <section id='support'>\n"
        "        <h2>Later support</h2>\n"
        "        <div class='mermaid'>\n"
        "            graph LR\n"
        "                A[Later support] --> B[Bug fix]\n"
        "                A --> C[User support]\n"
        "                A --> D[Performance monitoring]\n"
        "                B --> E[small improvement]\n"
        "                C --> F[Dedicated support team]\n"
        "                D --> G[Regular system updates]\n"
        "        </div>\n"
        "    </section>\n"
        "    <section id='sequence'>\n"
        "        <h2>User Interaction - Sequence Diagram</h2>\n"
        "        <div class='mermaid'>\n"
        "            sequenceDiagram\n"
        "                participant U as user\n"
        "                participant A as application\n"
        "                participant S as server\n"
        "                participant D as database\n"
        "                U->>A: Send login request\n"
        "                A->>S: Verify user credentials\n"
        "                S->>D: Get user data\n"
        "                D->>S: Return user data\n"
        "                S->>A: Send verification response\n"
        "                A->>U: Show user dashboard\n"
        "        </div>\n"
        "    </section>\n"
        "</div>"
    )
})
# Functions for interacting with the DeepSeek API
def interact_with_deepseek(messages):
    try:
        print("Call the DeepSeek API to get the model's answer...")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )

        assistant_reply = response.choices[0].message.content
        print(f"DeepSeek Assistant: {assistant_reply}")

        messages.append({"role": "assistant", "content": assistant_reply})

        try:
            with open("assistant_reply2.txt", "w", encoding="utf-8") as file:
                file.write(assistant_reply)
            print(f"Assistant's reply has been saved as 'assistant_reply2.txt'")
        except Exception as e:
            print(f"Error saving text: {e}")
            traceback.print_exc()

        return messages
    except Exception as e:
        print(f"Error interacting with the DeepSeek API: {e}")
        traceback.print_exc()  # Print detailed error information

import os

# Create a file system event processing class
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"File modification detected: {event.src_path}")
        
        # Check if event.src_path is a file and if it is the target file
        if os.path.isfile(event.src_path) and event.src_path.endswith(file_path):
            # When a file is modified, read the new content
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    file_content = file.read().strip()
                    if file_content:
                        print(f"File content: {file_content}")
                        # Add new content as user message to message history
                        messages.append({"role": "user", "content": file_content})
                        print(f"File content has been sent to DeepSeek: {file_content}")
                        interact_with_deepseek(messages)
                    else:
                        print("The file content is empty and was not sent to DeepSeek。")
            except Exception as e:
                print(f"Error reading file: {e}")
                traceback.print_exc()
        else:
            print()



# Initialize file change observer
def start_watching():
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)  # Monitor the current directory
    observer.start()
    print("# Monitor the current directory")

    try:
        while True:
            time.sleep(1)  # Monitor the current directory
    except KeyboardInterrupt:
        observer.stop()
        print("Stop monitoring a file.")
    observer.join()

# Start file monitoring
start_watching()
