import admin
import models
import user
import hashlib

adminusername = None
adminpass = None
try:
    with open('admindetails.txt', 'r') as f:
        details = f.readline()
        adminusername = details.split(':')[0]
        adminpass = details.split(':')[1]
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
    adminusername = username
    adminpass = password
    with open('admindetails.txt', 'w') as f:
        f.write(username +":" + password)
    print('Admin account created successfully')


def login():
    if username == adminusername and password == adminpass:
        return True
    elif user.validateuser(username, password):
        return True
    return False

#data.ReadFiles()
models.ReadFiles()
while True:
    try:
        switch = int(input("Enter \n 1) admin or user login. \n 2) Create new user. \n enter 0 to exit the application: "))
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
                    if username == adminusername:
                        admin.adminFn()
                    else:
                        user.userfn()
                    break
            else:
                print("Log in Failed")

    except:
        print("option invalid, enter only 1 or 2")
        input('press enter to continue...')
