from flask import Flask, request
# import http.client, urllib.parse
import json
from flask import jsonify
import mysql.connector
from datetime import datetime
from flask_cors import CORS

# Enable CORS for all routes


# Create a Flask web application instance
app = Flask(__name__)
CORS(app)
# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="news"
)

# Create a cursor object to interact with the database
cursor = mydb.cursor()

def fetch_extra_data(table, column, id_name, id_value):
    # Assuming 'con' is the established MySQL connection
    cursor = mydb.cursor(dictionary=True)
    sql = f"SELECT * FROM {table} WHERE {id_name} = {id_value}"
    cursor.execute(sql)
    row = cursor.fetchone()

    try:
        if row and len(row[column]) != 0:
            return row[column].upper()
        else:
            return 0
    except:
        return 0

# Route for the home page
@app.route('/viewAllNews')
def viewAllNews():
    # Define the SELECT query
    select_query = "SELECT * FROM tbl_article order by `id` desc"

    # Execute the query
    cursor.execute(select_query)

    # Fetch all rows
    result = cursor.fetchall()
    # Convert the result to a list of dictionaries
    # Get column names from cursor description
    columns = [column[0] for column in cursor.description]
    finaldata = []
  

    # Create a list of dictionaries where each dictionary represents a row
    data = [dict(zip(columns, row)) for row in result]
    # for dats in data:
        # char_array =dats['related_articles'].split(",")
        # my_list = []
        # for ra in char_array:
        #     my_sub_list = {}
        #     my_sub_list['id']=ra
        #     my_sub_list['title']=fetch_extra_data('tbl_article', 'title', 'id', ra)
        #     my_sub_list['image']=fetch_extra_data('tbl_article', 'image', 'id', ra)
        #     my_sub_list['views']=fetch_extra_data('tbl_article', 'views', 'id', ra)
        #     my_list.append(my_sub_list)
        # dats['related_articles']= my_list
        # finaldata.append(dats)

    # Convert the list of dictionaries to JSON format
    # json_data = json.dumps(data, indent=4)

    # Print the JSON data
    # print(json_data)

    # Close the cursor and the connection
    # cursor.close()
    # mydb.close()
    data={"error":False,"message":"viewAllNews","available_news":data}
    # data={'data':data}
    return jsonify(data)

# ===================================view single news===========================
# Route for the home page
@app.route('/viewSingleNews/<id>')
def viewSingleNews(id):
    # Define the SELECT query
    select_query = f"SELECT * FROM tbl_article WHERE id={id}"

    # Execute the query
    cursor.execute(select_query)

    # Fetch all rows
    result = cursor.fetchall()
    # Convert the result to a list of dictionaries
    # Get column names from cursor description
    columns = [column[0] for column in cursor.description]
    finaldata = []
  

    # Create a list of dictionaries where each dictionary represents a row
    data = [dict(zip(columns, row)) for row in result]
    for dats in data:
        views=dats['views']
        # views=1

        char_array =dats['related_articles'].split(",")
        my_list = []
        for ra in char_array:
            my_sub_list = {}
            my_sub_list['id']=ra
            my_sub_list['title']=fetch_extra_data('tbl_article', 'title', 'id', ra)
            my_sub_list['image']=fetch_extra_data('tbl_article', 'image', 'id', ra)
            my_sub_list['views']=fetch_extra_data('tbl_article', 'views', 'id', ra)
            my_list.append(my_sub_list)
        dats['related_articles']= my_list
        finaldata.append(dats)
        
    views=int(views)+1
    update_query = f"UPDATE tbl_article SET views = %s WHERE id = %s"

    # # Execute the query
    cursor.execute(update_query, (views, id))

    # # Commit the changes
    mydb.commit()
    # Convert the list of dictionaries to JSON format
    # json_data = json.dumps(data, indent=4)

    # Print the JSON data
    # print(json_data)

    # Close the cursor and the connection

    # cursor.close()
    # mydb.close()
    data={"error":False,"message":"viewSingleNews","available_news":finaldata}
    # data={'data':data}
    return jsonify(data)


# ===================================newsOperations===========================
# Route for the home page
@app.route('/newsOperations', methods=['POST'])
def newsOperations():
# Route for the hello page
    id = request.form.get('id')
    action = request.form.get('action')

    select_query = f"SELECT * FROM tbl_article WHERE id={id}"

    # Execute the query
    cursor.execute(select_query)

    result = cursor.fetchall()
    # Convert the result to a list of dictionaries
    # Get column names from cursor description
    columns = [column[0] for column in cursor.description]
    finaldata = []
  

    # Create a list of dictionaries where each dictionary represents a row
    data = [dict(zip(columns, row)) for row in result]
    for dats in data:
        likes=int(dats['likes'])
        dislikes=int(dats['dislikes'])
    # return jsonify(single_column_values['likes'])
    
    

    if(action=='like'):
        likes=int(likes)+1
        update_query = f"UPDATE tbl_article SET likes = %s WHERE id = %s"
        cursor.execute(update_query, (likes, id))
    else:
        dislikes=int(dislikes)+1
        update_query = f"UPDATE tbl_article SET dislikes = %s WHERE id = %s"
        cursor.execute(update_query, (dislikes, id))
    # # Commit the changes
    mydb.commit()
    data={"error":False,"message":"viewSingleNews", "likes": likes , "dislikes": dislikes}
    # return "test"
    return jsonify(data)

# ===================================searchNews===========================
# Route for the home page
@app.route('/searchNews/<keyword>')
def searchNews(keyword):
    # Define the SELECT query
    select_query = f"SELECT * FROM tbl_article WHERE description LIKE '%{keyword}%' OR title LIKE '%{keyword}%'"

    # Execute the query
    cursor.execute(select_query)

    # Fetch all rows
    result = cursor.fetchall()
    # Convert the result to a list of dictionaries
    # Get column names from cursor description
    columns = [column[0] for column in cursor.description]
    finaldata = []
  

    # Create a list of dictionaries where each dictionary represents a row
    data = [dict(zip(columns, row)) for row in result]
    if(len(data)>0):
        data_length=len(data)
    else:
        data_length=0
        data="Not found! Search diffrent keywords"

    # cursor.close()
    # mydb.close()
    data={"error":False,"message":"searchNews","available_news":data,"count":data_length}
    # data={'data':data}
    return jsonify(data)

# ===================================searchNews===========================
# Route for the home page
@app.route('/popularPosts')
def popularPosts():
    # Define the SELECT query
    select_query = f"SELECT * FROM `tbl_article` ORDER BY views DESC LIMIT 5"

    # Execute the query
    cursor.execute(select_query)

    # Fetch all rows
    result = cursor.fetchall()
    # Convert the result to a list of dictionaries
    # Get column names from cursor description
    columns = [column[0] for column in cursor.description]
    finaldata = []
  

    # Create a list of dictionaries where each dictionary represents a row
    data = [dict(zip(columns, row)) for row in result]


    # cursor.close()
    # mydb.close()
    data={"error":False,"message":"popularPosts","available_news":data}
    # data={'data':data}
    return jsonify(data)



@app.route('/hello')
def hello():
    return 'Hello, Flask World!'

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
