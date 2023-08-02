from flask import Flask,render_template,request
import requests
import logging
import os
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen
logging.basicConfig(filename="info.log", level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        try:
            file_path = "Base.csv"
            if os.path.exists(file_path):
                 os.remove(file_path)
            
            url = request.form['content'].replace(" ","")
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
            response = requests.get(url)
            
            soup = BeautifulSoup(response.content, "html.parser")

            name_tags = soup.find_all(class_="_2sc7ZR _2V5EHH")
            review_tags = soup.find_all(class_="_2-N8zT")
            rating_tags = soup.find_all(class_="_3LWZlK _1BLPMq")
            
            names = []
            for tag in name_tags:
                name = tag.text.strip()  # Remove any leading/trailing whitespaces from the name
                names.append(name)
            # reviews = [tag.text.strip() for tag in review_tags]
            reviews = []
            for tag in review_tags:
                review = tag.text.strip()
                reviews.append(review) 
            ratings = []
            for tag in rating_tags:
                rate = tag.text.strip()
                ratings.append(rate)

            data = [
               ["Name","Reviews","Rates"]
               ]
        
            for name, review, rate  in zip(names, reviews, ratings):
                 data.append([name, review, rate])   

            with open(file_path, mode='w', newline='') as file:
                   writer = csv.writer(file)
                   writer.writerows(data)
                   
            return render_template("base.html")       

        except Exception as e:
            logging.info(e)
            return 'something is wrong'
        
    else:
        return render_template('index.html')     
    
if __name__=="__main__":
    app.run(debug=True)       

            
                 
                 
            