balance=5000
password ="1234"

def atm():
    global balance
    right_of_entry=3

    while right_of_entry > 0:
        enter_password=input("Enter the password")

        if enter_password ==password:
            while True:
                print("1.Balance inquiry")
                print("2.Deposit")
                print("3.Withdraw money")
                print("4.Exit")

                amount=input("What would you like to do")

                if amount=="1":
                    print(f"New Balance:{balance}")

                elif amount=="2":
                    amount =float(input("Enter the Amount you want to deposit"))
                    if amount >0:
                        balance=balance+amount
                        print(f"New Balance: {balance}")
                    else:
                        print("Invalid amount")
                elif amount=="3":
                    amount=float(input("Enter the amount you want to withdraw"))
                    if 0 <amount<balance:
                        balance=balance-amount
                        print(f"New Balance: {balance}")
                    else:
                        print("Invalid amount")
                elif amount=="4":
                    print("Signing out")
                    return
                else:
                    print("Invalid amount")
        else:
            right_of_entry-=1

        if right_of_entry==0:
            print("Your account has been blocked:")
atm()