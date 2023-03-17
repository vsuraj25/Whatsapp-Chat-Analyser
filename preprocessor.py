import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AaPp][Mm]\s-\s'
    messages = re.split(pattern,data)[1:]
    messages = [i.strip() for i in messages]
    dates = re.findall(pattern, data)
    dates = [i.split(' -')[0] for i in dates]
    dates = [i.replace(',', '') for i in dates]

    df = pd.DataFrame({'message_date': dates,'user_message': messages})
    df['message_date'] = pd.to_datetime(df['message_date'],dayfirst=True)

    users = []
    sep_messages = []
    for msg in df['user_message']:
        entries = re.split('([\w\W]+?):\s', msg)
        if entries[1:]:
            users.append(entries[1])
            sep_messages.append(entries[2])
        else:
            users.append('group_nortification')
            sep_messages.append(entries[0])
    df['user'] = users
    df['message'] = sep_messages
    df.drop(columns=['user_message'], inplace = True)
            
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['month_num'] = df['message_date'].dt.month
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute
    df['only_date'] = df['message_date'].dt.date
    df['day_name'] = df['message_date'].dt.day_name()

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + '00')
        elif hour == 00:
            period.append('00' + '-' + str(hour+1))
        else:
            period.append(str(hour) + '-' + str(hour+1))
    df['period'] = period

    df = df[df['user'] != 'group_nortification']

    return df