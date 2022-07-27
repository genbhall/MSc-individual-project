from datetime import datetime

# variables to do with the file looked at
filename = "../preprocessing/processed_data/hh101/hh101_preprocessed_60sw.csv"
data_name = 'hh101'
interval = 60
start_date = datetime(2012,7,20,0,0,0)
all_activities = [
    'Time', 
    'Step_Out', 
    'Other_Activity',
    'Toilet', 
    'Phone', 
    'Personal_Hygiene', 
    'Leave_Home', 
    'Enter_Home', 
    'Relax', 
    'Sleep_Out_Of_Bed', 
    'Drink', 
    'Watch_TV', 
    'Dress', 
    'Evening_Meds', 
    'Wake_Up', 
    'Read', 
    'Morning_Meds', 
    'Cook_Breakfast', 
    'Eat_Breakfast', 
    'Bathe', 
    'Cook_Lunch', 
    'Eat_Lunch', 
    'Wash_Lunch_Dishes', 
    'Go_To_Sleep', 
    'Sleep', 
    'Bed_Toilet_Transition', 
    'Wash_Breakfast_Dishes', 
    'Work_At_Table', 
    'Groom', 
    'Cook', 
    'Eat', 
    'Cook_Dinner', 
    'Eat_Dinner', 
    'Wash_Dinner_Dishes', 
    'Wash_Dishes', 
    'Entertain_Guests',
]