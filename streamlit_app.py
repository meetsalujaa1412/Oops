import streamlit as st
import json
import random
import string
from pathlib import Path

st.set_page_config(page_title="Bank Management System", layout="centered")

class Bank:
    database = 'data.json'
    data = []
    
    try:
        if Path(database).exists():
            with open(database,'r') as fs:
                data = json.loads(fs.read())
        else:
            data = []
    
    except Exception as err:
        st.error(f'An exception occurred: {err}')

    @classmethod
    def _update(cls):
        with open(cls.database,'w') as fs:
            fs.write(json.dumps(cls.data))

    @staticmethod
    def _accountgenerate():
        alpha = random.choices(string.ascii_letters, k=3)
        nums = random.choices(string.digits, k=3)
        spchar = random.choices('!@#$%^&*', k=1)
        id = alpha + nums + spchar
        random.shuffle(id)
        return ''.join(id)

    @classmethod
    def create_account(cls, name, age, email, pin):
        if age < 18 or len(str(pin)) != 4:
            return False, "You are not eligible to create an account"
        
        info = {
            'name': name,
            'age': age,
            'email': email,
            'pin': pin,
            'account_number': cls._accountgenerate(),
            'balance': 0
        }
        cls.data.append(info)
        cls._update()
        return True, info

    @classmethod
    def deposit_money(cls, account_number, pin, amount):
        userdata = [i for i in cls.data if i['account_number'] == account_number and i['pin'] == pin]
        
        if not userdata:
            return False, "Invalid account number or pin"
        
        if amount > 10000 or amount < 0:
            return False, "You cannot deposit more than 10000 or less than 0"
        
        userdata[0]['balance'] += amount
        cls._update()
        return True, f"Money deposited successfully. New balance: {userdata[0]['balance']}"

    @classmethod
    def withdraw_money(cls, account_number, pin, amount):
        userdata = [i for i in cls.data if i['account_number'] == account_number and i['pin'] == pin]
        
        if not userdata:
            return False, "Invalid account number or pin"
        
        if userdata[0]['balance'] < amount:
            return False, "You do not have enough balance"
        
        userdata[0]['balance'] -= amount
        cls._update()
        return True, f"Money withdrawn successfully. Updated balance: {userdata[0]['balance']}"

    @classmethod
    def show_details(cls, account_number, pin):
        userdata = [i for i in cls.data if i['account_number'] == account_number and i['pin'] == pin]
        
        if not userdata:
            return False, "Invalid account number or pin"
        
        return True, userdata[0]

    @classmethod
    def update_email(cls, account_number, pin, new_email):
        userdata = [i for i in cls.data if i['account_number'] == account_number and i['pin'] == pin]
        
        if not userdata:
            return False, "Invalid account number or pin"
        
        userdata[0]['email'] = new_email
        cls._update()
        return True, "Email updated successfully"

    @classmethod
    def update_pin(cls, account_number, pin, new_pin):
        userdata = [i for i in cls.data if i['account_number'] == account_number and i['pin'] == pin]
        
        if not userdata:
            return False, "Invalid account number or pin"
        
        if len(str(new_pin)) != 4:
            return False, "Pin must be 4 digits"
        
        userdata[0]['pin'] = new_pin
        cls._update()
        return True, "Pin updated successfully"

    @classmethod
    def delete_account(cls, account_number, pin):
        userdata = [i for i in cls.data if i['account_number'] == account_number and i['pin'] == pin]
        
        if not userdata:
            return False, "No such user exists"
        
        index = cls.data.index(userdata[0])
        cls.data.pop(index)
        cls._update()
        return True, "Account deleted successfully"


# Streamlit UI
st.title("🏦 Bank Management System")

menu = st.sidebar.selectbox(
    "Select an option:",
    ["Home", "Create Account", "Deposit Money", "Withdraw Money", "View Details", "Update Details", "Delete Account"]
)

if menu == "Home":
    st.markdown("### Welcome to Bank Management System")
    st.write("""
    This is a simple bank management system where you can:
    - Create a new account
    - Deposit money into your account
    - Withdraw money from your account
    - View your account details
    - Update your email or PIN
    - Delete your account
    
    Select an option from the sidebar to get started!
    """)

elif menu == "Create Account":
    st.subheader("Create New Account")
    
    name = st.text_input("Enter your name:")
    age = st.number_input("Enter your age:", min_value=1, max_value=120)
    email = st.text_input("Enter your email:")
    pin = st.number_input("Enter your PIN (4 digits):", min_value=0, max_value=9999, format="%04d")
    
    if st.button("Create Account"):
        success, result = Bank.create_account(name, age, email, int(pin))
        
        if success:
            st.success("✅ Account created successfully!")
            st.json(result)
            st.info(f"📌 Please note down your account number: **{result['account_number']}**")
        else:
            st.error(f"❌ {result}")

elif menu == "Deposit Money":
    st.subheader("Deposit Money")
    
    account_number = st.text_input("Enter your account number:")
    pin = st.number_input("Enter your PIN:", min_value=0, max_value=9999, format="%04d", key="deposit_pin")
    amount = st.number_input("Enter deposit amount:", min_value=0, max_value=10000, step=100)
    
    if st.button("Deposit"):
        success, message = Bank.deposit_money(account_number, int(pin), amount)
        
        if success:
            st.success(f"✅ {message}")
        else:
            st.error(f"❌ {message}")

elif menu == "Withdraw Money":
    st.subheader("Withdraw Money")
    
    account_number = st.text_input("Enter your account number:", key="withdraw_account")
    pin = st.number_input("Enter your PIN:", min_value=0, max_value=9999, format="%04d", key="withdraw_pin")
    amount = st.number_input("Enter withdrawal amount:", min_value=0, max_value=100000, step=100, key="withdraw_amount")
    
    if st.button("Withdraw"):
        success, message = Bank.withdraw_money(account_number, int(pin), amount)
        
        if success:
            st.success(f"✅ {message}")
        else:
            st.error(f"❌ {message}")

elif menu == "View Details":
    st.subheader("View Account Details")
    
    account_number = st.text_input("Enter your account number:", key="view_account")
    pin = st.number_input("Enter your PIN:", min_value=0, max_value=9999, format="%04d", key="view_pin")
    
    if st.button("Show Details"):
        success, result = Bank.show_details(account_number, int(pin))
        
        if success:
            st.success("✅ Account Details:")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Name:** {result['name']}")
                st.write(f"**Age:** {result['age']}")
                st.write(f"**Email:** {result['email']}")
            with col2:
                st.write(f"**Account Number:** {result['account_number']}")
                st.write(f"**Balance:** ₹{result['balance']}")
        else:
            st.error(f"❌ {result}")

elif menu == "Update Details":
    st.subheader("Update Account Details")
    
    account_number = st.text_input("Enter your account number:", key="update_account")
    pin = st.number_input("Enter your PIN:", min_value=0, max_value=9999, format="%04d", key="update_pin")
    
    update_option = st.radio("What do you want to update?", ("Email", "PIN", "Both"))
    
    if update_option == "Email" or update_option == "Both":
        new_email = st.text_input("Enter your new email:")
    
    if update_option == "PIN" or update_option == "Both":
        new_pin = st.number_input("Enter your new PIN (4 digits):", min_value=0, max_value=9999, format="%04d", key="new_pin")
    
    if st.button("Update"):
        success = True
        message = ""
        
        if update_option == "Email":
            success, message = Bank.update_email(account_number, int(pin), new_email)
        elif update_option == "PIN":
            success, message = Bank.update_pin(account_number, int(pin), int(new_pin))
        else:  # Both
            success1, message1 = Bank.update_email(account_number, int(pin), new_email)
            success2, message2 = Bank.update_pin(account_number, int(pin), int(new_pin))
            success = success1 and success2
            message = message1 if success1 else message2
        
        if success:
            st.success(f"✅ {message}")
        else:
            st.error(f"❌ {message}")

elif menu == "Delete Account":
    st.subheader("Delete Account")
    
    st.warning("⚠️ This action cannot be undone!")
    
    account_number = st.text_input("Enter your account number:", key="delete_account")
    pin = st.number_input("Enter your PIN:", min_value=0, max_value=9999, format="%04d", key="delete_pin")
    
    confirm = st.checkbox("I confirm that I want to delete my account")
    
    if st.button("Delete Account", disabled=not confirm):
        success, message = Bank.delete_account(account_number, int(pin))
        
        if success:
            st.success(f"✅ {message}")
        else:
            st.error(f"❌ {message}")
