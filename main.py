import json
import random
import string
from pathlib import Path

class Bank:
    database = 'data.json'
    data = []
    
    try:
        if Path(database).exists():
            with open(database,'r') as fs:
                data = json.loads(fs.read())
        else:
            print('No such file exists')
    
    except Exception as err:
        print(f'an exception occurred: {err}')

    @classmethod
    def __update(cls):
        with open(cls.database,'w') as fs:
            fs.write(json.dumps(cls.data))

    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters,k = 3)
        nums = random.choices(string.digits,k = 3)
        spchar = random.choices('!@#$%^&*',k = 1)
        id = alpha + nums + spchar
        random.shuffle(id)
        return ''.join(id)

    def CreateAccount(self):
        info = {
            'name': input('Enter your name: '),
            'age': int(input('Enter your age: ')),
            'email': input('Enter your email: '),
            'pin' : int(input('Enter your pin: ')),
            'account_number': Bank.__accountgenerate(),
            'balance': 0
        }
        if info['age'] < 18 or len(str(info['pin'])) != 4:
            print('You are not eligible to create an account')
        else:
            print('Account created successfully')
            for i in info:
                print(f'{i} : {info[i]}')
            print('Please note down your account number.')
            
            Bank.data.append(info) #cls did not work here. Why?
            Bank.__update()
    
    def depositmoney(self):
        account_number = input('Enter your account number: ')
        pin = int(input('Enter your pin: '))
        
        userdata = [i for i in Bank.data if i['account_number'] == account_number and i['pin'] == pin]

        if userdata == False: 
            print('Invalid account number or pin')
        else:
            amount = int(input('How much you want to deposit: '))
            if amount > 10000 or amount < 0:
                print('You cannot deposit more than 10000 or less than 0')
            else:
                userdata[0]['balance'] += amount
                Bank.__update()
                print('Money deposited successfully')
    
    def withdrawmoney(self):
        account_number = input('Enter your account number: ')
        pin = int(input('Enter your pin: '))
        
        userdata = [i for i in Bank.data if i['account_number'] == account_number and i['pin'] == pin]
        print(userdata)
        
        if userdata == False: 
            print('Invalid account number or pin')
        else:
            amount = int(input('How much you want to wtihdraw: '))
            if userdata[0]['balance'] < amount:
                print('You do not have enough balance')
            else:
                userdata[0]['balance'] -= amount
                Bank.__update()
                print('Money withdrawn successfully')
                print(f'Updated Balance {userdata[0]["balance"]}')

    def showdetails(self):
        account_number = input('Enter your account number: ')
        pin = int(input('Enter your pin: '))
        
        userdata = [i for i in Bank.data if i['account_number'] == account_number and i['pin'] == pin]
        for i in userdata[0]:
            print(f'{i.capitalize()} : {userdata[0][i]}')
    
    def updatedetails(self):
        account_number = input('Enter your account number: ')
        pin = int(input('Enter your pin: '))
        
        userdata = [i for i in Bank.data if i['account_number'] == account_number and i['pin'] == pin]
        
        if userdata == False:
            print('Invalid account number or pin')
        else:
            question = input('What do you want to update? (email, pin): ')

            if question.lower() == 'email':
                new_email = input("Enter your new email: ").lower()
                userdata[0]['email'] = new_email
                Bank.__update()
                print('Email updated successfully')
            elif question.lower() == 'pin':
                new_pin = int(input("Enter your new pin: "))
                if len(str(new_pin)) != 4:
                    print('Pin must be 4 digits')
                else:
                    userdata[0]['pin'] = new_pin
                    Bank.__update()
                    print('Pin updated successfully')
            elif question.lower() == 'both':
                new_email = input("Enter your new email: ").lower()
                new_pin = int(input("Enter your new pin: "))
                if len(str(new_pin)) != 4:
                    print('Pin must be 4 digits')
                else:
                    userdata[0]['email'] = new_email
                    userdata[0]['pin'] = new_pin
                    Bank.__update()
                    print('Details updated successfully')
            else:
                print('Invalid input')
    

    def delete(self):
        account_number = input('Enter your account number: ')
        pin = int(input('Enter your pin: '))
        
        userdata = [i for i in Bank.data if i['account_number'] == account_number and i['pin'] == pin]
        
        if userdata == False:
            print('No such user exists')
        else:
            check = input("Press 'y' for deletion: ").lower()
            if check == 'y':
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print('Account deleted successfully')
                Bank.__update()
          

user = Bank()

print("Press 1 for creating an account: ")
print("Press 2 for deposit money in the bank: ")
print("Press 3 for withdrawing money from the bank: ")
print("Press 4 for details: ")
print("Press 5 for updating details: ")
print("Press 6 for deleting account: ")


check = int(input("Enter your reponse: "))

if check == 1:
    user.CreateAccount()

if check == 2:
    user.depositmoney()

if check ==3:
    user.withdrawmoney()

if check ==4:
    user.showdetails()

if check ==5:
    user.updatedetails()

if check ==6:
    user.delete()