from db import mycursor
import bcrypt

def login(username, password):
    query = f"SELECT * FROM `users` WHERE `Email` = '{username}'"

    mycursor.execute(query)

    res = mycursor.fetchall()

    numberOfUsers = len(res)


    if (numberOfUsers != 1):
        return "Incorrect username or password", False
    else:
        dbPass = res[0][2]
        active = res[0][4]
        checkPass = bcrypt.checkpw(password.encode(), dbPass.encode())
        if active == "Active":
            if (checkPass):
                return "Login successful!", True
            else:
                return "Incorrect username or password", False
        else:
            return "Activate your account.", False