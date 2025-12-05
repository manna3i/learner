# Solution for Problem 01 — untitled problem

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]



while True:    
    Startday = input("Enter the starting day of the week (e.g., Monday): ")
    if Startday in days:
       break
    else:
         print("Invalid day. Please try again.")

start_index = days.index(Startday)

       
while True:    
    try:
        num_days = int(input("Enter the number of days to add (non-negative integer): "))
        if num_days >= 0:
            break
        else:
            print("Please enter a non-negative integer.")
    except ValueError:
        print("Invalid input. Please enter a non-negative integer.")

end_index = (start_index + num_days)%7
Endday = days[end_index]
print(f"The day after adding {num_days} days to {Startday} is {Endday}.")