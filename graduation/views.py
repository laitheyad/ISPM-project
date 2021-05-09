from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User as SuperUser
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from .models import *
from django.contrib import messages


def landing_view(request):
    """
    ``(VIEW)`` The login view.
    logs-in the current user into the portal and redirect them, if they were admin they'll be redirected
    to the admins homepage, and if they were patients will direct them to the patient landing.
    """
    # request.session.clear()
    # if 'IsLoggedIn' in request.session.keys():
    # if request.session['IsLoggedIn']:
    #     return redirect('/admin-reports', admin_reports_view)
    # form = forms.LoginForm()

    return render(request, "home.html")


def logoutUser(request):
    logout(request)
    return render(request, "home.html")


def login_View(request):
    request.session["is_Logged_in"] = False

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        teacher = Teacher.objects.filter(username=user)
        student = Student.objects.filter(username=user)

        if (len(teacher) > 0):
            teacher = teacher[0]
            project_requests = Project.objects.filter(project_supervisor=teacher)
            meetings = Meeting.objects.filter(project_supervisor=teacher)
            reports = ProgressReport.objects.filter(project_supervisor=teacher)
            context = {'requests': list(project_requests.values()), 'meetings': meetings, 'reports': reports}
            return render(request, 'teacher-profile.html', context)

        # request.session["is_Logged_in"] = False
        if user is not None:
            auth.login(request, user)
            try:
                consumer = Student.objects.get(username=user)
                project = Project.objects.filter(group_members=consumer)
            except:
                print("invalid credentials")
                return redirect("/")
            request.session["is_Logged_in"] = True
            request.session["username"] = username
            request.session["user_pk"] = consumer.pk
            request.session["is_teacher"] = user.is_staff

            if len(project) > 0:
                request.session["project_id"] = project[0].pk
                project = project[0]
            else:
                project = ''
            full_name = u"{} {}".format(consumer.first_name, consumer.last_name)
            request.session["full_name"] = str(full_name)
            available_teachers = get_available_teachers()
            projects = Project.objects.all()

            return render(request, 'index.html',
                          {'username': user.username, 'full_name': full_name, 'user_pk': user.pk,
                           'consumer': consumer, 'project': project, 'available_teachers': available_teachers,
                           'error': '', 'projects': projects})
        else:
            messages.info(request, "invalid credentials")
            return redirect("/")

    else:
        if 'is_Logged_in' in request.session:
            if request.session["is_Logged_in"]:
                username = request.session["username"]
                user = SuperUser.objects.get(username=username)
                consumer = Student.objects.get(username=user)
                project = Project.objects.filter(group_members=consumer)
                full_name = u"{} {}".format(consumer.first_name, consumer.last_name)
                group = ''
                if len(project) > 0:
                    project = project[0]
                    group = list(project.getGroupeMembers().all().values())
                    for i in group:
                        i['index'] = group.index(i) + 1
                else:
                    project = ''
                available_teachers = get_available_teachers()
                return render(request, 'index.html',
                              {'username': user.username, 'full_name': full_name,
                               'available_teachers': available_teachers,
                               'consumer': consumer, 'project': project, 'group_members': group, 'error': ''})
        return render(request, 'home.html', )


def get_available_teachers():
    teacher_project_dict = {}
    not_av = []

    projects = Project.objects.all()
    teachers = list(Teacher.objects.all().values())
    for t in teachers:
        teacher_project_dict[t['id']] = 0

    for p in projects:
        for t in p.project_supervisor.all().values():
            not_av.append(Teacher.objects.get(pk=t['id']))
            teacher_project_dict[t['id']] += 1

    teacher_project_id_list = [x for x in teacher_project_dict]
    teacher_project_list = []
    for i in teacher_project_id_list:
        teach = Teacher.objects.get(pk=i)
        teach.num_of_projects = teacher_project_dict[i]
        teacher_project_list.append(teach)
    return teacher_project_list


def RegisterUser(request):
    # permission_classes = [IsAuthenticated]
    try:
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        date_of_birth = request.POST['date_of_birth']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
    except:
        return JsonResponse({'message': 'error while receiving data'})
    #   Creating Super user to authenticate with the given data
    try:
        user = SuperUser.objects.create(username=username, is_active=True)
        user.set_password(password)
        user.save()
    except:
        return JsonResponse({'message': 'user already exist'})
    #   creating User with the given Data
    try:
        User.objects.create(username=user, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth,
                            phone=phone, email=email)
    except:
        return JsonResponse({'message': 'error while creating user'})
    return JsonResponse({'message': 'User created'})


def apply_for_supervisor(request):
    if request.method == "POST":
        # receiving data
        error = ''
        try:
            supervisor = request.POST['supervisor']
            project_title = request.POST['project-title']
            project_members = request.POST['project-members']
            project_degree = request.POST['project-degree']
            project_description = request.POST['project-description']
        except:
            messages.add_message(request, messages.INFO, 'error while receiving data')
            return redirect('/')

        # applying request ...
        try:
            supervisor = Teacher.objects.get(id=supervisor)
            num_of_projects = Project.objects.filter(project_supervisor=supervisor.pk)
            if len(num_of_projects) >= 5:
                messages.add_message(request, messages.INFO, 'this teacher cannot accept more projects, his load is '
                                                             'full :(')
                return redirect('/')
            if ',' in project_members:
                project_members = project_members.split(',')
            else:
                t = []
                t.append(project_members)
                project_members = t
            project = Project.objects.create(project_title=project_title,
                                             project_degree=project_degree,
                                             project_description=project_description)
            list_of_members = []
            project.project_supervisor.set([supervisor.pk])
            for student_num in project_members:
                student = Student.objects.get(st_num=student_num)
                list_of_members.append(student.pk)
            project.group_members.set(list_of_members)
        except:
            messages.add_message(request, messages.INFO, 'error while applying request')

            return redirect('/')
    return redirect('/')


def acceptProject(request, pk):
    if request.method == 'GET':
        print(request.user)
        project = Project.objects.get(id=pk)
        project.status = 'Approved'
        project.save()
        teacher = Teacher.objects.filter(username=request.user)
        teacher = teacher[0]
        print(teacher)
        project_requests = Project.objects.filter(project_supervisor=teacher)
        print(project_requests)
        context = {'requests': list(project_requests.values())}

    return render(request, 'teacher-profile.html', context)


def rejectProject(request, pk):
    context = {}
    if request.method == 'GET':
        project = Project.objects.get(id=pk)
        project.status = 'Rejected'
        project.save()
        teacher = Teacher.objects.filter(username=request.user)
        teacher = teacher[0]
        project_requests = Project.objects.filter(project_supervisor=teacher)
        context = {'requests': list(project_requests.values())}

    return render(request, 'teacher-profile.html', context)


def acceptMeeting(request, pk):
    if request.method == 'GET':
        print(request.user)
        meeting = Meeting.objects.get(id=pk)
        meeting.status = 'Approved'
        meeting.save()
        teacher = Teacher.objects.filter(username=request.user)
        teacher = teacher[0]
        print(teacher)
        project_requests = Project.objects.filter(project_supervisor=teacher)
        meetings = Meeting.objects.filter(project_supervisor=teacher)
        print(project_requests)
        context = {'requests': list(project_requests.values()), 'meetings': meetings}

    return render(request, 'teacher-profile.html', context)


def rejectMeeting(request, pk):
    context = {}
    if request.method == 'GET':
        meeting = Meeting.objects.get(id=pk)
        meeting.status = 'Rejected'
        meeting.save()
        teacher = Teacher.objects.filter(username=request.user)
        teacher = teacher[0]
        project_requests = Project.objects.filter(project_supervisor=teacher)
        meetings = Meeting.objects.filter(project_supervisor=teacher)
        print(project_requests)
        context = {'requests': list(project_requests.values()), 'meetings': meetings}

    return render(request, 'teacher-profile.html', context)


def requestMeeting(request):
    if request.method == "POST":
        # receiving data
        error = ''
        try:
            supervisor = request.POST['supervisor']
            project = request.POST['project']
            date_0 = request.POST['date_0']
            date_1 = request.POST['date_1']
            meeting = Meeting.objects.create(project=project, project_supervisor=supervisor, date=f'{date_0}, {date_1}')
            meeting.save()
        except:
            messages.add_message(request, messages.INFO, 'error while receiving data')
            return redirect('/')