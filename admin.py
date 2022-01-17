from models import FoodItem,Order

def addFoodItem():
    name = input("Name: ")
    quantity = input("Quantity: ")
    price = input("Price: ")
    discount = input("Discount(%): ")
    stock = input("Stock: ")
    adminuser = FoodItem(name,quantity,price,discount,stock)

def editfoodItem(foodid):
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
        adminuser = FoodItem(name,quantity,price,discount,stock,foodid,True)
        print('item updated successfully')

def viewAllFoodItems():
    for item in FoodItem.allfooditems():
        if item['active'] == 'True':
            for key in item:
              print(key,":",item[key])
            print('.................................')


def adminFn():
    while True:
        print("\n\n\n")
        print('1) Add new food item ')
        print('2) Edit food item ')
        print('3) View All food items ')
        print('4) Remove food item ')
        print('5) Business Statistics ')
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
            else:
                print("option not valid")
            input('press enter to continue...')
        except:
            print("option not valid")
            input('press enter to continue...')

