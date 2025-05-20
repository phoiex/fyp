from openai import OpenAI
import time
import traceback
import os
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

# Initialize the OpenAI API client
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# Initialize vector database
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={'device': 'cpu'}
)
db_dir = os.path.join(os.path.dirname(__file__), "./chroma_db")
vectordb = Chroma(persist_directory=db_dir, embedding_function=embedding_model)


# Get and print the current working directory
current_directory = os.getcwd()
print(f"The current working directory is: {current_directory}")

# File path to monitor
file_path = "classproject.txt"  # Replace with the file path you want to monitor

# Initialize the message history list
messages = []

# Interact with DeepSeek and generate JSON output
def interact_with_deepseek(messages):
    # Vector retrieval context
    docs = vectordb.similarity_search(messages, k=10)
    context = "\n\n".join(doc.page_content for doc in docs)

    # Add initialized system messages to messages
    messages.append({
        "role": "system",
        "content": (
            "You are a web project management expert, primarily responsible for assisting clients in generating the development process for web projects. Based on the information provided by the client, you need to create a structured web development workflow. Do not generate any text other than the required content.\n\n"
            "The client's input information includes the following:\n"
            "1. Problem Statement: A clear description of the core issue or need that the project aims to solve. It explains why the project is being undertaken.\n"
            "2. Project Objectives: Specific, measurable outcomes that the project aims to achieve. For example, “Develop a system that supports 1,000 concurrent users.”\n"
            "3. Project Scope: Defines what is included and what is excluded in the project. It sets the boundaries of the work to be done.\n"
            "4. Goals: Broad, long-term aspirations or desired outcomes, such as “Improve customer satisfaction” or “Enhance user experience.”\n"
            "5. Assumptions: Conditions believed to be true for planning purposes, though they may carry uncertainty. For example, “Assume users will access the system no more than 8 hours per day.”\n"
            "6. Constraints: A limitation or restriction that the project must operate within. Common constraints include time, budget, and resources.\n\n"
            "After collecting the above information, the first thing you need to do is determine the required number of developers. Each developer should have a designated job title and will be assigned specific tasks in the project development process. If customer provide the developers that they have, you have to decide whether the number of developers is enough. If customer do not have enough developers, you have to show it in your plan.\n"
            "It is important to note that, whenever possible, you should minimize the number of developers as long as there are no scheduling conflicts, ensuring efficient utilization of available personnel.\n"
            "Additionally, you need to consider what resources are required for the project development. These resources will also be allocated accordingly in the project development process.\n\n"
            "After determining the required personnel and resources, you need to generate the project development process.  When generating the project development process, please follow the format below:\n"
            "Sbutitle 1: Task Name - The name of the development phase.\n"
            "Subtitle 2: Task Description - A brief explanation of what this phase entails.\n"
            "Subtitle 3: Assigned User ID - The email address of the developer to whom the task is assigned. Can be empty if don't know.\n"
            "Subtitle 4: Start Date - The start date of this process.\n"
            "Subtitle 5: End Date - The end date of this process.\n"
            "Subtitle 6: Status - Task status: 1 => Stuck, 2 => Working, 3 => Done.\n"
            "Subtitle 7: Due - Due Date Status: 1 => On Due, 2 => Overdue, 3 => Done.\n"
            "When deciding the start and end dates of each phase, you can assume that the first phase begins on the same day the client submits their requirements. And also you need to use ISO 8601 Date and Time Format to write the start date and end date (e.g. 2018-04-13T00:42:19.284Z). You can assume that people start working at 9:00 every morning and finish working at 17:00 every evening.\n\n"
            "After confirming the project development process, you need to identify the risks associated with each step. These risks should include both the potential issues within the current phase and their impact on the subsequent phases. Then, add the risk assessment for each step under the Subtitle of the corresponding process.\n\n"
            "While considering the entire development process, I will provide you with some reference materials. You can use these references along with the client's requirements to generate the project workflow.\n"
            # f"Context:\n{context}\n\n"
            "Most importantly: your output must follow this exact JSON format (do not explain anything):\n"
            "{\n"
            "  \"operation\": \"create\", # Or 'update' or 'delete', perform corresponding operations according to user requirements\n"
            "  \"tasks\": [\n"
            "    {\n"
            "      \"task_name\": \"New Task Name\", # Task name\n"
            "      \"task_description\": \"The Description of Task Description\", # Task description\n"
            "      \"project_id\": 1, # Project ID\n"
            "      \"assigned_user_ids\": [1, 2], #Assigned to which users (user ID list)\n"
            "      \"start_date\": \"2023-10-01T09:00:00.000Z\", # Start date\n"
            "      \"due_date\": \"2023-10-31T17:00:00.000Z\", # due date\n"
            "      \"status\": \"2\", #Task status: \"1\" => \"Stuck\", \"2\" => \"Working\", \"3\" => \"Done\"\n"
            "      \"due\": \"1\" #Due date status: \"1\" => \"On Due\", \"2\" => \"Overdue\", \"3\" => \"Done\"\n"
            "    }\n"
            "    {\n"
            "      \"task_name\": \"New Task Name\", # The name of the second task\n"
            "      \"task_description\": \"The Description of the second Task Description\", # The description of the second task\n"
            "      \"project_id\": 1, # Project ID\n"
            "      \"assigned_user_ids\": [3, 3], # List of assigned user IDs for the second task\n"
            "      \"start_date\": \"2024-10-01T09:00:00.000Z\", # The start date of the second task\n"
            "      \"due_date\": \"2024-10-31T17:00:00.000Z\", # The due date of the second task\n"
            "      \"status\": \"3\", # Status of the second task\n"
            "      \"due\": \"3\" # The second task's deadline status\n"
            "    }\n"
            "  ],\n"
            "  \"task_id\": 1 # Only required for 'update' or 'delete' operations (task id)\n"
            "}\n"
            "Only return the JSON output – do not explain anything else.\n"
            "Note:\n"
            "- If it is a 'create' operation, please return a list of task information, each task is a dictionary.\n"
            "- If it is an 'update' operation, please return the task to be updated and its ID.\n"
            "- If it is a 'delete' operation, please return the ID of the task to be deleted.\n"
        )},
    )



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
                        print(f"File content: {file_content}")  # Print file contents
                        # Add new content as a user message to the message history
                        interact_with_deepseek(messages)
                        messages.append({"role": "user", "content": file_content})
                        print(f"File content has been sent to DeepSeek: {file_content}")
                        

                        try:
                            # Call the DeepSeek Reasoner model
                            response = client.chat.completions.create(
                                model="deepseek-reasoner",
                                messages=messages,
                                stream=False
                            )

                            assistant_reply = response.choices[0].message.content.strip()
                            print(f"DeepSeek Assistant: {assistant_reply}")

                            messages.append({"role": "assistant", "content": assistant_reply})

                            try:
                                with open("assistant_reply1.txt", "w", encoding="utf-8") as file:
                                    file.write(assistant_reply)
                                print(f"Reply has been saved as 'assistant_reply1.txt'")
                            except Exception as e:
                                print(f"Error saving text: {e}")
                                traceback.print_exc()

                        except Exception as e:
                            print(f"Error interacting with the DeepSeek API: {e}")
                            traceback.print_exc()



                    else:
                        print("The file content is empty and not sent to DeepSeek.")
            except Exception as e:
                print(f"Error reading file:{e}")
                traceback.print_exc()
        else:
            print()



# Initialize file change observer
def start_watching():
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False) # Monitor the current directory
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