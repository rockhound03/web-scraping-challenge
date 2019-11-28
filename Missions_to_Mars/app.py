# import necessary libraries
from flask import Flask, render_template, redirect
from flask_table import Table, Col
#import django_tables2 as tables
import pymongo
import time
# create instance of Flask app
app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db

# Drops collection if available to remove duplicates
db.mars.drop()


# create route that renders index.html template
@app.route("/")
def echo():
    all_mars_data = list(db.mars.find())
    #print(all_mars_data('news_p'))
    try:
        mars_weather = all_mars_data[0]['mars_weather']
        news_para = all_mars_data[0]['news_p']
        news_title_txt = all_mars_data[0]['news_title']
        mars_feat_pic = all_mars_data[0]['featured_image_url']
        mars_facts = all_mars_data[0]['mars_facts']
        mars_hemis = all_mars_data[0]['hemisphere_image_urls']
    
    except Exception as e:
        mars_weather = str(e)
        news_para = "Nothing yet."
        news_title_txt = "No News is good news."
        mars_feat_pic = "placeholder"
        mars_facts = "Nothing to see here."
        mars_hemis = [{"title" : "pic_names[0]", "img_url" : "ref_list[0]"},
                            {"title" : "pic_names[1]", "img_url" : "ref_list[1]"},
                            {"title" : "pic_names[2]","img_url" : "ref_list[2]"},
                            {"title" : "pic_names[3]","img_url" : "ref_list[3]"}]

    weather = mars_weather
    return render_template("index.html",mars_table = mars_facts, mars_weather = weather, text = news_para, 
    text_title = news_title_txt, mars_feat_img = mars_feat_pic, hemi_pic_1 = mars_hemis[0]['img_url'], hemi_pic_2=mars_hemis[1]['img_url'],
    hemi_pic_3=mars_hemis[2]['img_url'],hemi_pic_4=mars_hemis[3]['img_url'],hemi_title_1=mars_hemis[0]['title'],hemi_title_2=mars_hemis[1]['title'],
    hemi_title_3 = mars_hemis[2]['title'], hemi_title_4 = mars_hemis[3]['title'])

@app.route("/scrape")
def scrape():
    import scrape_mars
    mars_dict = scrape_mars.scrape()
    time.sleep(20)
    dict_to_db = [{"mars_weather":mars_dict['mars_weather'],"mars_facts":mars_dict['mars_facts'], "hemisphere_image_urls" : mars_dict['hemisphere_image_urls'],
                "news_title":mars_dict['news_title'],"news_p":mars_dict['news_p'],"featured_image_url" : mars_dict['featured_image_url']}]
    db.mars.insert_many(dict_to_db)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
