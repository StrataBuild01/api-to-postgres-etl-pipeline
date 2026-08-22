import requests
import pandas as pd

#Where to get the data from
url = "https://jsonplaceholder.typicode.com/users"

#Extract the API data
response = requests.get(url)
data = response.json()
print(response.status_code)

#Transform the API data and get only the fields we need

users = []

for user in data:
    user_data = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "city": user["address"]["city"]
    }
    users.append(user_data)


#Convert the transformed data into a Pandas DataFrame
df = pd.DataFrame(users)
print(df)

# Save the DataFrame as a CSV file
df.to_csv("users.csv", index=False)





    #print(user["name"], "|", user["email"], "|", user["address"]["city"])
    