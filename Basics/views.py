from django.shortcuts import render

def Sum(request):
    if request.method == 'POST':
        num1 = int(request.POST.get('txt_num1', 0))
        num2 = int(request.POST.get('txt_num2', 0))
        result = num1 + num2
        return render(request, 'Basics/Sum.html', {'Result': result})
    return render(request, 'Basics/Sum.html')

def Calculator(request):
    if request.method == 'POST':
        num1 = int(request.POST.get('txt_num1', 0))
        num2 = int(request.POST.get('txt_num2', 0))
        button = request.POST.get('btn_calc')
        result = 0
        if button == "+":
            result = num1 + num2
        elif button == "-":
            result = num1 - num2
        elif button == "*":
            result = num1 * num2
        elif button == "/":
            result = num1 / num2 if num2 != 0 else "Cannot divide by zero"
        return render(request, 'Basics/Calculator.html', {'Result': result})
    return render(request, 'Basics/Calculator.html')

def Largest(request):
    if request.method == 'POST':
        num1 = int(request.POST.get('txt_num1', 0))
        num2 = int(request.POST.get('txt_num2', 0))
        num3 = int(request.POST.get('txt_num3', 0))
        result = max(num1, num2, num3)
        return render(request, 'Basics/Largest.html', {'Result': result})
    return render(request, 'Basics/Largest.html')

def Ranklist(request):
    if request.method == 'POST':
        name1 = request.POST.get('txt_name1', '')
        name2 = request.POST.get('txt_name2', '')
        name = f"{name1} {name2}".strip()
        gender = request.POST.get('gender')
        semester = request.POST.get('semester')
        subject = request.POST.get('Subject')
        m1 = int(request.POST.get('txt_m1', 0))
        m2 = int(request.POST.get('txt_m2', 0))
        m3 = int(request.POST.get('txt_m3', 0))
        total = m1 + m2 + m3
        percentage = (total / 300) * 100
        if percentage >= 90:
            grade = "A"
        elif percentage >= 75:
            grade = "B"
        elif percentage >= 50:
            grade = "C"
        else:
            grade = "Fail"
        return render(request, 'Basics/Ranklist.html', {
            'name': name,
            'gender': gender,
            'semester': semester,
            'subject': subject,
            'total': total,
            'percentage': round(percentage, 2),
            'grade': grade
        })
    return render(request, 'Basics/Ranklist.html')

def Salarycalculation(request):
    if request.method == 'POST':
        name1 = request.POST.get('txt_name1', '')
        name2 = request.POST.get('txt_name2', '')
        name = f"{name1} {name2}".strip()
        gender = request.POST.get('gender')
        martial = request.POST.get('Martial')
        dept = request.POST.get('Department')
        salary = int(request.POST.get('txt_m1', 0))
        if salary >= 10000:
            TA = salary * 0.4
            DA = salary * 0.35
            HRA = salary * 0.3
            LIC = salary * 0.25
            PF = salary * 0.2
        elif salary >= 5000:
            TA = salary * 0.35
            DA = salary * 0.3
            HRA = salary * 0.25
            LIC = salary * 0.2
            PF = salary * 0.15
        else:
            TA = salary * 0.3
            DA = salary * 0.25
            HRA = salary * 0.2
            LIC = salary * 0.15
            PF = salary * 0.1
        deduction = LIC + PF
        netamount = salary + TA + DA + HRA - deduction
        return render(request, 'Basics/Salarycalculation.html', {
            'name': name,
            'gender': gender,
            'martial': martial,
            'dept': dept,
            'salary': salary,
            'TA': TA,
            'DA': DA,
            'HRA': HRA,
            'LIC': LIC,
            'PF': PF,
            'deduction': deduction,
            'netamount': netamount
        })
    return render(request, 'Basics/Salarycalculation.html')
