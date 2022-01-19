import hashlib
import datetime as dt
from models import User, FoodItem, Order

userid = None


def validateuser(username, password):
    for user in User.allusers():
        if user["username"] == username and user["password"] == password:
            global userid
            userid = user['userid']
            return True
    return False


def createuser(update=False):
    username = input("Full Name: ")
    phonenumber = input("Phone Number: ")
    email = input("Email: ")
    address = input("Address: ")
    password = input("Password: ")
    repassword = input("Re-Enter Password: ")
    while repassword != password:
        print("Password Doesnt Match")
        password = input("Password: ")
        repassword = input("Re-Enter Password: ")
    if update:
        user = User(username, phonenumber, email, address, password, userid, True)
        print("Account Updated Successful, please use your full name as username")
    else:
        user = User(username, phonenumber, email, address, password)
        print("Account Created Successful, please use your full name as username")


def validatestock(orderlist, orderdic):
    seletedorders = {}
    for i in orderlist:
        for item in FoodItem.allfooditems():
            if item['foodid'] == orderdic[i]:
                if item['foodid'] in seletedorders:
                    seletedorders[item['foodid']] += 1
                else:
                    seletedorders[item['foodid']] = 1
    for foodid in seletedorders:
        for item in FoodItem.allfooditems():
            if item['foodid'] == foodid:
                if seletedorders[foodid] > int(item['stock']):
                    print('only', item['stock'], item['name'], 'are available in stock')
                    print('you ordered', seletedorders[foodid])
                    print('please order again with value lesser than stock')
                    return False
    return True


def placeorder():
    n = 1
    orderdic = {}
    seletedorders = []
    for item in FoodItem.allfooditems():
        if item['active'] == 'True' and int(item['stock']) > 0:
            if item['discount'] == '0':
                print('%s)%s (%s) [INR %s]' % (n, item["name"], item["quantity"], item["price"]))
            else:
                print('%s)%s (%s) [INR %s] (discount %s%%)' % (
                n, item["name"], item["quantity"], item["price"], item['discount']))
            orderdic[n] = item['foodid']
            n += 1
    if n == 1:
        print("No item is available to buy")
        return
    print('enter 0 to cancel')
    order = input("enter comma separated order numbers, if multiple same orders then repeat order numbers: ")
    if order == '0':
        return
    orderlist = list(map(int, order.split(',')))

    if not validatestock(orderlist, orderdic):
        return
    myorders = {}
    for item in orderlist:
        if item in myorders:
            myorders[item] += 1
        else:
            myorders[item] = 1
        seletedorders.append(orderdic[item])
    print("selected orders are :- ")
    totalamount = 0
    n = 1
    for i in myorders:
        for item in FoodItem.allfooditems():
            if item['foodid'] == orderdic[i]:
                print('%s)%s (%s) [%s]  X%s : amount = [%s]' % (n, item["name"], item["quantity"], item["price"],myorders[i], myorders[i]*(int(item["price"]) - int(item["price"]) * float(item['discount']) / 100)))
                n += 1
                #seletedorders.append(item['foodid'])
                totalamount += myorders[i]*(int(item["price"]) - int(item["price"]) * float(item['discount']) / 100)
                break
    print('Total Amount after discount:', totalamount)
    orderconfirm = int(input("enter 1 to confirm order, 0 to cancel: "))
    if orderconfirm == 1:
        FoodItem.updatestock(seletedorders.copy())
        try:
            oh = Order(userid, seletedorders.copy())
        except Exception as ex:
            print(ex.args)
        print("order placed")


def userfn():
    while True:
        print("\n\n\n")
        print('1) Place New Order')
        print('2) Order History')
        print('3) Update Profile')
        print('4) My Favorite Food')
        print("enter 0 to logout ")
        try:
            choose = int(input())
            if choose == 1:
                placeorder()
            elif choose == 2:
                Order.userhistory(userid)
            elif choose == 3:
                createuser(update=True)
            elif choose == 4:
                Order.UserFavoriteFood(userid)
            elif choose == 0:
                return
            else:
                print("option not valid")
            input('press enter to continue...')
        except:
            print("option not valid")
        # data.upadatefiles()
