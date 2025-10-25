import streamlit as st
import uuid6
import pandas as pd 
from datetime import datetime
import sqlite3
from sqlite3 import Error

 # Generating ID Automatically
def generate_id():
    id=None
    try:
        id=str(uuid6.uuid6()) 
        
    except Error as e:
        print(f'the error {e} occured' )
    return id
# creating database
def create_database(path):
    connection= None
    try:
        connection=sqlite3.connect(path)
        print('creation of database succesfull')
    except Exception as e:
        print(f'the error {e} occured')
    
    return connection

# connection to database 
connection=create_database('employee.db')

def execute_query(connection,query,data=None):
    cursor=connection.cursor()
    try:
        if data:
            cursor=cursor.execute(query,data)
        else:
            cursor=cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f'the error {e} occured')
    return cursor

#Create table 
create_staff_queary_table='''
CREATE TABLE IF NOT EXISTS staff(
staff_id VARCHAR(32) PRIMARY KEY ,
name VARCHAR(40) NOT NULL,
age INTEGER,
marital_status VARCHAR(7),
department VARCHAR(40),
created_at DATETIME
);
'''
#TEXT means a text string of any length.
#VARCHAR(255) means a text string with up to 255 characters, 
# but SQLite does not actually enforce the length (unlike MySQL or PostgreSQL).
#  It will still store longer strings.

cursor=execute_query(connection,create_staff_queary_table)
print('staff table created successfully')
print(cursor.executemany)
st.title('staff query form ') 
# 1. label

# The label is the text that shows up above (or beside) the input box.

# It tells the user what kind of data to enter.

# In your case, "Name" is the label, so users know this field is for typing their name.

# Example:

# Name
# [___________]

# 2. placeholder

# The placeholder is the faint (gray, usually) text that appears inside the input box before the user types anything.

# It gives an example or hint of what the input should look like.

# In this case, "Ali Ahmad" is the placeholder, suggesting that the expected input is a full name.

with st.form('STAFF INQUIRY FORM',clear_on_submit=True):
    is_form_data=False
    name=st.text_input(label='NAME',placeholder='surname firstname')
    age=st.number_input(label='AGE')
    marital_status=st.selectbox(label='MARITAL STATUS', options=('married' , 'unmarried'))
    department=st.selectbox(label='DEPARTMENT',options=('marketing','accounting','cybersecurity'))

    if (name and department and age>0 and marital_status):
        is_form_data=True

    submit=st.form_submit_button('submit')
    if submit and is_form_data:
        staff_id=generate_id()
        date_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
        staff_data_insertion='''
        INSERT INTO staff(staff_id,name,age,marital_status,department,created_at)
        VALUES(?,?,?,?,?,?);
        '''
        cursor=execute_query(connection,staff_data_insertion,data=(staff_id,name,age,marital_status,department,date_time))
        print(cursor.lastrowid)
        #cursor.lastrowid gives you the row ID of the last inserted record.
        # This is useful if you want to confirm the insertion or use the ID later.
        st.success('staff profile created successfully')
        st.balloons()
st.title('Staff list')
st.dataframe(pd.read_sql_query('SELECT * FROM staff',connection))