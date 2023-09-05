from django.shortcuts import render
import mysql.connector
from django.http import HttpResponseRedirect
from datetime import datetime

from django.core.files.storage import FileSystemStorage


mydb=mysql.connector.connect(host="localhost",user="root",passwd="",database="ecom")
mycursor=mydb.cursor(buffered=True)

# Create your views here.
def index(request):    
    query="""select * from products"""
    mycursor.execute(query)
    product=mycursor.fetchall()
    print(product)
    return render(request,"index.html",{"product":product})
def shop(request):
    return render(request,"shop.html")
def cart(request):  
    subtotal=0
    newCart=[]
    if 'cart' in request.session:
        cart=request.session['cart']
        for i in cart:
            id=i[0]
            query="""select * from products where id=%s"""
            val=(id,)
            mycursor.execute(query,val)
            prod=mycursor.fetchone()
            img=prod[6]
            name=prod[1]
            price=prod[3]
            qty=i[1]
            total=int(price)*int(qty)
            subtotal=subtotal+total
            child=[img,name,price,qty,total]
            newCart.append(child)
                
    gst=subtotal*(18/100)
    net=subtotal+gst
    return render(request,"cart.html",{"cart":newCart,"sub":subtotal,"net":net,"gst":gst})
def carts(request,id):
    return render(request,"cart.html")
def checkout(request):    
    if 'cart' in request.session:
        if 'user_id' in request.session:
            subtotal=0
            net=0
            gst=0
            newCart=[]
            if 'cart' in request.session:
                cart=request.session['cart']
                for i in cart:
                        id=i[0]
                        query="""select * from products where id=%s"""
                        val=(id,)
                        mycursor.execute(query,val)
                        prod=mycursor.fetchone()
                        img=prod[6]
                        name=prod[1]
                        price=prod[3]
                        qty=i[1]
                        total=int(price)*int(qty)
                        subtotal=subtotal+total
                        child=[img,name,price,qty,total]
                        newCart.append(child)
                            
                        gst=subtotal*(18/100)
                        net=subtotal+gst
            uid=request.session['user_id']
            query="""select * from address where uid=%s"""
            val=(uid,)
            mycursor.execute(query,val)
            count=mycursor.rowcount
            if count>0:
                address=mycursor.fetchone()
                return render(request,"checkout.html",{"address":address,"items":newCart,"sub":subtotal,"net":net,"gst":gst})
            else:
                address=[]
                return render(request,"checkout.html",{"address":address,"items":newCart,"sub":subtotal,"net":net,"gst":gst})

        else:
            return HttpResponseRedirect(redirect_to="login")
    
    else:
        return HttpResponseRedirect(redirect_to="cart")

def login(request):
    return render(request,"login.html")
def register(request):
    return render(request,"login.html")
def dash(request):
    username=request.session['user_name']
    ordersQuery="""select * from orders"""
    pendingQuery="""select * from orders where status='0'"""
    deliverQuery="""select * from orders where status='1'"""
    mycursor.execute(ordersQuery)
    overall=mycursor.rowcount
    orders=mycursor.fetchall()
    mycursor.execute(pendingQuery)
    pending=mycursor.rowcount
    mycursor.execute(deliverQuery)
    deliver=mycursor.rowcount
    return render(request,"dash.html",{'username':username,"overall":overall,"pending":pending,"deliver":deliver,"orders":orders})

def userdash(request):
    username=request.session['user_name']
    uid=request.session['user_id']
    ordersQuery="""select * from orders where uid=%s"""
    ordersVal=(uid,)
    pendingQuery="""select * from orders where uid=%s and status='0'"""
    pendingVal=(uid,)
    deliverQuery="""select * from orders where uid=%s and status='1'"""
    deliverVal=(uid,)
    mycursor.execute(ordersQuery,ordersVal)
    overall=mycursor.rowcount
    orders=mycursor.fetchall()
    mycursor.execute(pendingQuery,pendingVal)
    pending=mycursor.rowcount
    mycursor.execute(deliverQuery,deliverVal)
    deliver=mycursor.rowcount
    return render(request,"userdash.html",{'username':username,"overall":overall,"pending":pending,"deliver":deliver,"orders":orders})
def add_products(request):
    return render(request,"add_products.html")
def view_products(request):
    query="""select * from products"""
    mycursor.execute(query)
    prod=mycursor.fetchall
    return render(request,"view_products.html",{"prod":prod})
def view_pending(request):    
    pendingQuery="""select * from orders where status='0'"""
    mycursor.execute(pendingQuery)
    order=mycursor.fetchall()
    orders=[]
    for i in order:
        oid=i[0]
        query="""select * from items where oid=%s"""
        val=(oid,)
        mycursor.execute(query,val)
        items=mycursor.fetchall()
        uid=i[2]
        cquery="""select * from user where id=%s"""
        cval=(uid,)
        mycursor.execute(cquery,cval)
        user=mycursor.fetchone()
        uname=user[1]
        umobile=user[2]
        sno=0
        for j in items:
            qty=j[3]
            pid=j[2]
            psql="""select * from products where id=%s"""
            pval=(pid,)
            mycursor.execute(psql,pval)
            prod=mycursor.fetchone()
            name=prod[1]
            img=prod[6]
            sno=sno+1
            child=[sno,oid,name,qty,img,uname,umobile]
            orders.append(child)
    return render(request,"view_pending.html",{"orders":orders})
def view_status(request):
    return render(request,"view_status.html")
def view_delivered(request):
    pendingQuery="""select * from orders where status='1'"""
    mycursor.execute(pendingQuery)
    order=mycursor.fetchall()
    orders=[]
    for i in order:
        oid=i[0]
        query="""select * from items where oid=%s"""
        val=(oid,)
        mycursor.execute(query,val)
        items=mycursor.fetchall()
        uid=i[2]
        cquery="""select * from user where id=%s"""
        cval=(uid,)
        mycursor.execute(cquery,cval)
        user=mycursor.fetchone()
        uname=user[1]
        umobile=user[2]
        sno=0
        for j in items:
            qty=j[3]
            pid=j[2]
            psql="""select * from products where id=%s"""
            pval=(pid,)
            mycursor.execute(psql,pval)
            prod=mycursor.fetchone()
            name=prod[1]
            img=prod[6]
            sno=sno+1
            child=[sno,oid,name,qty,img,uname,umobile]
            orders.append(child)
    return render(request,"view_delivered.html",{"orders":orders})
def detail(request,id):
    query="""select * from products where id=%s"""
    val=(id,)
    mycursor.execute(query,val)
    product=mycursor.fetchone()
    return render(request,"detail.html",{"product":product})

def register_user(request):
    name=request.GET['name']
    mobile=request.GET['mobile']
    password=request.GET['password']

    query="""insert into user(name,mobile,password)values(%s,%s,%s)"""
    val=(name,mobile,password)
    mycursor.execute(query,val)
    mydb.commit()
    return HttpResponseRedirect(redirect_to="login")

def signin_user(request):
    mobile=request.GET['mobile']
    password=request.GET['password']

    if mobile=="admin" and password=="admin":
        request.session['user_type']="admin"
        request.session['user_id']=0        
        request.session['user_name']="Admin"

        return HttpResponseRedirect(redirect_to="dash")
    else:
        query="""select * from user where mobile=%s and password=%s"""
        val=(mobile,password)
        mycursor.execute(query,val)
        count=mycursor.rowcount
        if count>0:         
            user=mycursor.fetchone()   
            request.session['user_type']="user"
            request.session['user_id']=user[0]        
            request.session['user_name']=user[1]
            return HttpResponseRedirect(redirect_to="userdash")
        else:        
            return HttpResponseRedirect(redirect_to="login")

def logout(request):
    del request.session['user_type']
    del request.session['user_id']     
    del request.session['user_name']
    return HttpResponseRedirect(redirect_to="index")




def add_prod_details(request):
    name=request.POST['name']
    aprice=request.POST['aprice']
    dprice=request.POST['dprice']
    description=request.POST['description']
    info=request.POST['info']
    if len(request.FILES) !=0:
        img=request.FILES['pimgone'] 
        fs = FileSystemStorage()
        filename = fs.save(img.name, img)
        uploaded_file_url = fs.url(filename)
        pimgone=uploaded_file_url
        print(pimgone)
        
        img=request.FILES['pimgtwo'] 
        fs = FileSystemStorage()
        filename = fs.save(img.name, img)
        uploaded_file_url = fs.url(filename)
        pimgtwo=uploaded_file_url
        print(pimgtwo)

        
        img=request.FILES['pimgthree'] 
        fs = FileSystemStorage()
        filename = fs.save(img.name, img)
        uploaded_file_url = fs.url(filename)
        pimgthree=uploaded_file_url
        print(pimgthree)
        
        
        img=request.FILES['pimgfour'] 
        fs = FileSystemStorage()
        filename = fs.save(img.name, img)
        uploaded_file_url = fs.url(filename)
        pimgfour=uploaded_file_url
        print(pimgfour)

        query="""insert into products(name,aprice,dprice,description,info,imgone,imgtwo,imgthree,imgfour)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        val=(name,aprice,dprice,description,info,pimgone,pimgtwo,pimgthree,pimgfour)
        mycursor.execute(query,val)
        mydb.commit()
        return HttpResponseRedirect(redirect_to="dash")
    else:
        return HttpResponseRedirect(redirect_to="add_products")
    

def add_to_cart(request):
    pro_id=request.GET['id']
    pro_qty=request.GET['qty']
    if 'cart' not in request.session:
        cart=[]
        cart.append([pro_id,pro_qty])
        request.session['cart']=cart
    else:
        cart=request.session['cart']        
        cart.append([pro_id,pro_qty])
        request.session['cart']=cart
        print(cart)

    return HttpResponseRedirect(redirect_to="index")

def place_order(request):
    uid=request.session['user_id']
    name=request.GET['name']
    email=request.GET['email']
    mobile=request.GET['mobile']
    address=request.GET['address']
    city=request.GET['city']
    state=request.GET['state']
    pin=request.GET['pin']
    query="insert into address(uid,name,email,mobile,address,city,state,pin)values(%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(uid,name,email,mobile,address,city,state,pin)
    mycursor.execute(query,val)
    mydb.commit()
    aid=mycursor.lastrowid    
    cart=request.session['cart']
    subtotal=0
    gst=0
    net=0
    for i in cart:
        id=i[0]
        query="""select * from products where id=%s"""
        val=(id,)
        mycursor.execute(query,val)
        prod=mycursor.fetchone()
        img=prod[6]
        name=prod[1]
        price=prod[3]
        qty=i[1]
        total=int(price)*int(qty)
        subtotal=subtotal+total                        
        gst=subtotal*(18/100)
        net=subtotal+gst  
    sql="""insert into orders (aid,uid,subtotal,gst,net,status)values(%s,%s,%s,%s,%s,%s)"""  
    sqlVal=(aid,uid,subtotal,gst,net,0)
    mycursor.execute(sql,sqlVal)
    mydb.commit()
    oid=mycursor.lastrowid
    for j in cart:
        pid=j[0]
        pqty=j[1]
        insql="""insert into items(oid,pid,qty)values(%s,%s,%s)"""
        val=(oid,pid,pqty)
        mycursor.execute(insql,val)
        mydb.commit()
    del request.session['cart']
    

    return HttpResponseRedirect(redirect_to="index")

def process(request,id):
    query="""update orders set status=1 where id=%s"""
    val=(id,)
    mycursor.execute(query,val)
    mydb.commit()
    return HttpResponseRedirect(redirect_to="dash")

def decline(request,id):
    query="""delete from orders where id=%s"""
    val=(id,)
    mycursor.execute(query,val)
    mydb.commit()
    return HttpResponseRedirect(redirect_to="dash")
