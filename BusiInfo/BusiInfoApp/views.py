from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .stAPI import st_enroll
from .models import Student, Seller, Product
from random import randint
import datetime

appdetails = {
    'appName' : 'Business Information System',
    'appTagline' : 'A Business Infomation System for all students of college.'
}

def stAPI(request):
    return JsonResponse({"st_data": st_enroll})

def index(request):
    if 'user' in request.session:
        return render(request,'user.html', appdetails)
    else:
        return render(request,'index.html', appdetails)

def logout(request):
    del request.session['user']
    return redirect(index)

codes = {
    100: 'user found',
    101: 'incorrect password!',
    102: 'account created!',
    103: 'student not enrolled in any univercity!',
    104: 'no such seller added by any student!',
    105: 'please enter your id',
    106: 'please enter your password',
    107: 'profile updated successfully',
    108: 'product added successfully',
    109: 'product deleted successfully',
    110: 'profile updated successfully',
    111: 'seller added successfully',
    112: 'seller deleted successfully',
    113: 'product updated successfully'
}
def user(id, password):
    all_st = Student.objects.all()
    for st in all_st:
        if st.EnrollNum == id:
            if st.Password == password:
                return 100
            else:
                return 101
    else:
        for i in range(len(st_enroll)):
            if st_enroll[i]['enroll'] == int(id):
                col_id = st_enroll[i]['college']['col_id']
                col_name = st_enroll[i]['college']['col_name'] + ', ' + st_enroll[i]['college']['col_addr']
                name = st_enroll[i]['name']
                father = st_enroll[i]['father']
                gender = st_enroll[i]['gender']
                dob = st_enroll[i]['dob'].split('-')
                mobile = st_enroll[i]['mobile']
                address = st_enroll[i]['address']
                state = st_enroll[i]['state']
                city = st_enroll[i]['city']

                Student.objects.create(
                    EnrollNum = id,
                    CollegeID = col_id,
                    CollegeName = col_name,
                    FullName = name,
                    FatherName = father,
                    BirthDate = f"{dob[2]}-{dob[1]}-{dob[0]}",
                    Gender = gender,
                    State = state,
                    City = city,
                    Address = address,
                    Mobile = mobile,
                    Password = password,
                    RFID = f"RF{id}"
                )
                
                return 102
        else:
            return 103

def userpage(request):
    if 'user' in request.session:
        all_st = Student.objects.all()
        all_product = Product.objects.all()

        product_list = []
        for st in all_st:
            if st.EnrollNum == request.session['user']:
                appdetails['enroll_no'] = st.EnrollNum
                appdetails['user_name'] = st.FullName
                appdetails['fathername'] = st.FatherName
                appdetails['dob'] = st.BirthDate
                appdetails['gender'] = st.Gender
                appdetails['password'] = st.Password
                appdetails['mobile'] = st.Mobile
                appdetails['city'] = st.City
                appdetails['state'] = st.State
                appdetails['address'] = st.Address
                appdetails['sellers'] = loadSellers(st.RFID)

                s = ''
                for p in all_product:
                    if st.RFID == p.RFID:
                        appdetails['total_products'] = len(all_product)
                    for slr in appdetails['sellers']:
                        if p.RFID in slr.values():
                            s = slr['company']

                    product_list.append({'rfid':p.RFID,'seller':s,'product_id':p.ProductID,'product_name':p.ProductName,'price':p.Price,'category':p.Category,'product_desc':p.Description})

        appdetails['products'] = product_list
        appdetails['total_business'] = len(appdetails['sellers'])
        return render(request, 'user.html', appdetails)
    else:
        return redirect(index)

def sellerpage(request):
    if 'user' in request.session:
        all_seller = Seller.objects.all()
        all_product = Product.objects.all()
        
        for slr in all_seller:
            if slr.RFID == request.session['user']:
                appdetails['owner_id'] = slr.RFID
                appdetails['password'] = slr.Password
                appdetails['owner_name'] = slr.OwnerName
                appdetails['business_name'] = slr.Company
                appdetails['mobile'] = slr.Mobile
                appdetails['business_type'] = slr.Type
                appdetails['business_address'] = slr.Address
                appdetails['about'] = slr.About
                appdetails['products'] = loadProduct(request.session['user'])

                for p in all_product:
                    if slr.RFID == p.RFID:
                        appdetails['total_products'] = len(all_product)

        return render(request, 'seller.html', appdetails)
    else:
        return redirect(index)

def seller(rfid, password):
    all_st = Student.objects.all()
    all_seller = Seller.objects.all()

    for s in all_st:
        if s.RFID == rfid:
            for slr in all_seller:
                if slr.RFID == rfid:
                    if slr.Password == password:
                        return 100
                    else:
                        return 101
            else:
                Seller.objects.create(
                    RFID = rfid,
                    Password = password,
                    RegDate = datetime.datetime.now()
                )
                return 102
    else:
        return 104

def signup(request):
    if request.POST.get('role') == 'user':
        enroll = request.POST.get('id')
        password = request.POST.get('password')

        if enroll:
            if password:
                resp = user(enroll, password)
                if resp == 100:
                    #return render(request, 'user.html')
                    request.session['user'] = enroll
                    return JsonResponse({'code': 100, 'url': '/userpage'})
                else:
                    return JsonResponse({'role':'.user', 'code': codes[resp] })
            else:
                return JsonResponse({'role':'.user', 'code': 106, 'err': codes[106]})
        else:
            return JsonResponse({'role':'.user', 'code': 105, 'err': codes[105]})

    elif request.POST.get('role') == 'seller':
        rfid = request.POST.get('id')
        password = request.POST.get('password')

        if rfid:
            if password:
                resp = seller(rfid, password)
                if resp == 100:
                    #return render(request, 'seller.html')
                    request.session['user'] = rfid
                    return JsonResponse({'code': 100, 'url': '/seller'})
                else:
                    return JsonResponse({'role':'.seller', 'code': codes[resp] })
            else:
                return JsonResponse({'role':'.seller', 'code': 106, 'err': codes[106]})
        else:
            return JsonResponse({'role':'.seller', 'code': 105, 'err': codes[105]})

def refreshProfile(rfid):
    seller = Seller.objects.all()
    products = Product.objects.filter(RFID=rfid)

    data = {}
    for s in seller:
        if s.RFID == rfid:
            data['fullname'] = s.OwnerName
            data['mobile'] = s.Mobile
            data['password'] = s.Password
            data['company'] = s.Company
            data['type'] = s.Type
            data['address'] = s.Address
            data['total_products'] = len(products)
            data['about'] = s.About

    return data

def profile_update(request):
    if request.POST.get('role') == 'user':
        enroll_id = request.POST.get('enroll_id')
        password = request.POST.get('password')
        Student.objects.filter(EnrollNum=enroll_id).update(Password = password)
        return JsonResponse({'code':107, 'msg': codes[107]})

    elif request.POST.get('role') == 'seller':
        rfid = request.POST.get('id')
        fullname = request.POST.get('fullname')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        comp_name = request.POST.get('company_name')
        comp_type = request.POST.get('company_type')
        comp_address = request.POST.get('company_address')
        comp_about = request.POST.get('company_about')

        Seller.objects.filter(RFID=rfid).update(
            OwnerName = fullname,
            Company = comp_name,
            Mobile = mobile,
            Type = comp_type,
            Address = comp_address,
            About = comp_about,
            Password = password
        )
        return JsonResponse({'code':107, 'msg': codes[107], 'data': refreshProfile(rfid)})

def createID(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def loadProduct(rfid):
    products = Product.objects.all()

    product_list = []
    for p in products:
        if p.RFID == rfid:
            product_list.append({'product_id':p.ProductID,'product_name':p.ProductName,'price':p.Price,'category':p.Category,'product_desc':p.Description})

    return product_list

def loadSellers(rfid):
    sellers = Seller.objects.all()
    sellers_list = []
    for slr in sellers:
        #if slr.RFID == rfid:
        sellers_list.append(
            {
                'rfid': slr.RFID,
                'name': slr.OwnerName,
                'company': slr.Company,
                'mobile': slr.Mobile,
                'type': slr.Type,
                'address': slr.Address,
                'about': slr.About,
                'reg_date': slr.RegDate
            }
        )

    return sellers_list

def add_product(request):
    if request.POST.get('id'):
        rfid = request.POST.get('id')
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        product_desc = request.POST.get('product_desc')
        mode = request.POST.get('mode')

        res = ''
        if mode == 'save':
            Product.objects.create(
                RFID = rfid,
                ProductID = createID(4),
                ProductName = product_name,
                Price = price,
                Description = product_desc
            )
            products = Product.objects.filter(RFID=rfid)
            res = {'code': 108, 'msg': codes[108], 'total_products': len(products)}
        elif mode == 'update':
            product_id = request.POST.get('product_id')
            Product.objects.filter(RFID=rfid, ProductID=product_id).update(
                ProductName = product_name,
                Price = price,
                Description = product_desc
            )
            products = Product.objects.filter(RFID=rfid)
            res = {'code': 113, 'msg': codes[113], 'total_products': len(products)}
        
        return JsonResponse(res)

def remove_product(request):
    if request.POST.get('id'):
        rfid = request.POST.get('id')
        product_id = request.POST.get('product_id')

        Product.objects.filter(RFID=rfid, ProductID=product_id).delete()
        return JsonResponse({'code': 109, 'msg': codes[108]})