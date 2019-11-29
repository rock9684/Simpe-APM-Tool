import mysql.connector
import json
from app import webapp, bcrypt
from app import webapp, resources,bcrypt

host='localhost'
user_d='root'
password_d='Secure@123'

def create_database(database):
  conn = mysql.connector.connect(host=host,
                                 user=user_d,
                                 password=password_d)
  command = "Create Database %s" % database
  if conn.is_connected():
    print('Connected to MySQL database')
    cursor = conn.cursor()
    cursor.execute(command)
    conn.commit()
    conn.close()
  else:
    print('Error: Failed to Create a Database')

def view_all_account():
  conn = mysql.connector.connect(host=host,
                                 user=user_d,
                                 password=password_d)

  if conn.is_connected():
    print('Connected to MySQL database')
    cursor = conn.cursor()
    command = "SELECT name FROM sys.databases"

    cursor.execute(command)

    row = cursor.fetchall()
    print(row)


def create_table(database,table_name,column_list):
  conn = mysql.connector.connect(host=host,
                                 database=database,
                                 user=user_d,
                                 password=password_d)

  if conn.is_connected():

    print('Connected to MySQL database')
    command = "CREATE TABLE %s (" % table_name
    for column in column_list:
      command += "%s %s NOT NULL," % (column["name"],column["type"])
    command = command + " PRIMARY KEY (%s));"% (column_list[0])["name"]
    
    cursor = conn.cursor()
    
    cursor.execute(command)
    conn.commit()
    conn.close()
  else:
    print('Error: Failed to Create Table')

def create_account_table():
  column_list=[{"name":'AccountName',
                "type": 'varchar(255)'}
    ]
  #create_database('APM_Database')
  create_table('APM_Database','Accounts',column_list)
  

  
def add_accounts(account_name):
  conn = mysql.connector.connect(host=host,
                                 database='APM_Database',
                                 user=user_d,
                                 password=password_d)
  if conn.is_connected():

    print('Connected to MySQL database')
    command = "INSERT INTO Accounts(AccountName) " \
              "VALUES(\'%s\')" % account_name
    args=(account_name)
    print(command)
    cursor = conn.cursor()
    
    cursor.execute(command)
    conn.commit()
    print("Done")

    conn.close()
    return 1
    
  else:
    print('Error: Failed to Add Account')
    return 0


  
#add_accounts('Doors','charizard')
def view_accounts(account=None):
  if account!=None:
    conn = mysql.connector.connect(host=host,
                                   database='APM_Database',
                                   user=user_d,
                                   password=password_d)

    if conn.is_connected():
      print('Connected to MySQL database')
      cursor = conn.cursor()
      command="SELECT * FROM Accounts WHERE AccountName = \"%s\";" % account
      
      cursor.execute(command)

      rows = cursor.fetchall()
      row_list=[]
      for row in rows:
        row_list.append(row[0])
        
      print(row_list)
      return(row_list)
  else:
    
    conn = mysql.connector.connect(host=host,
                                   database='APM_Database',
                                   user=user_d,
                                   password=password_d)

    if conn.is_connected():
      print('Connected to MySQL database')
      cursor = conn.cursor()
      command="SELECT * FROM Accounts;"
      
      cursor.execute(command)

      rows = cursor.fetchall()
      row_list=[]
      for row in rows:
        row_list.append(row[0])
        
      print(row_list)
      return(row_list)

def verify_account(account):
  a=view_accounts(account)
  if len(a)>0:
    return 0
  else:
    return 1

def insert_user_database(username,password):
  conn = mysql.connector.connect(host=host,
                                 database='users',
                                 user=user_d,
                                 password=password_d)
  if conn.is_connected():

    print('Connected to MySQL database')
    command = "INSERT INTO user_list(username,password) " \
              "VALUES(%s,%s)"
    args=(username,password)
    cursor = conn.cursor()
    try:
      cursor.execute(command, args)
      conn.commit()
      conn.close()
      return 1
    except:
      return 0
  else:
    print('Error: Failed to Add the User')
    return 0



    
        

def add_user_account(account,username,password,access_level):
  conn = mysql.connector.connect(host=host,
                                 database=account,
                                 user=user_d,
                                 password=password_d)
  if conn.is_connected():

    print('Connected to MySQL database')
    command = "INSERT INTO user_list(username,password,access_level) " \
              "VALUES(%s,%s,%s)"
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    args=(username,hashed_password,access_level)
    cursor = conn.cursor()
    try:
      cursor.execute(command, args)
      conn.commit()
      conn.close()
      return 1
    except:
      return 0
  else:
    print('Error: Failed to Add the User')
    return 0

def new_account_created(account,password):
  hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
  add_accounts(account)
  create_database(account)
  column_list = [{"name": 'username',
                  "type": 'varchar(255)'},
                 {"name": 'password',
                  "type": 'varchar(255)'},
                 {"name": 'access_level',
                  "type": 'varchar(255)'}
                 ]
  create_table(account,'user_list', column_list)
  add_user_account(account, 'root', password, '3')





  ################Old Code

def insert_image_database(imagename,username):
  conn = mysql.connector.connect(host=host,
                                 database='users',
                                 user=user_d,
                                 password=password_d)
  if conn.is_connected():

    print('Connected to MySQL database')
    command = "INSERT INTO image_list(imagename,username) " \
              "VALUES(%s,%s)"
    args=(imagename,username)
    cursor = conn.cursor()
    try:
      cursor.execute(command, args)
      conn.commit()
      conn.close()
      return 1
    except:
      return 0

  else:
    print('Error: Failed to Add Image')
    return 0

def verify_username_password(account,username,password):
  conn = mysql.connector.connect(host=host,
                                 database=account,
                                 user=user_d,
                                 password=password_d)

  if conn.is_connected():
    print('Connected to MySQL database')
    cursor = conn.cursor()
    command="SELECT * FROM user_list WHERE username = \"%s\";" % username
    
    cursor.execute(command)

    row = cursor.fetchone()
    access_level = int(row[2])
    
    conn.close()
    if row!=None:
      if bcrypt.check_password_hash(row[1], password):
        return (1,access_level)
      else:
        print('Error: Authentication Failed')
        return (0,access_level)
    else:
      print('Error: Authentication Failed')
      return (-1,access_level)

def get_image_list(username):
  conn = mysql.connector.connect(host=host,
                                 database='users',
                                 user=user_d,
                                 password=password_d)

  if conn.is_connected():
    print('Connected to MySQL database')
    cursor = conn.cursor()
    command="SELECT imagename FROM image_list WHERE username = \"%s\";" % username

    cursor.execute(command)

    row = cursor.fetchall()
    file_list=[]

    conn.close()
    if row!=None:
      for i in row:
        file_list.append(i[0])
      return file_list
    
    else:
      return file_list



