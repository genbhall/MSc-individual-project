from datetime import datetime

# hh101 variables
# filename = "../CASAS_dataset/hh101/hh101.ann.features.csv"
# filename_proc = "processed_data/hh101/hh101_preprocessed_60sw.csv"
# data_name = 'hh101'
# interval = 60
# start_date = datetime(2012,7,20,0,0,0)
# end_date = datetime(2012,9,17,0,0,0)
# all_activities = [
#     'timestamp', 
#     'Step_Out', 
#     'Other_Activity',
#     'Toilet', 
#     'Phone', 
#     'Personal_Hygiene', 
#     'Leave_Home', 
#     'Enter_Home', 
#     'Relax', 
#     'Sleep_Out_Of_Bed', 
#     'Drink', 
#     'Watch_TV', 
#     'Dress', 
#     'Evening_Meds', 
#     'Wake_Up', 
#     'Read', 
#     'Morning_Meds', 
#     'Cook_Breakfast', 
#     'Eat_Breakfast', 
#     'Bathe', 
#     'Cook_Lunch', 
#     'Eat_Lunch', 
#     'Wash_Lunch_Dishes', 
#     'Go_To_Sleep', 
#     'Sleep', 
#     'Bed_Toilet_Transition', 
#     'Wash_Breakfast_Dishes', 
#     'Work_At_Table', 
#     'Groom', 
#     'Cook', 
#     'Eat', 
#     'Cook_Dinner', 
#     'Eat_Dinner', 
#     'Wash_Dinner_Dishes', 
#     'Wash_Dishes', 
#     'Entertain_Guests',
# ]
# sleep_activities = [
#     'timestamp',
#     'Date', 
#     'Sleep', 
# ]

# hh120 variables
filename = "../CASAS_dataset/hh120/hh120.ann.features.csv"
filename_proc = "processed_data/hh120/hh120_preprocessed_60sw.csv"
data_name = 'hh120'
interval = 60
start_date = datetime(2012,1,28,0,0,0)
end_date = datetime(2012,3,31,0,0,0)
all_activities = [
    'Sleep',
    'Other_Activity',
    'Bed_Toilet_Transition',
    'Toilet',
    'Relax',
    'Dress',
    'Personal_Hygiene',
    'Morning_Meds',
    'Wash_Dishes',
    'Leave_Home',
    'Enter_Home',
    'Watch_TV',
    'Entertain_Guests',
    'Work_On_Computer',
    'Work_At_Table',
    'Cook',
    'Eat',
    'Take_Medicine',
    'Drink',
    'Bathe',
    'Step_Out',
    'Evening_Meds',
    'Read',
    'Cook_Breakfast',
    'Eat_Breakfast',
    'Groom',
    'Cook_Lunch',
    'Eat_Lunch',
    'Wash_Lunch_Dishes',
    'Sleep_Out_Of_Bed',
    'Cook_Dinner',
    'Eat_Dinner',
    'Wash_Dinner_Dishes',
    'Phone',
    'Wash_Breakfast_Dishes'
]

sleep_activities = [
    'timestamp',
    'Date', 
    'Sleep', 
]