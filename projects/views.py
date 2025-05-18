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


from django.shortcuts import render, redirect
from .forms import ProjectRegistrationForm
from .models import Project  
import os
import json


def newProject(request):
    if request.method == 'POST':
        form = ProjectRegistrationForm(request.POST)
        if form.is_valid():
            project = form.save()  # 来来来你告诉你爸为什么这个save能报错
            project_dict = {
                'id': project.id,
                'name': project.name,
                'slug': project.slug,
                'efforts': project.efforts,
                'status': project.status,
                'dead_line': project.dead_line,
                'company_id': project.company_id,  
                'complete_per': project.complete_per,
                'description': project.description,
                'add_date': project.add_date,
                'upd_date': project.upd_date,
            }
            file_path = r'C:\Users\17905\Desktop\acdemic\UM\FYP\project-management-system-master\classproject.txt'
            with open(file_path, 'w', encoding='utf-8') as f:  
                f.write(json.dumps(project_dict, ensure_ascii=False, default=str) + '\n')

            return redirect('/projects/project-details/')
        else:
            return render(request, 'projects/new_project.html', {'form': form})
    else:
        form = ProjectRegistrationForm()
        return render(request, 'projects/new_project.html', {'form': form})


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

from django.shortcuts import render, get_object_or_404
from .models import ProjectDetails, Project, Task
from .forms import ProjectDetailsForm
import json

def project_details_view(request):
    tasks = []
    selected_project = None

    if request.method == 'POST':
        form = ProjectDetailsForm(request.POST)
        if form.is_valid():
            details = form.save()
            selected_project = details.project
            tasks = Task.objects.filter(project=selected_project).prefetch_related('assign')

            # 保存项目数据到txt
            merged_data = {
                'id': selected_project.id,
                'name': selected_project.name,
                'slug': selected_project.slug,
                'efforts': selected_project.efforts,
                'status': selected_project.status,
                'dead_line': selected_project.dead_line,
                'company_id': selected_project.company_id,
                'complete_per': selected_project.complete_per,
                'description': selected_project.description,
                'add_date': selected_project.add_date,
                'upd_date': selected_project.upd_date,
                'problem_statement': details.problem_statement,
                'project_objectives': details.project_objectives,
                'project_scope': details.project_scope,
                'goals': details.goals,
                'assumptions': details.assumptions,
                'constraints': details.constraints,
            }

            file_path = r'C:\Users\17905\Desktop\acdemic\UM\FYP\project-management-system-master\classproject.txt'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(merged_data, default=str, ensure_ascii=False) + '\n')
    else:
        form = ProjectDetailsForm()
        project_id = request.GET.get('project_id')
        if project_id:
            selected_project = get_object_or_404(Project, id=project_id)
            tasks = Task.objects.filter(project=selected_project).prefetch_related('assign')

    return render(request, 'projects/project_details_form.html', {
        'form': form,
        'tasks': tasks,
        'selected_project': selected_project,
        'projects': Project.objects.all(),  # 用于填充下拉框
    })







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
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
import os

def export_tasks_excel(request):
    from openpyxl import Workbook, load_workbook
    import os

    projects = Project.objects.all()

    if request.method == 'POST':
        project_id = request.POST.get('project')
        project = Project.objects.get(id=project_id)
        tasks = Task.objects.filter(project=project)
        planners = Planner.objects.all()  # 获取所有 Planner 数据

        save_path = r"C:\Users\17905\Desktop\acdemic\UM\FYP\test.xlsx"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # 打开或新建工作簿
        if os.path.exists(save_path):
            wb = load_workbook(save_path)
            # 清除旧工作表
            for sheet_name in ['CustomerData', 'CustomerInfo']:
                if sheet_name in wb.sheetnames:
                    wb.remove(wb[sheet_name])
            ws_data = wb.create_sheet('CustomerData')
            ws_info = wb.create_sheet('CustomerInfo')
        else:
            wb = Workbook()
            ws_data = wb.active
            ws_data.title = 'CustomerData'
            ws_info = wb.create_sheet('CustomerInfo')

        # 写 CustomerData（任务导出）
        headers_data = [
            'User ID', 'Task ID', 'Task Name', 'Assign', 'Status',
            'Due', 'Task Description', 'Start Date', 'Due Date'
        ]
        ws_data.append(headers_data)

        row_count = 0
        for i, task in enumerate(tasks, start=1):
            row_count += 1
            assign_users = task.assign.all()
            user_id = assign_users[0].id if assign_users else ''
            assign_names = ', '.join([user.username for user in assign_users]) if assign_users else ''

            row = [
                user_id if user_id != '' else 0,
                task.id if task.id else i,
                task.task_name if task.task_name else 0,
                assign_names if assign_names else 0,
                task.get_status_display() if task.status else 0,
                task.get_due_display() if task.due else 0,
                task.task_description if task.task_description else 0,
                task.start_date if task.start_date else 0,
                task.due_date if task.due_date else 0,
            ]
            ws_data.append(row)

        # 补足 Task ID 到50行
        for i in range(row_count + 1, 51):
            row = [''] * len(headers_data)
            row[1] = i  # Task ID列填行号
            ws_data.append(row)

        # 写 CustomerInfo
        headers_info = ['Index', 'User ID', 'Group ID', 'Plan ID', 'Task Number']
        ws_info.append(headers_info)

        for idx, planner in enumerate(planners, start=1):
            row = [
                idx,
                1,  # 默认 User ID
                planner.teams_id or '',
                planner.plannerid or '',
                1  # 默认 Task Number
            ]
            ws_info.append(row)

        wb.save(save_path)

        return render(request, 'projects/select_project.html', {
            'projects': projects,
            'message': 'finished'
        })

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
        return render(request, 'projects/select_project.html', {'projects': projects, 'message': 'Project selected for export.'})

    # 如果是 GET 请求，显示所有项目的选择界面
    return render(request, 'projects/select_project.html', {'projects': projects})


from django.shortcuts import render

def dual_view(request):
    return render(request, 'projects/dual_view.html')


from django.shortcuts import render
from .forms import PlannerForm
from .models import Planner

def export_tasks_planner(request):
    success_message = ''
    if request.method == 'POST':
        form = PlannerForm(request.POST)
        if form.is_valid():
            planner_instance = Planner.objects.first()
            if planner_instance:
                planner_instance.plannerid = form.cleaned_data['plannerid']
                planner_instance.teams_id = form.cleaned_data['teams_id']
                planner_instance.save()
            else:
                form.save()
            success_message = 'submit successfully'
            form = PlannerForm() 
    else:
        form = PlannerForm()
    return render(request, 'projects/loginmicrosoft.html', {'form': form, 'success_message': success_message})


