from models import FoodItem, Order
import hashlib

def adminlogincheck(username,password):
    with open('admindetails.txt', 'r') as f:
        details = f.readline()
        adminusername = details.split(':')[0]
        adminpass = details.split(':')[1]
    if adminusername == username and adminpass == password:
        return True
    else:
        return False


def addFoodItem():
    name = input("Name: ")
    quantity = input("Quantity: ")
    price = input("Price: ")
    discount = input("Discount(%): ")
    stock = input("Stock: ")
    adminuser = FoodItem(name, quantity, price, discount, stock)
    print(name,'added successfully')

def editfoodItem(foodid):
    print('1) Update Item Stock')
    print('2) edit Item details')
    choose = int(input())
    if choose == 1:
        print('name = %s \nAvailable Stock = %s \n'%( FoodItem.food(foodid)['name'], FoodItem.food(foodid)['stock']))
        addstock = int(input("enter new stock: "))
        FoodItem.food(foodid)['stock'] = int(FoodItem.food(foodid)['stock']) + addstock
        FoodItem.UpdateFoodItemFile()
        print('Stocked Updated Successfully')

    if choose == 2:

        edititem = None
        for item in FoodItem.allfooditems():
            if item['foodid'] == foodid:
                edititem = item
                break
        if edititem is None:
            print(foodid, "not found")
        else:
            print(edititem)
            name = input("Updated Name: ")
            quantity = input("Updated Quantity: ")
            price = input("Updated Price: ")
            discount = input("Updated Discount(%): ")
            stock = input("Updated Stock: ")
            adminuser = FoodItem(name, quantity, price, discount, stock, foodid, True)
            print('item updated successfully')


def viewAllFoodItems():
    if not FoodItem.allfooditems():
        print('No food items present, please add food items.')
    for item in FoodItem.allfooditems():
        if item['active'] == 'True':
            for key in item:
                print(key, ":", item[key])
            print('.................................')


def UpdateAdminProfile():
    username = input("enter new username: ")
    password = input("enter new password: ")
    repassword = input("Re-Enter Password: ")
    while repassword != password:
        print("Password Doesnt Match")
        password = input("Password: ")
        repassword = input("Re-Enter Password: ")
    res = hashlib.sha256(password.encode())
    password = res.hexdigest()
    with open('admindetails.txt', 'w') as f:
        f.write(username + ":" + password)
    print('Admin account Modified successfully')

def adminFn():
    while True:
        print("\n\n\n")
        print('1) Add new food item ')
        print('2) Edit food item ')
        print('3) View All food items ')
        print('4) Remove food item ')
        print('5) Business Statistics ')
        print('6) Update Admin profile')
        print("enter 0 to logout ")
        try:
            choose = int(input())
            if choose == 0:
                return
            elif choose == 1:
                addFoodItem()
            elif choose == 2:
                editfoodItem(input("enter food id: "))
            elif choose == 3:
                viewAllFoodItems()
            elif choose == 4:
                FoodItem.deleteitem(input("enter food id: "))
            elif choose == 5:
                try:
                    Order.BusinessStatistics()
                except Exception as ex:
                    print(ex.args)
            elif choose == 6:
                UpdateAdminProfile()
            else:
                print("option not valid")
            input('press enter to continue...')
        except:
            print("option not valid")
            input('press enter to continue...')
