from flask import Flask,request,make_response,jsonify
import requests
import certifi
import json
from pymongo import MongoClient,UpdateOne
import pymongo
import re
import datetime
import pytz

tz = pytz.timezone('Asia/Kolkata')
ca = certifi.where()

client = pymongo.MongoClient('mongodb+srv://whatsapp:v1prkDHjYLtrcB3C@cluster0.yclbutx.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.WhatsApp_DB


app = Flask(__name__)

@app.route('/')
def index():
    return 'Finance by Sharan WhatsApp Bot!'

def return_text_and_suggestion_chip_with_context(text,suggestions,context_session,context_parameter_name,context_value):
    suggestion_list = []
    for suggestion in suggestions:
        suggestion_list.append({"title":suggestion})
    return {"fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "simpleResponses": {
          "simpleResponses": [
            {
              "textToSpeech": text
            }
          ]
        }
      },
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "suggestions": {
          "suggestions": suggestion_list
        }
      },
      {
        "text": {
          "text": [
            text
          ]
        }
      }
    ],
    "outputContexts": [
      {
        "name": context_session+"/my_context",
        "lifespanCount": 25,
        "parameters": {
          context_parameter_name+".original":context_value,
          context_parameter_name:context_value
        }
      }
    ],}


def return_list(title,subtitle,options,descriptions,button_text,postback_text):
    options_list = []
    for option,description,postback in zip(options,descriptions,postback_text):
        options_list.append(
    {
                      "cells": [
                        {},
                        {
                          "text": option
                        },
                        {
                          "text": description
                        },
                        {
                            "text":postback
                        }
                        
                      ]
                    })
    return {"fulfillmentMessages": [
              {
                "platform": "ACTIONS_ON_GOOGLE",
                "simpleResponses": {
                  "simpleResponses": [
                    {
                      "textToSpeech": ""
                    }
                  ]
                }
              },
              {
                "platform": "ACTIONS_ON_GOOGLE",
                "tableCard": {
                  "title": title,
                  "subtitle": subtitle,
                  "columnProperties": [
                    {
                      "header": "Section Title",
                      "horizontalAlignment": "LEADING"
                    },
                    {
                      "header": "Option Title",
                      "horizontalAlignment": "LEADING"
                    },
                    {
                      "header": "Option Description",
                      "horizontalAlignment": "LEADING"
                    },
                    {
                      "header": "Postback text",
                      "horizontalAlignment": "LEADING"
                    }
                  ],
                  "rows": options_list,
                  "buttons": [
                    {
                      "title": button_text,
                      "openUriAction": {}
                    }
                  ]
                }
              },
              {
                "text": {
                  "text": [
                    ""
                  ]
                }
              }
            ]}

def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))


def return_text_and_suggestion_chip_with_context(text,suggestions,context_session,context_parameter_name,context_value):
    suggestion_list = []
    for suggestion in suggestions:
        suggestion_list.append({"title":suggestion})
    return {"fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "simpleResponses": {
          "simpleResponses": [
            {
              "textToSpeech": text
            }
          ]
        }
      },
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "suggestions": {
          "suggestions": suggestion_list
        }
      },
      {
        "text": {
          "text": [
            text
          ]
        }
      }
    ],
    "outputContexts": [
      {
        "name": context_session+"/my_context",
        "lifespanCount": 25,
        "parameters": {
          context_parameter_name+".original":context_value,
          context_parameter_name:context_value
        }
      }
    ],}

def return_text_with_context(text,context_session,context_parameter_name,context_value):
    
    parameters = {}
    for param,value in zip(context_parameter_name,context_value):
        parameters[param+".original"] = value
        parameters[param] = value

    return {"fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "simpleResponses": {
          "simpleResponses": [
            {
              "textToSpeech": text
            }
          ]
        }
      },
      {
        "text": {
          "text": [
            text
          ]
        }
      }
    ],
    "outputContexts": [
      {
        "name": context_session+"/my_context",
        "lifespanCount": 25,
        "parameters": parameters
      }
    ],}
    

def return_file_with_buttons(subtitle,text,url,suggestions):
    suggestion_list = []
    for suggestion in suggestions:
        suggestion_list.append({"title":suggestion})
    return {"fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "basicCard": {
          "subtitle": subtitle,
          "formattedText": text,
          "image": {
            "imageUri": url,
            "accessibilityText": "Please try again later"
          }
        }
      },
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "suggestions": {
          "suggestions": suggestion_list
        }
      }
    ]}


def return_text_and_suggestion_chip(text,suggestions):
    suggestion_list = []
    for suggestion in suggestions:
        suggestion_list.append({"title":suggestion})
    return {"fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "simpleResponses": {
          "simpleResponses": [
            {
              "textToSpeech": text
            }
          ]
        }
      },
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "suggestions": {
          "suggestions": suggestion_list
        }
      },
      {
        "text": {
          "text": [
            text
          ]
        }
      }
    ]}

def send_aisensy_template_message(template_name,destination,reciever_name,template_params,media_url):
        url = "https://backend.aisensy.com/campaign/t1/api"

        headers = {
                    "Content-Type": "application/json"}

        data = {
          "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1MzExZGI2ZWI4OGZkMWI0YjE0ZjdmMCIsIm5hbWUiOiJGaW5hbmNlIFdpdGggU2hhcmFuIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY1MWQ1N2QxYzk3YWQ2MGI1NWQ0NjE4OCIsImFjdGl2ZVBsYW4iOiJOT05FIiwiaWF0IjoxNjk3NzE3Njg3fQ.dCKR0o0EAB71P4bZUSR0169mc6OAxu6v7TSeZOfJmrI",
          "campaignName": template_name,
          "destination": destination,
          "userName": reciever_name ,
          "templateParams": template_params,
          "media":{
              "url":media_url,
          "filename":"Image by Sharan"}
        }

        resp = requests.post(url, headers=headers, json=data)
        


def return_only_text(text):
    return {'fulfillmentMessages':[{"text":{"text":[text]}}]}


def results():
    req = request.get_json(force=True)
    #print(req)
    
    intent_name = req['queryResult']['intent']['displayName']
    whatsapp_mobile_number = req['originalDetectIntentRequest']['payload']['AiSensyMobileNumber']
    whatsapp_mobile_number = re.sub('[^0-9]','',whatsapp_mobile_number)
    whatsapp_customer_name = req['originalDetectIntentRequest']['payload']['AiSensyName']
        
        
    if intent_name == "Default Welcome Intent":

        date = datetime.datetime.now(tz).date().day

        if date<=4:
            template_name = "WhatsApp_Comic_Day"+str(date)
        else:
            template_name = "WhatsApp_Comic_Daily_New"

        cursor = db.First_Message.find({})
        for c in cursor:
            topic = c['Topic_Name']
            url = c['Image_URL']

        name = whatsapp_customer_name
        
        if date<=4:
            template_params_dict = {"WhatsApp_Comic_Day1":[topic],"WhatsApp_Comic_Day2":[topic],"WhatsApp_Comic_Day3":[topic],
                           "WhatsApp_Comic_Day4":[topic]}

            template_params = template_params_dict[template_name]
            send_aisensy_template_message(template_name,whatsapp_mobile_number,name,template_params,url)
        else:

            first_place = 'Member'
            second_place = 'Member'
            third_place = 'Member'
            
            rank = 'NA'
            cursor = db.Leader_Board.find({"Mobile Number":whatsapp_mobile_number})
            for c in cursor:
                rank = str(c['Rank'])

            total_count = str(db.Users.count_documents({"Status":"ACTIVE"}))

            cursor = db.Leader_Board.find({"Rank":1})
            for c in cursor:
                first_place = c['Name']

            cursor = db.Leader_Board.find({"Rank":2})
            for c in cursor:
                second_place = c['Name']

            cursor = db.Leader_Board.find({"Rank":3})
            for c in cursor:
                third_place = c['Name']

            template_params_dict = {"WhatsApp_Comic_Day1":[topic],"WhatsApp_Comic_Day2":[topic],"WhatsApp_Comic_Day3":[topic],
                           "WhatsApp_Comic_Day4":[topic],"WhatsApp_Comic_Daily_New":[topic.strip(),str(rank),total_count,first_place,second_place,third_place]}


            template_params = template_params_dict[template_name]

            send_aisensy_template_message(template_name,whatsapp_mobile_number,name,template_params,url)
        
        
        
    if intent_name=="Quiz Me":
        context_session = re.findall("\'name\':\s\'(.*?)\/contexts",str(req))[0]+"/contexts"
        context_parameter_name = "correct_answer"
        if len(req['queryResult']['parameters']['quiz_answer'])<1:
            cursor = db.Quiz_Question.find({})
            for c in cursor:
                text = c['Quiz_Question']
                Button1 = c['Button1']
                Button2 = c['Button2']
                Button3 = c['Button3']
                correct_answer = c['Correct_Answer']
                
            context_value = correct_answer
            
            suggestions = [Button1,Button2,Button3]
                
            return return_text_and_suggestion_chip_with_context(text,suggestions,context_session,context_parameter_name,context_value)
        
        else:
            date = datetime.datetime.now(tz).date().day
            answer = req['queryResult']['parameters']['quiz_answer']
            cursor = db.Quiz_Question.find({})
            for c in cursor:
                text = c['Quiz_Question'].strip()
                Button1 = c['Button1'].strip()
                Button2 = c['Button2'].strip()
                Button3 = c['Button3'].strip()
                correct_answer = c['Correct_Answer'].strip()
                
            if answer == req['queryResult']['outputContexts'][0]['parameters']['correct_answer']:
                if db.Leader_Board.count_documents({"Mobile Number":str(whatsapp_mobile_number)})>0:
                    cursor = db.Leader_Board.find({"Mobile Number":str(whatsapp_mobile_number)})
                    for c in cursor:
                        score = int(c['Score'])
                        time = float(c['Time'])
                        
                    if score>=date:
                        score = score
                    else:
                        score = score +1
                    hours = datetime.datetime.now(tz).hour
                    minutes = datetime.datetime.now(tz).minute
                    seconds = datetime.datetime.now(tz).second

                    new_time = (hours*60)+minutes+(seconds/60)
                        
                    db.Leader_Board.update_one(
                                {
                                    "Mobile Number" : whatsapp_mobile_number
                                },
                                {
                                    "$set" :
                                    {
                                        "Score" : int(score),
                                        "Time":float(time+new_time)
                                    }
                                }
                            )
                
                    return return_only_text("Great job! That's the right answer.")
                
                else:
                    hours = datetime.datetime.now(tz).hour
                    minutes = datetime.datetime.now(tz).minute
                    seconds = datetime.datetime.now(tz).second

                    new_time = (hours*60)+minutes+(seconds/60)
                    
                    db.Leader_Board.insert_one({
                    "Mobile Number":whatsapp_mobile_number,
                    "Name":whatsapp_customer_name,
                    "Score":int(1),
                    "Time":float(new_time)
                    })
                    
                    return return_only_text("Great job! That's the right answer.")
                
            else:
                text = "That's not the right answer, better luck next time! The correct answer is "+correct_answer
                return return_only_text(text)
            
    if intent_name == "Check Rank":
        cursor = db.Leader_Board.find().sort([('Score', -1), ('Time', 1)])   # 1 for ascending order, -1 for descending order
        sorted_documents = list(cursor)

        for rank, document in enumerate(sorted_documents, start=1):

            db.Leader_Board.update_one({'_id': document['_id']}, {'$set': {'Rank': rank}})
            
        cursor = db.Leader_Board.find({"Mobile Number":whatsapp_mobile_number})
        for c in cursor:
            rank = c['Rank']
            
        total_count = db.Leader_Board.count_documents({})
        text = "Your rank is *#"+str(rank)+"/"+str(total_count)+"*"
        return return_only_text(text)
    
    if intent_name == "Tell Me More":
        cursor = db.First_Message.find({})
        for c in cursor:
            text = c['Tell_Me_More']
            
        return return_text_and_suggestion_chip(text,['Additional Resources'])
            
    if intent_name == "Additional Resources":
        cursor = db.First_Message.find({})
        for c in cursor:
            text = c['Additional_Resources']
            
        return return_only_text(text)
    
def results_insert_data():
    try:
        req = request.get_json(force=True)
        mobile = req['mobile']
        status = req['status']
        name = req['name']
        email = req['email']
        updated_at = datetime.datetime.now(tz).ctime()
        created_at = datetime.datetime.now(tz).ctime()


        db.Users.insert_one({
                    "Mobile":str(mobile).strip(),
                    "Status":str(status).strip(),
                    "Name":str(name).strip(),
                    "Email":str(email).strip(),
                    "Updated_At":str(updated_at).strip(),
                    "Created_At":str(created_at).strip()})

        return {"Response":"Success"}
    
    except:
        return {"Response":"Error Occurred"}
        
@app.route('/api/', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))


@app.route('/insert_data/', methods=['GET', 'POST'])
def webhook_insert_data():
    # return response
    return make_response(jsonify(results_insert_data()))


if __name__ == '__main__':
    app.run()
    #app.run(host="0.0.0.0",port = 8000)