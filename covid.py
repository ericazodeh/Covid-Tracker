
import mysql.connector
import requests
import json
import urllib.parse
from datetime import datetime


#connect to mySQL database
db = mysql.connector.connect(host='###############', user='admin',
                            password='###############')
cursor = db.cursor()

#use the created schema and commit execution
cursor.execute("use newSchema;")
db.commit()

#allow a continuous loop of SQL and JSON queries
while(True):
    print("===COVID API Query===")
    #ask user for a state abbreviation
    state = str(input("Enter the state abbreviation for which the COVID data should be retrieved:"))

    #ask user for a date
    #restart program if user gives an invald date
    try:
        date = int(input('Enter the date for which the COVID data should be retrieved e.g. ( 20201219 ) : '))
    except:
       print("Error: input a valid date")
       continue


    #format url to eventually pasrse JSON
    url = 'https://api.covidtracking.com/v1/states/{}/daily.json?'.format(state)

    positiveCases = 0
    deaths = 0

    #encode JSON from url
    url1 = url + urllib.parse.urlencode({'date' : date})

    #convert JSON response to a string
    response = requests.get(url1).text

    #if an error occurs, then there was an incorrect state given by the user
    if response.find("\"error\": true,") == True:
        print("Error: please type in a correct state (i.e. TX).")
        continue

    #convert string into a list through json.loads()
    data = json.loads(response)

    #loop through each through element (day) in the list, looking for
    #the date given by the user
    #then update the positive cases and death variables
    for day in data:
        if day['date'] == date:
            positiveCases = day['positiveIncrease']
            deaths = day['deathIncrease']

    #convert date to datetime format for SQL execution
    #make sure that the user gave a valid date
    dateAsString = str(date)
    try:
        date = datetime(year=int(dateAsString[0:4]), month=int(dateAsString[4:6]), day=int(dateAsString[6:8]))
    except:
        print("Error: input a valid date")
        continue





    #create the correct string for query execution
    string = "insert into data(state,date,positiveIncrease,deathIncrease) values (" +'\''+ state +'\''+", "+'\''+ str(date)+'\'' + ", "+'\''+ str(positiveCases)+'\'' + ", "+'\''+ str(deaths)+'\'' +");"
    #execute and commit query
    cursor.execute(string)
    db.commit()

    #also output results to the console
    print("state: " + state)
    print("date: " + str(date))
    print("Positive cases: " + str(positiveCases))
    print("Death: " + str(deaths))




