import re
import pandas as pd


def process(data):
    pattern =  '\d{1,2}\/\d{2,4}\/\d{2,4},\s\d{1,2}:\d{1,2}\s\w{1,2}'

    #spliting messages and dates from data
    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    
    
    #Create a dataframe
    df = pd.DataFrame({"Text":messages,"Date":dates})
    

    #Convert date column to date-time format
    df["Date"] = pd.to_datetime(df["Date"],format='%d/%m/%Y, %I:%M %p')


    #Seprating usernames and messages
    Users = []
    messages = []

    for message in df['Text']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            Users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            Users.append("Group Notification")
            messages.append(entry[0])

    df['user'] = Users
    df['message'] = messages
    df.drop(columns=['Text'], inplace=True)

    #creating new columns for year/month/time
    df['only_date'] = df['Date'].dt.date
    df['year'] = df['Date'].dt.year
    df['month_num'] = df['Date'].dt.month
    df['month'] = df['Date'].dt.month_name()
    df['day'] = df['Date'].dt.day
    df['day_name'] = df['Date'].dt.day_name()
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute 

    df = df[df['user'] != 'Group Notification']

    return df
