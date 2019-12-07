import pandas as pd

# script to clean TweetDataCleaned for Non-ASCII characters and empty fields
df = pd.read_csv('TweetDataCleaned.csv')
df2 = df.dropna(axis=0, subset=["Date", "Tweet_Text", "Source", "User_ID", "Lat", "Lng"])
df3 = df2[~df2['Tweet_Text'].str.contains(r'[^\x00-\x7F]+')]
df4 = df3[~df3['Source'].str.contains(r'[^\x00-\x7F]+')]
new_df = df4.to_csv('TweetDataCleanedNew.csv', index=False)

# script to clean UserDataCleaned for Non-ASCII characters and empty fields
df = pd.read_csv('UserDataCleaned.csv')
df2 = df.dropna(axis=0, subset=["ID", "Name", "Screen_Name", "User_Location"])
df3 = df2[~df2['Name'].str.contains(r'[^\x00-\x7F]+')]
df4 = df3[~df3['User_Location'].str.contains(r'[^\x00-\x7F]+')]
new_df = df4.to_csv('UserDataCleanedNew.csv', index=False)

# script to clean event_clean_cat.csv
keep_cols= ["event_id", "start_time", "city", "state", "country", "lat", "lng"]
new_df = df[keep_cols]
n_df = new_df.dropna(axis=0, subset=['event_id', 'start_time', 'city', 'state', 'country'])
n_df.to_csv("events_clean.csv", index=False)

df2 = pd.read_csv('users.csv')
new_df2 = df2.dropna(axis=0, subset=['user_id', 'locale', 'birthyear', 'gender', 'joinedAt', 'location', 'timezone'])
new_df2.to_csv("users_clean.csv", index=False)
