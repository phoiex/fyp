from openai import OpenAI
import time
import traceback
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

# 初始化 OpenAI API 客户端
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# 获取并打印当前工作目录
current_directory = os.getcwd()
print(f"当前工作目录是: {current_directory}")

# 要监听的文件路径
file_path = "update_log.txt"  # 替换为你想监听的文件路径

# 初始化消息历史列表
messages = []

# 向 messages 中添加初始化的系统消息
messages.append({
    "role": "system",
    "content": (
        "你是一个 HTML 助手，目标是根据用户提供的信息生成一个软件工程管理报告的 HTML 页面。记住，只返回html代码的格式，不要其他任何内容"
        "报告应该包含以下内容：\n\n"
        "1. 页面头部：包含标题 <h1>Project Plan & Management>，并且样式为蓝色背景和白色文字。\n"
        "2. 项目计划部分：包含项目介绍，项目时间表，项目里程碑，交付物清单。\n"
        "3. 任务表部分：表格应列出任务编号、任务描述、责任人、截止日期和任务状态。\n"
        "4. 项目管理方法部分：提供角色与职责列表，沟通与协作方式，风险管理与缓解措施。\n"
        "5. 使用 mermaid 图表：包括 Gantt 图、角色与职责图、风险管理图、系统架构图等。根据具体数据需求选择添加某几个图像就行，不需要强行添加\n"
        "6. 页面样式：页面背景色为浅灰色，表格的边框为细灰色，表头的背景色为蓝色，字体简洁。\n\n"
        "以下是一个参考的 mermaid 图表示例：\n\n"
        "<div class='content'>\n"
        "    <section id='gantt-chart' style='display: block;'>\n"
        "        <h2>项目时间表 - Gantt 图</h2>\n"
        "        <div class='mermaid'>\n"
        "            gantt\n"
        "                title 项目计划时间表\n"
        "                dateFormat  YYYY-MM-DD\n"
        "                section 第一阶段：需求与设计\n"
        "                需求收集       :a1, 2025-03-01, 3d\n"
        "                线框图设计     :a2, after a1, 5d\n"
        "                section 第二阶段：开发\n"
        "                任务创建功能   :b1, 2025-03-04, 3d\n"
        "                任务管理功能   :b2, after b1, 4d\n"
        "                section 第三阶段：测试与部署\n"
        "                用户验收测试   :c1, 2025-03-15, 4d\n"
        "                Bug 修复与部署 :c2, after c1, 3d\n"
        "                文档与交接     :c3, 2025-03-22, 3d\n"
        "        </div>\n"
        "    </section>\n"
        "    <section id='roles'>\n"
        "        <h2>角色与职责</h2>\n"
        "        <div class='mermaid'>\n"
        "            graph LR\n"
        "                A[项目经理] --> B[开发负责人]\n"
        "                A --> C[设计师]\n"
        "                A --> D[QA 测试]\n"
        "                B --> E[前端开发]\n"
        "                B --> F[后端开发]\n"
        "                C --> G[UI/UX 设计师]\n"
        "                D --> H[测试工程师]\n"
        "        </div>\n"
        "    </section>\n"
        "    <section id='risks'>\n"
        "        <h2>风险管理</h2>\n"
        "        <div class='mermaid'>\n"
        "            graph TD\n"
        "                A[风险 1: 设计延迟] --> B[缓解: 提前启动、保持沟通]\n"
        "                A --> C[缓解: 跨部门合作]\n"
        "                D[风险 2: 本地存储技术问题] --> E[缓解: 使用开源库]\n"
        "                D --> F[缓解: 参考文档]\n"
        "                G[风险 3: 时间紧迫] --> H[缓解: 优先核心功能]\n"
        "                G --> I[缓解: 采用敏捷方法]\n"
        "                J[风险 4: UI 不符合预期] --> K[缓解: 提前用户反馈]\n"
        "                J --> L[缓解: 迭代设计]\n"
        "        </div>\n"
        "    </section>\n"
        "    <section id='architecture'>\n"
        "        <h2>系统架构</h2>\n"
        "        <div class='mermaid'>\n"
        "            graph TB\n"
        "                A[用户界面] --> B[React]\n"
        "                B --> C[Node.js 后端]\n"
        "                C --> D[MongoDB 数据库]\n"
        "                B --> E[JWT 认证]\n"
        "                E --> F[安全会话管理]\n"
        "        </div>\n"
        "    </section>\n"
        "    <section id='support'>\n"
        "        <h2>后期支持</h2>\n"
        "        <div class='mermaid'>\n"
        "            graph LR\n"
        "                A[后期支持] --> B[Bug 修复]\n"
        "                A --> C[用户支持]\n"
        "                A --> D[性能监控]\n"
        "                B --> E[小幅改进]\n"
        "                C --> F[专门支持团队]\n"
        "                D --> G[定期系统更新]\n"
        "        </div>\n"
        "    </section>\n"
        "    <section id='sequence'>\n"
        "        <h2>用户交互 - 时序图</h2>\n"
        "        <div class='mermaid'>\n"
        "            sequenceDiagram\n"
        "                participant U as 用户\n"
        "                participant A as 应用\n"
        "                participant S as 服务器\n"
        "                participant D as 数据库\n"
        "                U->>A: 发送登录请求\n"
        "                A->>S: 验证用户凭据\n"
        "                S->>D: 获取用户数据\n"
        "                D->>S: 返回用户数据\n"
        "                S->>A: 发送验证响应\n"
        "                A->>U: 显示用户仪表盘\n"
        "        </div>\n"
        "    </section>\n"
        "</div>"
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
            with open("assistant_reply2.txt", "w", encoding="utf-8") as file:
                file.write(assistant_reply)
            print(f"助手的回复已保存为 'assistant_reply2.txt'")
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
