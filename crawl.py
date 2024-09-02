import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from db import news, engine

Session = sessionmaker(bind=engine)

session = Session()

link = "https://vnexpress.net/"

request = requests.get(link)

home = BeautifulSoup(request.text, "html.parser")

list_data = []
list_data_json = []



top_story = home.find("section", class_="section section_topstory")

list_data.append(top_story.find("article", class_="item-news full-thumb article-topstory"))

for item in top_story.find("ul", class_="list-sub-feature").find_all("li"):
    list_data.append(item)

for item in home.find_all("article", class_="item-news item-news-common"):
    list_data.append(item)

for item in home.find_all("article", class_="item-news item-news-common hidden"):
    list_data.append(item)
    
for item in list_data:
    
    link = item.find("a").get("href")
    try:
        request_news = BeautifulSoup(requests.get(link).text, "html.parser")
        description = ""

        try:
            description = request_news.find("p", class_="description").text
        except:
            pass
    except:
        pass
    

    try:
        title = item.find("h3", class_="title_news").find("a").get("title")
    except:
        title = item.find("h3", class_="title-news").find("a").get("title")

    data = {
        "description": description,
        "image": item.find("div", class_= "thumb-art").find("a").get("href"),
        "title": title,
        "link": link
    }
    
    list_data_json.append(data)
    db_data = news(title = data["title"], image = data["image"], link = data["link"], description = data["description"])
    session.add(db_data)

session.commit()

# for item in home.find_all("h3", class_="title-news"):
#     list_data.append(item)

# for item in home.find_all("h3", class_="title_news"):
#     list_data.append(item)


# for item in list_data:

    # link = item.find("a").get("href")
    # request_news = BeautifulSoup(requests.get(link).text, "html.parser")
    # description = ""

    # try:
    #     description = request_news.find("p", class_="description").text
    # except:
    #     pass
   
#     data = {
#         "link": link,
#         "name": item.find("a").get("title"),
#         "image": item.find("div", class_="thumb_art").find("a").get("thumb-art"),
#         "description": description
#     }
#     # print(data)
#     # print('\n')
#     list_data_json.append(data)






