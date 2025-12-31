import mysql.connector
import plotly.express as px
import pandas as pd

mydb = mysql.connector.connect(
    host="localhost",
    user="ECEG1user1",
    port=8889,
    password="ECEG1user1ECEG1user1",
    database="vin",
    auth_plugin='mysql_native_password'
)

'''mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM producteurs;")
myresult = mycursor.fetchall()

for x in myresult:
    print(x)'''

df = pd.read_sql_query("SELECT cru, quantite FROM recoltes join vins on (nvin=num);", mydb)
figure = px.histogram(df, x='cru', y='quantite')
figure.show()