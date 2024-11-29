import http.client, urllib.parse
import json
import mysql.connector


# https://mediastack.com/documentation

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="news"
)

# Create a cursor object to interact with the database
cursor = mydb.cursor()

# Establish an HTTP connection to the API server
conn = http.client.HTTPConnection('api.mediastack.com')

# Prepare the query parameters
params = urllib.parse.urlencode({
    'access_key': '4dcea90b841f2c2dae2c121b95e16ce8',
    'categories': '-general,-sports',
    'sort': 'published_desc',
    'limit': 100,
    'country':'in',
})

# Send a GET request to the API endpoint with the prepared parameters
conn.request('GET', '/v1/news?{}'.format(params))

# Get the API response
res = conn.getresponse()
data = res.read()

# Decode the response data as UTF-8
data_str = data.decode('utf-8')

# Parse the JSON data
json_data = json.loads(data_str)

articles_list = json_data['data']
# print(articles_list)
# Iterate over each article and print as formatted JSON
for article in articles_list:
    title = article['title']
    source = article['source']
    author = article['author']
    publishedAt = article['published_at']
    description = article['description']
    url = article['url']
    urlToImage = article['image']
    # content = article['content']
    category=article['category']
        # SQL query for inserting an article if image is not null
    if article.get('image') is not None:
        insert_query = "INSERT INTO `tbl_article`( `title`, `image`, `description`, `likes`, `dislikes`, `created_at`, `related_articles`, `source`, `author`, `category`, `url`) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert_values = (title, urlToImage, description,1,1,publishedAt,'1,2,4,5',source,author,category,url)
        # print(insert_query)
        # Execute the query
        cursor.execute(insert_query, insert_values)
        mydb.commit()
    
    formatted_json = json.dumps(article, indent=4)
    print(formatted_json)
    print("===")  # Optional separator between articles
# Pretty-print the JSON data
# formatted_json = json.dumps(json_data, indent=4)

# Print the formatted JSON
# print(formatted_json)
