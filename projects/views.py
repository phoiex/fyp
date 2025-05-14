from django.shortcuts import render
from django.db.models import Avg
from register.models import Project
from projects.models import Task
from projects.forms import TaskRegistrationForm
from projects.forms import ProjectRegistrationForm

# Create your views here.
def projects(request):
    projects = Project.objects.all()
    avg_projects = Project.objects.all().aggregate(Avg('complete_per'))['complete_per__avg']
    tasks = Task.objects.all()
    overdue_tasks = tasks.filter(due='2')
    context = {
        'avg_projects' : avg_projects,
        'projects' : projects,
        'tasks' : tasks,
        'overdue_tasks' : overdue_tasks,
    }
    return render(request, 'projects/projects.html', context)

def newTask(request):
    if request.method == 'POST':
        form = TaskRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            context = {
                'created': created,
                'form': form,
            }
            return render(request, 'projects/new_task.html', context)
        else:
            return render(request, 'projects/new_task.html', context)
    else:
        form = TaskRegistrationForm()
        context = {
            'form': form,
        }
        return render(request,'projects/new_task.html', context)

from django.shortcuts import render, redirect
from .forms import ProjectRegistrationForm


def newProject(request):
    if request.method == 'POST':
        form = ProjectRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # 保存表单数据

            # 使用绝对路径进行重定向
            return redirect('/projects/project-details/')  # 绝对路径

        else:
            # 表单无效，返回同一页面，显示错误
            context = {'form': form}
            return render(request, 'projects/new_project.html', context)
    
    else:
        # 初始访问页面时显示空表单
        form = ProjectRegistrationForm()
        context = {'form': form}
        return render(request, 'projects/new_project.html', context)

 # projects/views.py

from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .models import Project, Task
from .forms import TaskForm


def project_overview(request):
    projects = Project.objects.all().prefetch_related('task_set', 'assign')

    if request.method == 'POST':
        
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id=task_id)
       
        task_form = TaskForm(request.POST, instance=task)

        if task_form.is_valid():  
            task_form.save()  
            return redirect('projects:project_overview')  

    return render(request, 'projects/project_overview.html', {'projects': projects})


from django.shortcuts import render, redirect
from .forms import ProjectDetailsForm
from .models import Project

def project_details_view(request):
    if request.method == 'POST':
        form = ProjectDetailsForm(request.POST)
        if form.is_valid():
            form.save()  # 保存项目详情
            return redirect('/projects/projects-edit')
    else:
        form = ProjectDetailsForm()

    return render(request, 'projects/project_details_form.html', {'form': form})





from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, ProjectDetails, Task
from .forms import ProjectForm, TaskForm, ProjectDetailsFormedit
from django.contrib.auth.decorators import login_required

@login_required
def project_detail_edit(request):
# 获取所有项目
    projects = Project.objects.all()
    project_data = []

    for project in projects:
        project_details = ProjectDetails.objects.get(project=project)
        tasks = Task.objects.filter(project=project)
        
        # 处理表单提交
        if request.method == 'POST':
            # 为每个项目创建表单实例
            project_form = ProjectForm(request.POST, instance=project)
            project_details_form = ProjectDetailsFormedit(request.POST, instance=project_details)
            task_forms = {task.id: TaskForm(request.POST, instance=task) for task in tasks}

            if project_form.is_valid() and project_details_form.is_valid() and all(task_form.is_valid() for task_form in task_forms.values()):
                project_form.save()
                project_details_form.save()
                for task_form in task_forms.values():
                    task_form.save()
               
        else:
            # 在初次加载页面时创建表单实例
            project_form = ProjectForm(instance=project)
            project_details_form = ProjectDetailsFormedit(instance=project_details)
            task_forms = {task.id: TaskForm(instance=task) for task in tasks}

        # 保存项目数据和表单
        project_data.append({
            'project': project,
            'project_details': project_details,
            'tasks': tasks,
            'project_form': project_form,
            'project_details_form': project_details_form,
            'task_forms': task_forms,
        })

    context = {'project_data': project_data}
    return render(request, 'projects/project_detail.html', context)




# views.py
from django.shortcuts import render, redirect
from .forms import ProjectedInfoForm

def projected_info_add(request):
    if request.method == 'POST':
        form = ProjectedInfoForm(request.POST)
        if form.is_valid():
            # 保存表单数据
            form.save()
            return redirect('projects:projects')  # 提交后跳转到项目列表页面
    else:
        form = ProjectedInfoForm()
    
    return render(request, 'projects/projected_info_add.html', {'form': form})



import subprocess
from django.shortcuts import render
from django.http import HttpResponse

# 视图函数来处理表单提交
def run_scripts(request):
    if request.method == "POST":
        try:
            # 运行 editdatabase.py
            subprocess.run(["python", "path_to_your_script/editdatabase.py"], check=True)

            # 运行 run-2.py
            subprocess.run(["python", "path_to_your_script/run-2.py"], check=True)

            return HttpResponse("脚本运行成功！")
        except subprocess.CalledProcessError as e:
            return HttpResponse(f"运行失败: {e}")

    return render(request, 'projects/project_details_form.html')


from openpyxl import Workbook
from django.shortcuts import render
from .models import Project, Task
import os

from django.shortcuts import render
from openpyxl import Workbook
import os
from .models import Project, Task, ProjectDetails, ProjectedInfo

def export_tasks_excel(request):
    # 获取所有项目，用于选择
    projects = Project.objects.all()

    if request.method == 'POST':
        project_id = request.POST.get('project')
        project = Project.objects.get(id=project_id)

        # 查询对应项目的任务
        tasks = Task.objects.filter(project=project)

        # 创建一个新的 Excel 工作簿
        wb = Workbook()
        ws = wb.active
        ws.title = 'Tasks'

        # 写入标题行
        ws.append(['Task Name', 'Assign', 'Status', 'Due'])

        # 将任务信息写入工作簿
        for task in tasks:
            assign_users = ', '.join([user.username for user in task.assign.all()])
            ws.append([task.task_name, assign_users, task.status, task.due])

        # 设置文件保存路径
        save_path = r"C:\Users\17905\Desktop\acdemic\UM\FYP\project-management-system-master\tranexcel.xlsx"

        # 确保目录存在
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # 保存到指定路径
        wb.save(save_path)

        # 给出一个提示，返回导出成功的页面
        return render(request, 'projects/select_project.html', {'projects': projects, 'message': 'Tasks exported to Excel successfully.'})

    return render(request, 'projects/select_project.html', {'projects': projects})

def export_tasks_txt(request):
    # 获取所有项目，用于选择
    projects = Project.objects.all()

    if request.method == 'POST':
        project_id = request.POST.get('project')
        project = Project.objects.get(id=project_id)

        # 查询对应项目的任务
        tasks = Task.objects.filter(project=project)

        # 创建一个新的 TXT 文件，保存项目相关信息和任务
        txt_save_path = r"C:\Users\17905\Desktop\acdemic\UM\FYP\project-management-system-master\update_log.txt"
        with open(txt_save_path, 'w') as f:
            # 写入项目基本信息
            f.write(f"Project Name: {project.name}\n")
            f.write(f"Project Description: {project.description}\n")
            f.write(f"Deadline: {project.dead_line}\n")
            f.write(f"Company: {project.company.name}\n\n")

            # 写入 ProjectDetails（如果有）
            try:
                project_details = ProjectDetails.objects.get(project=project)
                f.write(f"Problem Statement: {project_details.problem_statement}\n")
                f.write(f"Project Objectives: {project_details.project_objectives}\n")
                f.write(f"Project Scope: {project_details.project_scope}\n")
                f.write(f"Goals: {project_details.goals}\n")
                f.write(f"Assumptions: {project_details.assumptions}\n")
                f.write(f"Constraints: {project_details.constraints}\n\n")
            except ProjectDetails.DoesNotExist:
                f.write("No Project Details available\n\n")

            # 写入 ProjectedInfo（如果有）
            try:
                projected_info = ProjectedInfo.objects.get(project=project)
                f.write(f"Business Process: {projected_info.business_process}\n")
                f.write(f"User Requirements: {projected_info.user_requirements}\n")
                f.write(f"Non-functional Requirements: {projected_info.non_functional_requirements}\n")
                f.write(f"User Roles/Permissions: {projected_info.user_roles_permissions}\n")
                f.write(f"System Integration: {projected_info.system_integration}\n")
                f.write(f"Technical Architecture: {projected_info.technical_architecture}\n")
                f.write(f"Data Management: {projected_info.data_management}\n")
                f.write(f"UI Interaction Design: {projected_info.ui_interaction_design}\n")
                f.write(f"Security Compliance: {projected_info.security_compliance}\n")
                f.write(f"Acceptance Criteria: {projected_info.acceptance_criteria}\n")
                f.write(f"Project Budget: {projected_info.project_budget}\n")
                f.write(f"Project Timeline: {projected_info.project_timeline}\n")
                f.write(f"Risk Management: {projected_info.risk_management}\n")
                f.write(f"Post Deployment Support: {projected_info.post_deployment_support}\n")
                f.write(f"Legal Compliance: {projected_info.legal_compliance}\n")
                f.write(f"Extra Information: {projected_info.extra_information}\n\n")
            except ProjectedInfo.DoesNotExist:
                f.write("No Projected Info available\n\n")

            # 写入任务信息
            f.write("Tasks:\n")
            for task in tasks:
                assign_users = ', '.join([user.username for user in task.assign.all()])
                f.write(f"Task Name: {task.task_name}\n")
                f.write(f"Assigned Users: {assign_users}\n")
                f.write(f"Status: {task.status}\n")
                f.write(f"Due: {task.due}\n\n")

        # 提示成功，返回导出页面
        return render(request, 'projects/select_project.html', {'projects': projects, 'message': 'AI Report updated successfully.'})

    return render(request, 'projects/select_project.html', {'projects': projects})


from django.shortcuts import render
from .models import Project

def export_tasks(request):
    # 获取所有项目，用于选择
    projects = Project.objects.all()

    # 如果是 POST 请求，用户选择了项目进行导出
    if request.method == 'POST':
        # 获取用户选择的项目 ID
        project_id = request.POST.get('project')
        project = Project.objects.get(id=project_id)

        # 可以根据选择的项目来处理导出逻辑，下面是导出 Excel 和 TXT 文件的代码
        # 这里可以调用之前定义的 export_tasks_excel 或 export_tasks_txt 函数
        # 为简便起见，可以直接重定向或返回成功消息

        return render(request, 'projects/select_project.html', {'projects': projects, 'message': 'Project selected for export.'})

    # 如果是 GET 请求，显示所有项目的选择界面
    return render(request, 'projects/select_project.html', {'projects': projects})


from django.shortcuts import render

def dual_view(request):
    return render(request, 'projects/dual_view.html')
