import re
import pandas as pd

def preprocess(data):
    pattern = r"(\d{2}/\d{2}/\d{4}), (\d{1,2}:\d{2}\s*[ap]m) - ([^:]+): (.*)"
    messages = re.split(pattern, data)[1:]
    user_messages = []
    message_dates = []
    user_names = []

    for i in range(0, len(messages), 5):
        message_date = messages[i]
        message_time = messages[i + 1]
        user_name = messages[i + 2]
        user_message = messages[i + 3]

        user_names.append(user_name)
        user_messages.append(user_message)
        message_dates.append(message_date + ', ' + message_time)

    df = pd.DataFrame({'user': user_names, 'message': user_messages, 'date': message_dates})

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %I:%M\u202f%p')
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []

    for hour in df[['day', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df