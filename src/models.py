import hashlib
import json
import datetime as dt

FoodItems = []
UserDetails = []
OrderHistory = []


def ReadFiles():
    try:
        with open('FoodItems.txt', 'a+') as fptr:
            fptr.seek(0)
            lines = fptr.readlines()
            for line in lines:
                FoodItems.append(json.loads(line.replace("'", '"')))

        with open('OrderHistory.txt', 'a+') as fptr:
            fptr.seek(0)
            lines = fptr.readlines()
            for line in lines:
                OrderHistory.append(json.loads(line.replace("'", '"')))

        with open('UserDetails.txt', 'a+') as fptr:
            fptr.seek(0)
            lines = fptr.readlines()
            for line in lines:
                UserDetails.append(json.loads(line.replace("'", '"')))
    except Exception as ex:
        print(ex)


class FoodItem:
    def __init__(self, name, quantity, price, discount, stock, foodid=None, update=False):
        self.foodid = dt.datetime.now().strftime("%m%d%Y%H%M%S")
        self.name = name
        self.quantity = quantity
        self.price = price
        self.discount = discount
        self.stock = stock
        self.active = str(True)
        if update:
            delitem = None
            for item in FoodItems:
                if item["foodid"] == foodid:
                    delitem = item
                    break
            if delitem is None:
                print("Food id not valid")
                return
            FoodItems.remove(delitem)
            FoodItems.append(dict({'foodid': foodid, 'name': self.name, 'quantity': self.quantity, 'price': self.price,
                                   'discount': self.discount, 'stock': self.stock, 'active': self.active}))

            with open('FoodItems.txt', 'w') as fptr:
                for line in FoodItems:
                    fptr.write(str(line) + '\n')
        else:
            newrecord = dict({'foodid': self.foodid, 'name': self.name, 'quantity': self.quantity, 'price': self.price,
                              'discount': self.discount, 'stock': self.stock, 'active': self.active})
            FoodItems.append(newrecord)

            with open('FoodItems.txt', 'a') as fptr:
                fptr.write(str(newrecord) + '\n')

    @staticmethod
    def allfooditems():
        return FoodItems

    def deleteitem(foodid):
        deleteItem = None
        for item in FoodItems:
            if item['foodid'] == foodid:
                deleteItem = item
                break
        if deleteItem is not None:
            FoodItems.remove(deleteItem)
            deleteItem['active'] = 'False'
            FoodItems.append(deleteItem)
            with open('FoodItems.txt', 'w') as fptr:
                for line in FoodItems:
                    fptr.write(str(line) + '\n')
            print(deleteItem['name'],"deleted successfully")
        else:
            print("You have entered wrong id")

    def updatestock(seletedlist):
        itemcount = {}
        for item in seletedlist:
            if item in itemcount:
                itemcount[item] += 1
            else:
                itemcount[item] = 1

        for foodid in itemcount:
            for item in FoodItems:
                if item['foodid'] == foodid:
                    item['stock'] = int(item['stock']) - itemcount[foodid]

        with open('FoodItems.txt', 'w') as fptr:
            for line in FoodItems:
                fptr.write(str(line) + '\n')

    def food(foodid):
        for item in FoodItems:
            if item['foodid'] == foodid:
                return item
        return 'Item Not Found'

    @staticmethod
    def UpdateFoodItemFile():
        with open('FoodItems.txt', 'w') as fptr:
            for line in FoodItems:
                fptr.write(str(line) + '\n')

    def __str__(self):
        return str(dict({'foodid': self.foodid, 'name': self.name, 'quantity': self.quantity, 'price': self.price,
                         'discount': self.discount, 'stock': self.stock}))


class User:

    def __init__(self, name, mobile, email, address, password, userid=None, update=False):
        self.userid = dt.datetime.now().strftime("%m%d%Y%H%M%S")
        res = hashlib.sha256(password.encode())
        self.password = res.hexdigest()
        self.name = name
        self.mobile = mobile
        self.email = email
        self.address = address
        if update:
            delitem = None
            for item in UserDetails:
                if item["userid"] == userid:
                    delitem = item
                    break
            UserDetails.remove(delitem)
            UserDetails.append(
                dict({'userid': userid, 'username': self.name, 'phonenumber': self.mobile, 'email': self.email,
                      'address': self.address, 'password': self.password}))

            with open('UserDetails.txt', 'w') as fptr:
                for line in UserDetails:
                    fptr.write(str(line) + "\n")
        else:

            newrecord = dict(
                {'userid': self.userid, 'username': self.name, 'phonenumber': self.mobile, 'email': self.email,
                 'address': self.address, 'password': self.password})
            UserDetails.append(newrecord)

            with open('UserDetails.txt', 'a') as fptr:
                fptr.write(str(newrecord) + "\n")

    def user(userid):
        for user in UserDetails:
            if user['userid'] == userid:
                return user
        return 'User Not Found'

    @staticmethod
    def allusers():
        return UserDetails

    def __str__(self):
        return str(dict({'userid': self.userid, 'username': self.name, 'phonenumber': self.mobile, 'email': self.email,
                         'address': self.address, 'password': self.password}))


class Order:
    def __init__(self, userid, seletedorders):
        self.userid = userid
        self.seletedorders = seletedorders
        newrecord = {'userid': self.userid, 'orders': self.seletedorders, 'datetime': str(dt.datetime.now())}
        OrderHistory.append(newrecord)
        with open('OrderHistory.txt', 'a') as fptr:
            fptr.write(str(newrecord) + "\n")

    def userhistory(userid):
        noordersplaced = True
        for val in OrderHistory:
            orderedtime = None
            orderidcount = {}
            if val['userid'] == userid:
                orderedtime = val['datetime']

                for item in val['orders']:
                    if item in orderidcount:
                        orderidcount[item] += 1
                    else:
                        orderidcount[item] = 1
                        noordersplaced = False

            i = 1
            if orderedtime == None:
                continue
            print('ordered on:', orderedtime)
            for order in orderidcount:
                item = FoodItem.food(order)
                sno = str(i) + ')'
                print(sno, item['name'], 'X', orderidcount[order])
                i += 1
            print('---------------------')
        if noordersplaced:
            print('no orders placed yet')

    @staticmethod
    def UserFavoriteFood(userid):
        myorders = {}
        for order in OrderHistory:
            if order['userid'] == userid:
                for food in order['orders']:
                    if food in myorders:
                        myorders[food] += 1
                    else:
                        myorders[food] = 1
        if myorders == {}:
            print('No orders placed yet')
            return
        foodid = None
        maxc = 0
        for order in myorders:
            if myorders[order] > maxc:
                foodid = order
                maxc = myorders[order]
            elif myorders[order] == maxc:
                if not isinstance(foodid,list):
                    temp = foodid
                    foodid = []
                    foodid.append(temp)
                foodid.append(order)
        if isinstance(foodid, list):
            print('your favorite food items are :')
            i = 1
            for item in foodid:
                print("%s) %s, you ordered it %s times" %(i,FoodItem.food(item)['name'],maxc))
                i += 1
        else:
            print("your favorite food item is : %s, you have ordered it %s times" %(FoodItem.food(foodid)['name'],maxc))
    @staticmethod
    def BusinessStatistics():
        if not OrderHistory:
            print('no orders placed yet')
            return
        users = {}
        foods = {}
        for order in OrderHistory:
            if order['userid'] in users:
                users[order['userid']] += 1
            else:
                users[order['userid']] = 1

            for item in order['orders']:
                if item in foods:
                    foods[item] += 1
                else:
                    foods[item] = 1

        valueuser = None
        highsales = None
        maxu = 0
        maxs = 0

        for user in users:
            if users[user] > maxu:
                valueuser = user
                maxu = users[user]
            elif users[user] == maxu:
                if not isinstance(valueuser, list):
                    temp = valueuser
                    valueuser = []
                    valueuser.append(temp)
                valueuser.append(user)

        for food in foods:
            if foods[food] > maxs:
                highsales = food
                maxs = foods[food]

            elif foods[food] == maxs:
                if not isinstance(highsales, list):
                    temp = highsales
                    highsales = []
                    highsales.append(temp)
                highsales.append(food)
        if isinstance(highsales, list):
            print("High sale Food items are :")
            i = 1
            for item in highsales:
                print(str(i) + ') ' + FoodItem.food(item)['name'] + ", number of times ordered = " + str(maxs))
                i += 1
        else:
            print("High sale Food item :",
                  FoodItem.food(highsales)['name'] + ", No of times ordered = " + str(maxs))

        if isinstance(valueuser, list):
            i = 1
            for user in valueuser:
                print(str(i) + ') ' + User.user(user)['username']+', No of orders placed = ' + str(maxu))
                i += 1
        else:
            print('value customer name:', User.user(valueuser)['username']+', No of orders placed = ' + str(maxu))
        print('---------------------------------')
