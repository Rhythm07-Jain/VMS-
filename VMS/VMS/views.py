from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import Usersform
import MySQLdb
from datetime import datetime


db = MySQLdb.connect("127.0.0.1","root","MILTONalmonds@100","vms_db" )

def home(request):
    return render(request,"index.html")

def adminLogin(request):
    try:
        if request.method=="POST":
            admin_id = request.POST.get("admin_id")
            # print(admin_id)
            a_password = request.POST.get("a_password")
            cursor = db.cursor()
            cursor.execute(f"select * from funding_committee where admin_id = '{admin_id}'")
            data = cursor.fetchone()
            # print("hyt")
            if(a_password==data[4]):
                print(data)
                request.session['admin_id'] = admin_id
                return redirect('/admin-login/dashboard/')
    except Exception as e:
        print("Exception1:",e)
    return render(request,"adminLogin.html")

def adminDashboard(request):
    try:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
            data = {
                'admin_id':admin_id,
                }
            return render(request, "adminDashboard.html", data)
    except Exception as e:
        print("Exception1:",e)
    return render(request, "adminDashboard.html")

def addStudent(request):
    try:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
            if request.method=="POST":
                c_fname = request.POST.get('s_fname')
                c_lname = request.POST.get('s_lname')
                cid = request.POST.get('s_id')
                c_email = request.POST.get('s_email')
                c_password = request.POST.get('s_password')
                c_phonenumber = request.POST.get('s_phonenumber')
                c_alternatephonenumber = request.POST.get('s_alternatephonenumber')
                cursor00 = db.cursor()
                cursor00.execute(f"insert into customer values('{cid}','{c_fname}','{c_lname}','{c_email}','{admin_id}','{c_password}')")
                cursor01 = db.cursor()
                cursor01.execute(f"insert into customer_mobno values('{cid}', {c_phonenumber})")
                if (c_alternatephonenumber):
                    cursor02 = db.cursor()
                    cursor02.execute(f"insert into customer_mobno values('{cid}', {c_alternatephonenumber})")
                db.commit()
            data = {
                'admin_id':admin_id,
            }
            return render(request,"adminAddStudent.html", data)

    except Exception as e:
        print("Exception:",e)
        return render(request,"adminAddStudent.html")

def studentDetails(request):
    try:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
            cursor00 = db.cursor()
            cursor00.execute(f"select cid, c_fname, c_lname, c_email from customer where admin_id='{admin_id}'")
            x = cursor00.fetchall()
            data = {
                'admin_id': admin_id,
                'fetched_data': x,
            }
            print(data)
            return render(request,"adminStudentDetails.html", data)

    except Exception as e:
        print("Exception:",e)
        return render(request,"adminStudentDetails.html")

def studentFullDetail(request, student_id):
    try:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
            cursor00 = db.cursor()
            cursor00.execute(f"select cid, c_fname, c_lname, c_email from customer where admin_id='{admin_id}' and cid='{student_id}'")
            x = cursor00.fetchone()
            cursor01 = db.cursor()
            cursor01.execute(f"select c_mobno from customer_mobno where cid='{student_id}'")
            y = cursor01.fetchall()
            # cursor02 = db.cursor()
            # cursor03 = db.cursor()
            # cursor02.execute(f"select count(*) from cart_item, orders where cart_item.item_id = orders.item_id and cart_item.in_cart = 0 and cart_item.cid = '{student_id}'")
            # cursor03.execute(f"select cart_item.item_id, cart_item.quantity, cart_item.order_item_price, cart_item.quantity*cart_item.order_item_price as amount from cart_item, orders where cart_item.item_id = orders.item_id and cart_item.in_cart = 0 and cart_item.cid = '{student_id}'")
            # count = cursor02.fetchone()[0]
            # expenses = 0
            # for i in range(count):
            #     expenses += cursor03.fetchone()[3]

            cursor03 = db.cursor()
            # cursor02.execute(f"select count(*) from cart_item, orders where cart_item.item_id = orders.item_id and cart_item.in_cart = 0 and cart_item.cid = '{cid}'")
            cursor03.execute(f"select sum(cart_item.quantity*cart_item.order_item_price) from cart_item where in_cart = 0 and cid = '{student_id}';")
            # count = cursor02.fetchone()[0]
            expenses = cursor03.fetchone()[0]
            data = {
                'admin_id': admin_id,
                'fetched_data': x,
                'cid': student_id,
                'mobile_numbers': y,
                'expenses': expenses,
            }
            print(data)
            return render(request,"adminEachStudentDetail.html", data)

    except Exception as e:
        print("Exception:",e)
        return render(request,"adminEachStudentDetail.html")

def studentEditDetails(request, student_id):
    try:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
            cursor03 = db.cursor()
            cursor03.execute(f"select cid, c_fname, c_lname, c_email, password from customer where admin_id='{admin_id}' and cid='{student_id}'")
            x = cursor03.fetchone()
            cursor04 = db.cursor()
            cursor05 = db.cursor()
            cursor04.execute(f"select count(*) from customer_mobno where cid='{student_id}'")
            count = int(cursor04.fetchone()[0])
            cursor05.execute(f"select c_mobno from customer_mobno where cid='{student_id}'")
            y = cursor05.fetchall()
            print(y)
            data = {
                'admin_id': admin_id,
                'fetched_data': x,
                'mob_numbers': y,
                'cid': student_id,
            }
            if request.method=="POST":
                c_fname = request.POST.get('s_fname')
                c_lname = request.POST.get('s_lname')
                cid = request.POST.get('s_id')
                c_email = request.POST.get('s_email')
                c_password = request.POST.get('s_password')
                c_phonenumber = request.POST.get('s_phonenumber')
                c_alternatephonenumber = request.POST.get('s_alternatephonenumber')
                cursor00 = db.cursor()
                cursor00.execute(f"update customer set cid='{cid}', c_fname='{c_fname}', c_lname='{c_lname}', c_email='{c_email}', password='{c_password}' where cid='{student_id}'")
                cursor01 = db.cursor()
                cursor01.execute(f"update customer_mobno set cid='{cid}', c_mobno={c_phonenumber} where cid='{student_id}' and c_mobno={y[0][0]}")
                # db.commit()
                if ((count==2) and (c_alternatephonenumber)):
                    cursor06 = db.cursor()
                    cursor06.execute(f"update customer_mobno set cid='{cid}', c_mobno={c_alternatephonenumber} where cid='{student_id}' and c_mobno={y[1][0]}")
                elif ((count==1) and (c_alternatephonenumber)):
                    cursor07 = db.cursor()
                    cursor07.execute(f"insert into customer_mobno values('{cid}', {c_alternatephonenumber})")
                elif ((count==2) and not(c_alternatephonenumber)):
                    cursor08 = db.cursor()
                    cursor08.execute(f"delete from customer_mobno where cid='{student_id}' and c_mobno={y[1][0]}") 
                db.commit()
                return redirect('/admin-login/dashboard/student-details')
            
            print(data)
            return render(request,"adminEditStudent.html", data)

    except Exception as e:
        print("Exception:",e)
        return render(request,"adminEditStudent.html")

def adminAddVendor(request):
    try:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
            if request.method == "POST":
                shop_name = request.POST.get("shopname")
                location = request.POST.get("location")
                email = request.POST.get("email")
                commission = request.POST.get("commission")
                v_password = request.POST.get("v_password")
                phonenumber = request.POST.get("phonenumber")
                alternatephonenumber = request.POST.get("alternatephonenumber")
                cursor1 = db.cursor()
                cursor1.execute(f"select count(*) from vendor")
                count = cursor1.fetchone()[0]
                vid = shop_name.split()[0] + str(count+1)
                print(vid)
                cursor2 = db.cursor()
                cursor2.execute(f"insert into vendor values('{vid}', '{shop_name}', '{location}', '{email}', {commission}, {0}, '{admin_id}', '{v_password}', {0}, {0})")
                cursor3 = db.cursor()
                cursor3.execute(f"insert into vendor_mobno values('{vid}', '{phonenumber}')")
                db.commit()
                if (alternatephonenumber):
                    cursor3.execute(f"insert into vendor_mobno values('{vid}', '{alternatephonenumber}')")
                    db.commit()
            data = {
                'admin_id':admin_id,
                }
            return render(request, "adminAddVendor.html", data)
    except Exception as e:
        print("Exception1:",e)
    return render(request, "adminAddVendor.html")

def adminEditVendor(request, vid):
    try:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
            cursor1 = db.cursor()
            cursor1.execute(f"select shop_name, location, v_email, v_commission, password from vendor where vid = '{vid}' and deleted = 0")
            details = cursor1.fetchone()
            cursor2 = db.cursor()
            cursor2.execute(f"select count(*) from vendor_mobno where vid = '{vid}'")
            count = cursor2.fetchone()[0]
            cursor3 = db.cursor()
            cursor3.execute(f"select v_mobno from vendor_mobno where vid = '{vid}'")
            phonenumbers = []
            for i in range(count):
                x = cursor3.fetchone()[0]
                phonenumbers.append(x)
            
            if len(phonenumbers) == 1:
                phonenumbers.append("-")

            if request.method == "POST":
                shop_name = request.POST.get('shopname')
                email = request.POST.get('email')
                location = request.POST.get('location')
                commission = request.POST.get('commission')
                password = request.POST.get('password')
                phonenumber = request.POST.get('phonenumber')
                alternatephonenumber = request.POST.get('alternatephonenumber')

                cursor4 = db.cursor()
                cursor4.execute(f"update vendor set shop_name = '{shop_name}', location = '{location}', v_email = '{email}', v_commission = {commission}, password = '{password}' where vid = '{vid}' and deleted=0")

                cursor5 = db.cursor()
                cursor5.execute(f"update vendor_mobno set v_mobno = '{phonenumber}' where vid = '{vid}'")
                if alternatephonenumber != '-':
                    cursor5.execute(f"update vendor_mobno set v_mobno = '{alternatephonenumber}' where vid = '{vid}'")
                db.commit()
                return redirect("/admin-login/dashboard/vendor-details/")
            data = {
                'admin_id':admin_id,
                'details': details,
                'phonenumbers':phonenumbers,
            }
            print("jvadh", data)

            return render(request, "adminEditVendor.html", data)
    except Exception as e:
        print("Exception1:",e)
    return render(request, "adminEditVendor.html")

def adminDeleteVendor(request, vid):
    try:
        if request.session.has_key('admin_id'):
            cursor1 = db.cursor()
            cursor1.execute(f"update vendor set deleted = 1 where vid = '{vid}' and deleted=0")
            db.commit()
            return redirect("/admin-login/dashboard/vendor-details/")
    except Exception as e:
        print("Exception1:",e)
    return render(request, "adminDeleteVendor.html")
    
def adminVendorDetails(request):
    try:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
            cursor1 = db.cursor()
            cursor1.execute("select vid,shop_name from vendor where deleted = 0")
            vendors = cursor1.fetchall()
            print(vendors)
            data = {
                'admin_id':admin_id,
                'vendors':vendors,
                }
            return render(request, "adminVendorDetails.html", data)
    except Exception as e:
        print("Exception1:",e)
    return render(request, "adminVendorDetails.html")

def adminVendorViewDetails(request, vid):
    try:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
            cursor1 = db.cursor()
            cursor1.execute(f"select shop_name, location, v_email, v_commission, v_income, open from vendor where vid = '{vid}' and deleted = 0")
            details = cursor1.fetchone()
            data = {
                'admin_id':admin_id,
                'vid':vid,
                'details':details,
                }
            return render(request, "adminVendorViewDetails.html", data)

    except Exception as e:
        print("Exception1:",e)
    return render(request, "adminVendorViewDetails.html")

def adminLogout(request):
    try:
        if request.session.has_key('admin_id'):
            del request.session['admin_id']
        return redirect('/admin-login/')
    except Exception as e:
        print("Exception:",e)

def studentLogin(request):
    try:
        if request.method=="POST":
            cid = request.POST.get("cid")
            # print(cid)
            c_password = request.POST.get("c_password")
            cursor = db.cursor()
            cursor.execute(f"select * from customer where cid='{cid}'")
            data = cursor.fetchone()
            if(c_password==data[5]):
                # print(data)
                request.session['cid'] = cid
                return redirect('/student-login/dashboard/')
    except Exception as e:
        print("Exception:",e)
    return render(request,"studentLogin.html")

def studentDashboard(request):
    try:
        if request.session.has_key('cid'):
            cid = request.session['cid']
            # print(cid)
            cursor = db.cursor()
            cursor.execute(f"select shop_name, location, open from vendor where deleted=0 order by shop_name")
            fetched_data = cursor.fetchall()
            # print(fetched_data)
            data = {
                'cid':cid,
                'fetched_data':fetched_data,
                }
            # print(data)
            return render(request,"studentDashboard.html", data)
    except Exception as e:
        print("Exception:",e)
        return render(request,"studentDashboard.html")

def studentOutlet(request, outlet_name):
    try:
        if request.session.has_key('cid'):
            cid = request.session['cid']
            cursor03 = db.cursor()
            # print(outlet_name)
            cursor03.execute(f"select vid from vendor where shop_name = '{outlet_name}' and deleted=0")
            vid = cursor03.fetchone()[0]
            # print(vid)
            request.session['active_vendor'] = vid
            cursor_first = db.cursor()
            cursor_first = db.cursor()
            cursor_first.execute(f"select oid, in_cart from cart_item where cid='{cid}' and vid='{vid}' order by in_cart desc")
            y = cursor_first.fetchone()
            in_cart_value = int(y[1])
            if (in_cart_value==1):
                current_order_id = y[0]
                request.session['current_order_id'] = current_order_id
            else:
                cursor00 = db.cursor()            
                cursor00.execute(f"select count(distinct oid) from cart_item where cid='{cid}';")
                order_number = int(cursor00.fetchone()[0]) + 1
                current_order_id = f"{cid}_{order_number}"
                request.session['current_order_id'] = current_order_id
            
            if request.method=="POST":
                # print("HelloPost1")
                item_id = request.POST.get('addBtn')
                qty = int(request.POST.get('qty'))
                pack = request.POST.get('pack')
                pack_int = 0
                if pack == 'on':
                    # print("HelloPost2")
                    pack_int = 1
                else:
                    # print("HelloPost3")
                    pack_int = 0
                cursor01 = db.cursor()
                cursor01.execute(f"select * from cart_item where in_cart=1 and cid='{cid}' and oid='{current_order_id}' and item_id='{item_id}'")
                if(cursor01.fetchone()):
                    # print("HelloPost4")
                    if (qty !=0):
                        # print(f"HelloPost5 -- {item_id} -- {qty} -- {current_order_id}")
                        cursor09 = db.cursor()
                        cursor09.execute(f"update cart_item set quantity={qty}, pack_flag={pack_int} where item_id='{item_id}' and oid='{current_order_id}'")
                        db.commit()
                    else:
                        # print("HelloPost6")
                        cursor06 = db.cursor()
                        cursor06.execute(f"delete from cart_item where item_id = '{item_id}' and oid='{current_order_id}'")
                        db.commit()
                else:
                    # print("HelloPost7")
                    if (qty != 0):
                        # print("HelloPost8")
                        cursor04 = db.cursor()
                        cursor04.execute(f"select item_price from item where item_id='{item_id}'")
                        item_price = int(cursor04.fetchone()[0])
                        cursor02 = db.cursor()
                        cursor02.execute(f"insert into cart_item values('{item_id}', '{current_order_id}', {qty}, '{vid}', '{cid}', {item_price}, {pack_int}, 1)")
                        db.commit()

                # print(request.POST.get('qty'))
                # print(request.POST.get('pack'))
                # print(request.POST.get('addBtn'))
                # print(cid)
            
            cursor1 = db.cursor()
            cursor1.execute(f"select * from item left join vendor on item.vid = vendor.vid where vendor.shop_name = '{outlet_name}' and vendor.deleted=0 order by item_name, item_availability desc")
            vendor_items = cursor1.fetchall()
            # print(vendor_items)
            vendor_name = outlet_name

            # cursor08 = db.cursor()
            # cursor08.execute(f"select * from cart_item where oid='{current_order_id}' and cid='{cid} and in_cart=1'")
            # x = cursor08.fetchall()
            data = {
                'cid':cid,
                'vendor_items':vendor_items,
                'vendor_name': vendor_name,
                # 'cart_items':x,
                }
            # print(data)
            return render(request,"studentOutlet.html", data)
    except Exception as e:
        print("Exception:",e)
        return render(request,"studentOutlet.html")

def studentExpense(request):
    try:
        if request.session.has_key('cid'):
            cid = request.session['cid']
            # print(cid)
            cursor3 = db.cursor()
            cursor3.execute(f"select c_fname, c_lname from customer where cid = '{cid}'")
            name_row = cursor3.fetchone()
            name = name_row[0]+' ' + name_row[1]
            print(name[0]+' ' + name[1])
            # cursor02 = db.cursor()
            cursor03 = db.cursor()
            # cursor02.execute(f"select count(*) from cart_item, orders where cart_item.item_id = orders.item_id and cart_item.in_cart = 0 and cart_item.cid = '{cid}'")
            cursor03.execute(f"select sum(cart_item.quantity*cart_item.order_item_price) from cart_item where in_cart = 0 and cid = '{cid}';")
            # count = cursor02.fetchone()[0]
            expenses = cursor03.fetchone()[0]
            # for i in range(count):
            #     expenses += cursor03.fetchone()[3]
            data = {
                'cid':cid,
                'expense':expenses,
                'name': name,
                }
            print(data)
            return render(request,"studentExpense.html", data)
    except Exception as e:
        print("Exception:",e)
        return render(request,"studentExpense.html")

def studentCurrentOrders(request):
    try:
        if request.session.has_key('cid'):
            cid = request.session['cid']
            cursor1 = db.cursor()
            cursor2 = db.cursor()
            cursor3 = db.cursor()
            cursor1.execute(f"select * from cart_item left join orders on cart_item.cid = orders.cid and cart_item.oid = orders.oid where orders.cid = '{cid}' and is_prepared_flag=0 order by date_time desc")
            cursor2.execute(f"select count(*) from cart_item left join orders on cart_item.cid = orders.cid and cart_item.oid = orders.oid where orders.cid = '{cid}' and is_prepared_flag=0")
            count = cursor2.fetchone()[0]
            dict1 = dict()
            print(count)
            
            for i in range(count):
                x = cursor1.fetchone()
                # print(x)
                oid = x[1]
                print(oid)
                items = dict()
                
                if oid in dict1.keys():
                    dict1[oid][0] += x[5]*x[2]
                    cursor3.execute(f"select item_name from item where item_id='{x[0]}'")
                    item_name = cursor3.fetchone()[0]
                    dict1[oid][3][item_name] = x[2]
                    # print('1: ' + dict1)
                else:
                    date = x[12].strftime("%x")
                    time = x[12].strftime("%X")
                    amount = x[5]*x[2]
                    # print(date+'' + ''+time+'' + amount)
                    cursor3.execute(f"select item_name from item where item_id='{x[0]}'")
                    item_name = cursor3.fetchone()[0]
                    items[item_name] = x[2]
                    dict1[oid] = [amount, date, time, items]
                    # print('2: ' + dict1)
            # print('final: ' + dict1)

            data = {
                'cid':cid,
                'orders':dict1
                }
            print(data)
            return render(request,"studentCurrentOrders.html", data)
    except Exception as e:
        print("Exception:",e)
        return render(request,"studentCurrentOrders.html")

def studentPastOrders(request):
    try:
        if request.session.has_key('cid'):
            cid = request.session['cid']
            cursor1 = db.cursor()
            cursor2 = db.cursor()
            cursor3 = db.cursor()
            cursor1.execute(f"select date_time, oid from orders where cid = '{cid}' and is_prepared_flag = 1 order by date_time desc")
            cursor2.execute(f"select count(*) from orders where cid = '{cid}' and is_prepared_flag = 1")
            
            count = cursor2.fetchone()[0]
            dict1 = dict()
            
            for i in range(count):
                x = cursor1.fetchone()
                oid = x[1]
                
                if oid in dict1.keys():
                    # dict1[oid][0] += x[5]*x[2]
                    pass
                else:
                    date = x[0].strftime("%x")
                    time = x[0].strftime("%X")
                    cursor3.execute(f"select sum(cart_item.quantity*cart_item.order_item_price) as amount from cart_item, orders where cart_item.oid = orders.oid and cart_item.item_id = orders.item_id and orders.oid ='{oid}'")
                    # amount = x[5]*x[2]
                    amount = cursor3.fetchone()[0]
                    dict1[oid] = [amount, date, time]
            print(dict1)

            data = {
                'cid':cid,
                'orders':dict1
                }
            print(data)
            return render(request,"studentPastOrders.html", data)
    except Exception as e:
        print("Exception:",e)
        return render(request,"studentPastOrders.html")

def studentPastOrderDetails(request):
    try:
        if request.session.has_key('cid'):
            cid = request.session['cid']
            # print(cid)
            orderid = None
            if request.method=="POST":
                # print("I am here hello")
                orderid = request.POST['orderid']
                cursor1 = db.cursor()
                cursor2 = db.cursor()
                cursor3 = db.cursor()
                cursor1.execute(f"select * from cart_item left join orders on cart_item.cid = orders.cid and cart_item.oid = orders.oid where orders.cid = '{cid}' and is_prepared_flag=1 and orders.oid='{orderid}'")
                cursor2.execute(f"select count(*) from cart_item left join orders on cart_item.cid = orders.cid and cart_item.oid = orders.oid where orders.cid = '{cid}' and is_prepared_flag=1 and orders.oid='{orderid}'")
                
                cursor04 = db.cursor()
                cursor04.execute(f"select sum(cart_item.quantity*cart_item.order_item_price) as amount from cart_item, orders where cart_item.oid = orders.oid and cart_item.item_id = orders.item_id and orders.oid ='{orderid}'")
                expense = cursor04.fetchone()[0]
                count = cursor2.fetchone()[0]
                dict1 = dict()
                for i in range(count):
                    x = cursor1.fetchone()
                    # print(x)
                    oid = x[1]
                    print(oid)
                    items = dict()
                    
                    if oid in dict1.keys():
                        dict1[oid][0] += x[5]*x[2]
                        cursor3.execute(f"select item_name from item where item_id='{x[0]}'")
                        item_name = cursor3.fetchone()[0]
                        dict1[oid][3][item_name] = x[2]
                        # print('1: ' + dict1)
                    else:
                        date = x[12].strftime("%x")
                        time = x[12].strftime("%X")
                        amount = x[5]*x[2]
                        # print(date+'' + ''+time+'' + amount)
                        cursor3.execute(f"select item_name from item where item_id='{x[0]}'")
                        item_name = cursor3.fetchone()[0]
                        items[item_name] = x[2]
                        dict1[oid] = [amount, date, time, items]
            data = {
                'cid':cid,
                'orders':dict1,
                'expense': expense,
                }
            print(data)
            return render(request,"studentPastOrderDetails.html", data)
    except Exception as e:
        print("Exception:",e)
        return render(request,"studentPastOrderDetails.html")

def studentCart(request, vendor_name):
    try:
        if request.session.has_key('cid'):
            cid = request.session['cid']
            print(cid)
            oid = request.session['current_order_id']
            if(request.method=="POST"):
                item_id = request.POST.get('deleteCartBtn')
                cursor02 = db.cursor()
                cursor02.execute(f"delete from cart_item where cid='{cid}' and item_id='{item_id}' and in_cart=1")
                db.commit()
            cursor00 = db.cursor()
            cursor01 = db.cursor()
            cursor01.execute(f"select count(*) from cart_item where cid='{cid}' and oid='{oid}' and in_cart=1")
            cursor00.execute(f"select * from cart_item where cid='{cid}' and oid='{oid}' and in_cart=1")
            count = int(cursor01.fetchone()[0])
            data = {}
            if (count==0):
                data = {
                'cid':cid,
                'vendor_name':vendor_name,
                'noData': True,
                }
                return render(request,"studentCart.html", data)
            dict1 = dict()
            expense = 0
            for i in range(count):
                x = cursor00.fetchone()
                item_id = x[0]
                qty = x[2]
                price = x[5]
                expense += qty*price
                pack = x[6]
                cursor04 = db.cursor()
                cursor04.execute(f"select item_name from item where item_id='{item_id}'")
                item_name = cursor04.fetchone()[0]
                dict1[item_id] = [qty, price, pack, item_name]
            data = {
                'cid':cid,
                'vendor_name':vendor_name,
                'oid' :oid,
                'cart_items':dict1,
                'total_amount':expense,
                'noData': False,
                }
            print(data)
            return render(request,"studentCart.html", data)
    except Exception as e:
        print("Exception:",e)
        return render(request,"studentCart.html")

def orderComplete(request):
    try:
        if request.session.has_key('cid'):
            cid = request.session['cid']
            print(cid)
            # print("in ocPost")
            # print("in ocPost")
            oid = request.session['current_order_id']
            cursor00 = db.cursor()
            cursor00.execute(f"select count(*) from cart_item where oid='{oid}' and cid='{cid}' and in_cart=1")
            count = int(cursor00.fetchone()[0])
            # print(f"I am hereeeee000 {count}")
            cursor01 = db.cursor()
            cursor01.execute(f"select item_id from cart_item where oid='{oid}' and cid='{cid}' and in_cart=1")
            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            for i in range(count):
                x = cursor01.fetchone()
                # print(f"I am hereeeee {x}")
                cursor02 = db.cursor()
                cursor02.execute(f"insert into orders values('{cid}', '{x[0]}', '{oid}', 0, '{date_time}')")
                db.commit()
            cursor03 = db.cursor()
            cursor03.execute(f"update cart_item set in_cart=0 where oid='{oid}' and cid='{cid}'")
            db.commit()
            # print("in2 ocPost")
            return redirect('/student-login/dashboard/current-orders/')
    except Exception as e:
        print("Exception:",e)

def logout(request):
    try:
        if request.session.has_key('cid'):
            del request.session['cid']
        return redirect('/student-login/')
    except Exception as e:
        print("Exception:",e)

def vendorLogin(request):
    try:
        if request.method=="POST":
            vid = request.POST.get("vid")
            print(vid)
            v_password = request.POST.get("v_password")
            cursor = db.cursor()
            cursor.execute(f"select * from vendor where vid = '{vid}' and deleted = 0")
            data = cursor.fetchone()
            if(v_password==data[7]):
                print(data)
                request.session['vid'] = vid
                return redirect('/vendor-login/dashboard/')
    except Exception as e:
        print("Exception1:",e)
    return render(request,"vendorLogin.html")

def vendorDashboard(request):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            if request.method == 'POST':
                if 'turn_on' in request.POST:
                    cursor0 = db.cursor()
                    cursor0.execute(f"update item set item_availability = 1 where item_id = '{request.POST.get('turn_on')}'")
                    db.commit()
                elif 'turn_off' in request.POST:
                    cursor0 = db.cursor()
                    cursor0.execute(f"update item set item_availability = 0 where item_id = '{request.POST.get('turn_off')}'")
                    db.commit()
            cursor1 = db.cursor()
            cursor1.execute(f"select count(*) from item where vid = '{vid}' and deleted = 0")
            cursor2 = db.cursor()
            cursor2.execute(f"select item_name, item_availability, item_id from item where vid = '{vid}' and deleted = 0")
            cursor3 = db.cursor()
            cursor3.execute(f"select open from vendor where vid = '{vid}' and deleted = 0")
            open = cursor3.fetchone()[0]
            item_id = dict()
            for i in range(cursor1.fetchone()[0]):
                x = cursor2.fetchone()
                item_id[x[2]] = [x[0], x[1]]
            print(item_id)
            data = {
                'vid':vid,
                'item_id':item_id,
                'open':open,
                }
            return render(request,"vendorDashboard.html",data)
    except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorDashboard.html")

def vendorEditItem(request, item_id):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            if request.method == 'POST':
                new_item_name = request.POST.get('itemname')
                new_price = request.POST.get('price')
                cursor0 = db.cursor()
                cursor0.execute(f"update item set item_name = '{new_item_name}', item_price = {new_price} where item_id = '{item_id}'")
                db.commit()
                return redirect('/vendor-login/dashboard/')
            cursor1 = db.cursor()
            cursor1.execute(f"select item_name, item_price from item where item_id = '{item_id}'")
            x = cursor1.fetchone()
            data = {
                'vid':vid,
                'item_id':item_id,
                'item_name':x[0],
                'item_price':x[1],
                }
            return render(request,"vendorEditItem.html",data)
    except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorEditItem.html")

def vendorDeleteItem(request, item_id):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            if request.method == 'POST':
                cursor0 = db.cursor()
                cursor0.execute(f"update item set deleted = 1 where item_id = '{item_id}'")
                db.commit()
                return redirect('/vendor-login/dashboard/')
            cursor1 = db.cursor()
            cursor1.execute(f"select item_name, item_price from item where item_id = '{item_id}'")
            x = cursor1.fetchone()
            data = {
                'vid':vid,
                'item_id':item_id,
                'item_name':x[0],
                'item_price':x[1],
                }
            return render(request,"vendorDeleteItem.html",data)
    except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorDeleteItem.html")

def vendorAddItem(request):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            data = {
                'vid':vid,
                }
            if request.method == "POST":
                cursor1 = db.cursor()
                cursor2 = db.cursor()
                itemname = request.POST.get('itemname')
                price = request.POST.get('price')
                
                cursor1.execute(f"select count(*) from item where vid='{vid}'")
                count = cursor1.fetchone()[0]
                item_id = vid + str(count)
                cursor2.execute(f"insert into item values('{item_id}', '{vid}', '{itemname}', {price}, {1}, {0})")
                db.commit()
            return render(request,"vendorAddItem.html",data)
    except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorAddItem.html")

def vendorCurrentOrders(request):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            cursor1 = db.cursor()
            cursor2 = db.cursor()
            cursor3 = db.cursor()
            cursor1.execute(f"select * from cart_item left join orders on cart_item.item_id = orders.item_id and cart_item.oid = orders.oid where vid = '{vid}' and is_prepared_flag=0 order by date_time desc")
            cursor2.execute(f"select count(*) from cart_item left join orders on cart_item.item_id = orders.item_id and cart_item.oid = orders.oid where vid = '{vid}' and is_prepared_flag=0")
            count = cursor2.fetchone()[0]
            dict1 = dict()
            
            for i in range(count):
                x = cursor1.fetchone()
                oid = x[1]
                items = dict()
                
                if oid in dict1.keys():
                    dict1[oid][0] += x[5]*x[2]
                    cursor3.execute(f"select item_name from item where item_id='{x[0]}' and vid='{vid}'")
                    item_name = cursor3.fetchone()[0]
                    dict1[oid][3][item_name] = x[2]
                else:
                    date = x[12].strftime("%x")
                    time = x[12].strftime("%X")
                    amount = x[5]*x[2]
                    cursor3.execute(f"select item_name from item where item_id='{x[0]}' and vid='{vid}'")
                    item_name = cursor3.fetchone()[0]
                    items[item_name] = x[2]
                    dict1[oid] = [amount, date, time, items]
            print(dict1)

            data = {
                'vid':vid,
                'orders':dict1
                }
            print(data)
            return render(request,"vendorCurrentOrders.html",data)
    except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorCurrentOrders.html")

def vendorCurrentOrdersPrepared(request, oid):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            cursor1 = db.cursor()
            cursor1.execute(f"update orders set is_prepared_flag = 1 where oid = '{oid}'")
            db.commit()
            data = {
                'vid':vid,
            }
            return redirect('/vendor-login/dashboard/current-orders')
    except Exception as e:
        print("Exception2:",e)
        return redirect('/vendor-login/dashboard/current-orders')

def vendorPastOrders(request):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            cursor1 = db.cursor()
            cursor2 = db.cursor()
            cursor1.execute(f"select orders.oid, order_item_price, quantity, date_time from cart_item left join orders on cart_item.item_id = orders.item_id and cart_item.oid = orders.oid where vid = '{vid}' and is_prepared_flag=1 order by date_time desc")
            cursor2.execute(f"select count(*) from cart_item left join orders on cart_item.item_id = orders.item_id and cart_item.oid = orders.oid where vid = '{vid}' and is_prepared_flag=1")
            count = cursor2.fetchone()[0]
            dict1 = dict()
            income = 0
            for i in range(count):
                x = cursor1.fetchone()
                oid = x[0]
                
                if oid in dict1.keys():
                    dict1[oid][0] += x[1]*x[2]
                else:
                    date = x[3].strftime("%x")
                    time = x[3].strftime("%X")
                    amount = x[1]*x[2]
                    income += amount
                    dict1[oid] = [amount, date, time]
            
            cursor3 = db.cursor()
            cursor3.execute(f"update vendor set v_income = {income} where vid='{vid}' and deleted=0")
            db.commit()

            data = {
                'vid':vid,
                'orders':dict1
                }
            print(data)
            return render(request,"vendorPastOrders.html",data)
    except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorPastOrders.html")

def vendorPastOrderDetails(request, oid):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            cursor1 = db.cursor()
            cursor1.execute(f"select orders.item_id, item_name, order_item_price, quantity, date_time from item, cart_item, orders where item.item_id = cart_item.item_id and cart_item.oid = orders.oid and orders.item_id = cart_item.item_id and orders.oid = '{oid}'")
            cursor2 = db.cursor()
            cursor2.execute(f"select count(*) from item, cart_item, orders where item.item_id = cart_item.item_id and cart_item.oid = orders.oid and orders.item_id = cart_item.item_id and orders.oid = '{oid}'")
            count = cursor2.fetchone()[0]
            items = dict()
            amount = 0
            for i in range(count):
                x = cursor1.fetchone()
                items[x[0]] = [x[1], x[2], x[3], x[2]*x[3]]
                amount += x[2]*x[3]
            data = {
                'vid':vid,
                'oid':oid,
                'items': items,
                'date' : x[4].strftime("%x"),
                'time' : x[4].strftime("%X"),
                'amount' : amount,
                'count' : count,
                }
            return render(request,"vendorPastOrderDetails.html",data)
    except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorPastOrderDetails.html")

def vendorIncome(request):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            cursor1 = db.cursor()
            cursor2 = db.cursor()
            cursor3 = db.cursor()
            cursor1.execute(f"select * from cart_item left join orders on cart_item.item_id = orders.item_id and cart_item.oid = orders.oid where vid = '{vid}' and is_prepared_flag=1")
            cursor2.execute(f"select count(*) from cart_item left join orders on cart_item.item_id = orders.item_id and cart_item.oid = orders.oid where vid = '{vid}' and is_prepared_flag=1")
            cursor3.execute(f"select shop_name from vendor where vid = '{vid}' and deleted=0")
            count = cursor2.fetchone()[0]
            income = 0
            for i in range(count):
                x = cursor1.fetchone()
                income+=x[5]*x[2]

            data = {
                'vid':vid,
                'income':income,
                'name': cursor3.fetchone()[0]
                }
            return render(request,"vendorIncome.html",data)
    except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorIncome.html")

def vendorShopStatus(request,status):
     try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            print(status)
            cursor1 = db.cursor()
            cursor1.execute(f"update vendor set open = {status} where vid = '{vid}' and deleted = 0")
            return redirect("/vendor-login/dashboard/")
     except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorDashboard.html")

def vendorLogout(request):
    try:
        if request.session.has_key('vid'):
            del request.session['vid']
        return redirect('/vendor-login/')
    except Exception as e:
        print("Exception:",e)
