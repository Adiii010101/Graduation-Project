# #=============================================imprt libraries=======================
import http.client, urllib.parse
import json
import mysql.connector
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# https://mediastack.com/documentation
# ========================================Database connection===========================
# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="news"
)

# Create a cursor object to interact with the database
cursor = mydb.cursor()


# =======================================fetch live news==================================================
# Establish an HTTP connection to the API server
conn = http.client.HTTPConnection('api.mediastack.com')


# general - Uncategorized News
# business - Business News
# entertainment - Entertainment News
# health - Health News
# science - Science News
# sports - Sports News
# technology - Technology News

# Prepare the query parameters
params = urllib.parse.urlencode({
    'access_key': '4dcea90b841f2c2dae2c121b95e16ce8',
    'categories': '-general,-sports,-entertainment,-health,-technology',
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
# ====================================format data and store into database==============================================================================================
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
        
        # Execute the query
        cursor.execute(insert_query, insert_values)
        mydb.commit()
    
    formatted_json = json.dumps(article, indent=4)
    # print(formatted_json)
    # print("===")  # Optional separator between articles


# Pretty-print the JSON data
# formatted_json = json.dumps(json_data, indent=4)

# Print the formatted JSON
# print(formatted_json)


# ====================================find similarity of all the news====================================



# Your SELECT query
select_query = "SELECT * FROM tbl_article"

# Execute the query
cursor.execute(select_query)

# Fetch all the results
result = cursor.fetchall()

# Get the column names
columns = [column[0] for column in cursor.description]

# Create a list of dictionaries where each dictionary represents a row
finaldata = []

for row in result:
    # Convert the 'created_at' string to a datetime object
    row_dict = dict(zip(columns, row))
    row_dict['created_at'] = str(row_dict['created_at'])
    finaldata.append(row_dict)

# Print the data
# print(finaldata)

df_news = pd.DataFrame(finaldata)

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df_news['description'])

# Cosine Similarity
cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get news recommendations
def get_all_recommendations(cosine_similarities, df, top_n=5):
    all_recommendations = {}
    for _, news_row in df.iterrows():
        news_id = news_row['id']
        idx = df[df['id'] == news_id].index[0]
        sim_scores = list(enumerate(cosine_similarities[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n + 1]
        news_indices = [i[0] for i in sim_scores]
        
        # Filter out the source news id from recommendations
        recommendations = [str(df.iloc[i]['id']) for i in news_indices if df.iloc[i]['id'] != news_id]
        all_recommendations[news_id] = recommendations
    return all_recommendations

# Get recommendations for all news
all_recommendations = get_all_recommendations(cosine_similarities, df_news)

# Output in the requested format
output_data = []
for _, news_row in df_news.iterrows():
    news_id = news_row['id']
    selected_news = news_row.to_dict()
    
    # Show only the most relevant 4 ids in recommendations
    selected_news['recommendations'] = all_recommendations[news_id][:4]
    
    output_data.append(selected_news)
# Output in the requested format



# Function to convert
def listToString(s):
 
    # initialize an empty string
    str1 = ","
 
    # return string
    return (str1.join(s))
     
# =================update news database============================
output_json = json.dumps(output_data, indent=4)
for item in json.loads(output_json):
    print("-----------------")
    print(item['id'])
    print("-----------------")
    print(listToString(item['recommendations']))

    update_query = f"UPDATE tbl_article SET related_articles = %s WHERE id = %s"

    # # Execute the query
    cursor.execute(update_query, (listToString(item['recommendations']), item['id']))
    mydb.commit()
