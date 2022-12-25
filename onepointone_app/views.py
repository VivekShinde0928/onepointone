import glob
import string
from datetime import datetime
import json
import csv
import random

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt

from onepointone_app.models import LoginDetails, EmployeeData
import os

baseURL = "/"
# baseURL = "http://127.0.0.1:8009/"
baselink="http://127.0.0.1:8009/media/"

local_directory = 'D:/PycharmProjects/onepointone/media/'

@csrf_exempt
def home(request):
    return render(request,'home.html')

@csrf_exempt
def login_access(request):
    return render(request, 'login.html', {'baseURL': baseURL})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        response = {}

        char_set = string.ascii_uppercase + string.digits
        session_key = ''.join(random.sample(char_set * 20, 20))
        print(session_key)
        
        id = request.POST.get('id')
        password = request.POST.get('password')

        validate = EmployeeData.objects.filter(emp_id=id,password=password).exists()

        if validate:
            name = EmployeeData.objects.filter(emp_id=id).values_list('name')
            print('name--->',name)
            request.session['session_key'] = session_key
            request.session['empid'] = id
            request.session['name'] = name[0][0]
            response['status']='true'
            return JsonResponse(json.dumps(response),safe=False)
        else:
            response['status'] = 'false'
            response['msg'] = 'Invalid ID or password!!'
            return JsonResponse(json.dumps(response),safe=False)

@csrf_exempt
def logout(request):
    del request.session['session_key']
    return redirect(baseURL)

@csrf_exempt
def csv_page(request):
    if request.session.has_key('session_key'):
        data =  EmployeeData.objects.values_list().order_by('-id')
        name = request.session.get('name')
        print('data---->',data)

        if len(data) > 0:
            paginator = Paginator(data, 1)
            page = request.GET.get('page')
            fetchuserdata = paginator.get_page(page)

            if page:
                strt = int(page) * 1 - 1
                end = int(page) * 1

            userlist = zip(data)

        return render(request, 'csv_upload.html', {'baseURL': baseURL,'data':data,'fetchuserdata':fetchuserdata,'datalength':len(data),
        'name':name})


@csrf_exempt
def upload_csv(request):
    if request.method == "POST":
        response={}
        print('in csv method')
        csv_file = request.FILES["csv_upload"]
        print('csv_file--->',csv_file)

        if not csv_file.name.endswith('.csv'):
            print('not cvs')
            messages.warning(request, 'The wrong file type was uploaded')
            # return HttpResponseRedirect(request.path_info)
            response['msg'] = 'The wrong file type was uploaded!!'
            return  JsonResponse(json.dumps(response),safe=False)
        file_data = csv_file.read().decode("utf-8")
        # file_data = csv_file.read()
        csv_data = file_data.split("\n")
        print('csv_data---------->',csv_data)

        csv_header = ['name','dob','doj','gender','designation','manager','picture','password','email\r']

        for x in csv_data:
            fields = x.split(",")
            # print('fields--->',fields)
            if csv_header == fields:
                print('matched')
                response['status']='true'
                response['msg']='Data added successfully!!'
                break
            else:
                response['status'] = 'false'
                response['msg']='Header not matched.Kindly check CSV!!'

        query1_op = EmployeeData.objects.all().order_by('-id').values_list()[::1]
        emp_id = ""
        if query1_op:
            emp_id = int(query1_op[0][1]) + 1
        else:
            emp_id = '1001'
        for row in range(1, len(csv_data)):
            field = (csv_data[row]).split(",")
            if '' not in field:
                EmployeeData.objects.create(
                            emp_id=emp_id,
                            name=field[0],
                            dob=field[1],
                            doj=field[2],
                            gender=field[3],
                            designation=field[4],
                            manager=field[5],
                            picture=field[6],
                            password=field[7],
                            email=field[8]
                        )
        return JsonResponse(json.dumps(response),safe=False)


@csrf_exempt
def empForm(request):
    return render(request, 'empForm.html',{'baseURL': baseURL})

@csrf_exempt
def addEmp(request):
    if request.method == 'POST':
        response = {}
        print('------ add emp-----')
        json_data = request.POST.get('requestData')
        print('json_data===>', json_data)
        upload_file = request.FILES.get('files')
        print('upload_file------>',upload_file)

        # if not MyFiles:
        #     file_name = ""
        # else:
        #     for file in MyFiles:
        #         if MyFiles:
        #             file_name = file.name
        #             print('file_name======>', file_name)

        new_req = json.loads(json_data)
        emp_name = new_req['employee_name']
        password = new_req['password']
        mail = new_req['mail']
        designation = new_req['designation']
        gender = new_req['gender']
        join_date = new_req['join_date']
        dob = new_req['dob']
        rights = new_req['rights']

        query1_op = EmployeeData.objects.all().order_by('-id').values_list()[::1]
        print(query1_op[0][1])

        emp_id = ""
        if query1_op:
            emp_id = int(query1_op[0][1]) + 1

        else:
            emp_id = '1001'

        if upload_file is not None:
            UPLOAD_FOLDER = f'{local_directory}{emp_id}/pic/'
            fs = FileSystemStorage(location=UPLOAD_FOLDER)
            isExist = os.path.exists(UPLOAD_FOLDER)
            name = upload_file.name
            if not isExist:
                os.makedirs(UPLOAD_FOLDER)
                print("The new directory is created!")
                file = fs.save(name, upload_file)
                imgpath = f"{baselink}{emp_id}/pic/{name}"
                print('imgpath==>', imgpath)
            else:
                filelist = glob.glob(os.path.join(UPLOAD_FOLDER, "*"))
                for f in filelist:
                    os.remove(f)
                    print('file removed')
                files = fs.save(name, upload_file)

                imgpath = f"{baselink}{emp_id}/pic/{name}"
                print('imgpath==>', imgpath)

            # Customer.objects.filter(customer_id=customer_id).update(consent_form=imgpath)

        emp_data = EmployeeData(name=emp_name, password=password, email=mail,
                                     manager=rights,
                                     emp_id=emp_id, designation=designation, picture=name,
                                     gender=gender, doj=join_date, dob=dob
                                )
        emp_data.save()
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        response['status'] = 'true'
        response['msg'] = 'Record added successfully!!'
        messages.success(request, 'Employee added Successfully!')
        print('response---->',response)
        return JsonResponse(json.dumps(response),safe=False)

def editEmp(request, id):
        print(id)

        # query = f"select * from table_helpdesk_user where id = '{id}'"
        # print('query in attach=====--->', query)
        # cursor.execute(query)
        # output = cursor.fetchall()
        # print('output in attach====>', output)

        edit_object = EmployeeData.objects.filter(id=id).values_list()
        print('edit_object====>',edit_object)

        # emp_id = edit_object[0][6]
        emp_name = edit_object[0][2]
        dob = edit_object[0][3]
        join_date = edit_object[0][4]
        gender = edit_object[0][5]
        designation = edit_object[0][6]
        rights = edit_object[0][7]
        mail = edit_object[0][10]
        pic = edit_object[0][8]
        password = edit_object[0][9]

        return render(request, 'editEmp.html',
                      {'baseURL': baseURL, 'emp_name': emp_name,'id':id,
                       'designation': designation,
                       'gender': gender, 'join_date': join_date,
                       'mail': mail,
                       'dob': dob,"password":password,
                        "rights": rights,"pic":pic
                       })


@csrf_exempt
def saveEditEmp(request):
    if request.method == 'POST':
        response={}
        json_data = request.POST.get('requestData')
        print('json_data=----==>', json_data)
        updated_data = json.loads(json_data)
        emp_name = updated_data['employee_name']
        unique_id = updated_data['unique_id']
        password = updated_data['password']
        mail = updated_data['mail']
        designation = updated_data['designation']
        gender = updated_data['gender']
        join_date = updated_data['join_date']
        dob = updated_data['dob']
        rights = updated_data['rights']

        upload_file = request.FILES.get('files')

        update_obj = EmployeeData.objects.filter(id=unique_id)

        emp_id = EmployeeData.objects.filter(id=unique_id).values_list('emp_id')
        emp_id=emp_id[0][0]

        if upload_file is not None:
            UPLOAD_FOLDER = f'{local_directory}{emp_id}/pic/'
            fs = FileSystemStorage(location=UPLOAD_FOLDER)
            isExist = os.path.exists(UPLOAD_FOLDER)
            name = upload_file.name
            if not isExist:
                os.makedirs(UPLOAD_FOLDER)
                print("The new directory is created!")
                file = fs.save(name, upload_file)
            else:
                filelist = glob.glob(os.path.join(UPLOAD_FOLDER, "*"))
                for f in filelist:
                    os.remove(f)
                    print('file removed')
                files = fs.save(name, upload_file)


        for obj in update_obj:
            obj.name=emp_name
            obj.dob=dob
            obj.doj=join_date
            obj.gender=gender
            obj.designation=designation
            obj.manager=rights
            obj.password=password
            obj.email=mail
            if upload_file:
                obj.picture= name

            obj.save()
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        response['status'] = 'true'
        response['msg'] = 'Record added successfully!!'
        # messages.success(request, 'Employee added Successfully!')
        print('response---->', response)
        return JsonResponse(json.dumps(response), safe=False)


def deleteEmp(request, id):
        response = {}
        try:
            print(id)

            del_obj = EmployeeData.objects.filter(id=id)
            del_obj.delete()

            response['status'] = True
            response['msg'] = 'User Deleted Successfully.'
            messages.success(request, 'User Deleted Successfully!')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        except:
            response['status'] = False
            response['msg'] = 'Something went wrong.'
            return JsonResponse(json.dumps(response), safe=False)


def downloadCSV(request):
    reponse = {}

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Employee Data.csv";encoding="utf-8";sep=","'
    writer = csv.writer(response)
    
    # writer.writerow(['Pending Tickets'])
    writer.writerow(
        ['Sr.No','EmpID', 'Name', 'DOB', 'DOJ', 'Gender', 'Designation',
            'Manager',
            'Pic', 'Password', 'Email'
            ])

    csv_data = EmployeeData.objects.values_list('emp_id','name','dob','doj','gender','designation','manager','picture','password','email')
    print('csv_data----->',csv_data)


    csv_count = 0
    for employe in csv_data:
        csv_count += 1
        e_12 = list(employe)
        e_12.insert(0, csv_count)
        new_arr = tuple(e_12)
        # print("--------------", new_arr)
        writer.writerow(new_arr)
    return response