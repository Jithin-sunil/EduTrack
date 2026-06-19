from django.shortcuts import render, redirect
from Administrator.models import tbl_adminregistration, tbl_department, tbl_programme
from Guest.models import tbl_student, tbl_faculty, tbl_company

def index(request):
    return render(request, 'Guest/index.html')

def Login(request):
    if request.method == 'POST':
        email = request.POST.get('txt_email')
        password = request.POST.get('txt_password')
        
        # 1. Admin login check
        admin = tbl_adminregistration.objects.filter(adminregistration_email=email, adminregistration_password=password).first()
        if admin:
            request.session['aid'] = admin.adminregistration_id
            request.session['role'] = 'Admin'
            request.session['name'] = admin.adminregistration_name
            return redirect('Administrator:Dashboard')
            
        # 2. Student login check
        student = tbl_student.objects.filter(student_email=email, student_password=password).first()
        if student:
            if student.student_status == 0:
                return render(request, 'Guest/Login.html', {'error': 'Your student registration is pending administrator approval.'})
            elif student.student_status == 2:
                return render(request, 'Guest/Login.html', {'error': 'Your student registration has been rejected.'})
            
            request.session['sid'] = student.student_id
            request.session['role'] = 'Student'
            request.session['name'] = student.student_name
            return redirect('Student:Dashboard')
            
        # 3. Faculty login check
        faculty = tbl_faculty.objects.filter(faculty_email=email, faculty_password=password).first()
        if faculty:
            if faculty.faculty_status == 0:
                return render(request, 'Guest/Login.html', {'error': 'Your faculty registration is pending administrator approval.'})
            elif faculty.faculty_status == 2:
                return render(request, 'Guest/Login.html', {'error': 'Your faculty registration has been rejected.'})
                
            request.session['fid'] = faculty.faculty_id
            request.session['role'] = 'Faculty'
            request.session['name'] = faculty.faculty_name
            return redirect('Faculty:Dashboard')
            
        # 4. Company login check
        company = tbl_company.objects.filter(company_email=email, company_password=password).first()
        if company:
            if company.company_status == 0:
                return render(request, 'Guest/Login.html', {'error': 'Your company registration is pending administrator approval.'})
            elif company.company_status == 2:
                return render(request, 'Guest/Login.html', {'error': 'Your company registration has been rejected.'})
                
            request.session['cid'] = company.company_id
            request.session['role'] = 'Company'
            request.session['name'] = company.company_name
            return redirect('Company:Dashboard')
            
        return render(request, 'Guest/Login.html', {'error': 'Invalid Email or Password.'})
        
    return render(request, 'Guest/Login.html')

def StudentRegister(request):
    programmes = tbl_programme.objects.filter(programme_status=1)
    if request.method == 'POST':
        name = request.POST.get('txt_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        email = request.POST.get('txt_email')
        contact = request.POST.get('txt_contact')
        address = request.POST.get('txt_address')
        admissionno = request.POST.get('txt_admissionno')
        password = request.POST.get('txt_password')
        confirm_password = request.POST.get('txt_confirm_password')
        programme_id = request.POST.get('sel_programme')
        photo = request.FILES.get('photo')
        
        # Validation
        if tbl_student.objects.filter(student_email=email).exists():
            return render(request, 'Guest/StudentRegister.html', {'programmes': programmes, 'error': 'Email is already registered.'})
        if tbl_student.objects.filter(student_admissionno=admissionno).exists():
            return render(request, 'Guest/StudentRegister.html', {'programmes': programmes, 'error': 'Admission Number is already registered.'})
        if password != confirm_password:
            return render(request, 'Guest/StudentRegister.html', {'programmes': programmes, 'error': 'Passwords do not match.'})
            
        prog = tbl_programme.objects.get(programme_id=programme_id)
        tbl_student.objects.create(
            programme=prog,
            student_name=name,
            student_gender=gender,
            student_dob=dob,
            student_email=email,
            student_contact=contact,
            student_address=address,
            student_admissionno=admissionno,
            student_password=password,
            student_photo=photo,
            student_status=0
        )
        return render(request, 'Guest/Login.html', {'msg': 'Student registration successful! Pending admin approval.'})
        
    return render(request, 'Guest/StudentRegister.html', {'programmes': programmes})

def FacultyRegister(request):
    departments = tbl_department.objects.filter(department_status=1)
    if request.method == 'POST':
        name = request.POST.get('txt_name')
        email = request.POST.get('txt_email')
        contact = request.POST.get('txt_contact')
        address = request.POST.get('txt_address')
        password = request.POST.get('txt_password')
        confirm_password = request.POST.get('txt_confirm_password')
        department_id = request.POST.get('sel_department')
        photo = request.FILES.get('photo')
        
        # Validation
        if tbl_faculty.objects.filter(faculty_email=email).exists():
            return render(request, 'Guest/FacultyRegister.html', {'departments': departments, 'error': 'Email is already registered.'})
        if password != confirm_password:
            return render(request, 'Guest/FacultyRegister.html', {'departments': departments, 'error': 'Passwords do not match.'})
            
        dept = tbl_department.objects.get(department_id=department_id)
        tbl_faculty.objects.create(
            department=dept,
            faculty_name=name,
            faculty_email=email,
            faculty_contact=contact,
            faculty_address=address,
            faculty_password=password,
            faculty_photo=photo,
            faculty_status=0
        )
        return render(request, 'Guest/Login.html', {'msg': 'Faculty registration successful! Pending admin approval.'})
        
    return render(request, 'Guest/FacultyRegister.html', {'departments': departments})

def CompanyRegister(request):
    if request.method == 'POST':
        name = request.POST.get('txt_name')
        contactperson = request.POST.get('txt_contactperson')
        email = request.POST.get('txt_email')
        contact = request.POST.get('txt_contact')
        address = request.POST.get('txt_address')
        password = request.POST.get('txt_password')
        confirm_password = request.POST.get('txt_confirm_password')
        proof = request.FILES.get('proof')
        
        # Validation
        if tbl_company.objects.filter(company_email=email).exists():
            return render(request, 'Guest/CompanyRegister.html', {'error': 'Email is already registered.'})
        if password != confirm_password:
            return render(request, 'Guest/CompanyRegister.html', {'error': 'Passwords do not match.'})
            
        tbl_company.objects.create(
            company_name=name,
            company_contactperson=contactperson,
            company_email=email,
            company_contact=contact,
            company_address=address,
            company_password=password,
            company_proof=proof,
            company_status=0
        )
        return render(request, 'Guest/Login.html', {'msg': 'Company registration successful! Pending admin approval.'})
        
    return render(request, 'Guest/CompanyRegister.html')

def Logout(request):
    request.session.flush()
    return redirect('Guest:index')
