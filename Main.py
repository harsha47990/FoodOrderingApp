import admin
import models
import user
import hashlib

adminlogin = False

try:
    with open('admindetails.txt', 'r') as f:
        details = f.readline()
except:
    print("Welcome, Please create admin account")
    username = input("enter username: ")
    password = input("enter password: ")
    repassword = input("Re-Enter Password: ")
    while repassword != password:
        print("Password Doesnt Match")
        password = input("Password: ")
        repassword = input("Re-Enter Password: ")
    res = hashlib.sha256(password.encode())
    password = res.hexdigest()

    with open('admindetails.txt', 'w') as f:
        f.write(username + ":" + password)
    print('Admin account created successfully')



def login():
    if admin.adminlogincheck(username, password):
        global adminlogin
        adminlogin = True
        return True
    elif user.validateuser(username, password):
        adminlogin = False
        return True
    return False


# data.ReadFiles()
models.ReadFiles()
while True:
    try:
        switch = int(
            input("Enter \n 1) admin or user login. \n 2) Create new user. \n enter 0 to exit the application: "))
        if switch not in [0, 1, 2]:
            raise "wrong details entered"
        if switch == 0:
            break
        elif switch == 2:
            user.createuser()
        elif switch == 1:
            username = input("Enter UserName: ")
            res = hashlib.sha256(input("Enter Password: ").encode())
            password = res.hexdigest()
            if login():
                while True:
                    print("Login Successful")
                    try:
                        if adminlogin:
                            admin.adminFn()
                        else:
                            user.userfn()
                        break
                    except Exception as ex:
                        print(ex.args)
            else:
                print("Log in Failed")

    except:
        print("option invalid, enter only 1 or 2")
        input('press enter to continue...')
