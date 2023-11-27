from flask import Flask,request,make_response,jsonify
import requests
import certifi
import json
from pymongo import MongoClient
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


def return_only_text(text):
    return {'fulfillmentMessages':[{"text":{"text":[text]}}]}


def results():
    req = request.get_json(force=True)
    #print(req)
    
    intent_name = req['queryResult']['intent']['displayName']
    whatsapp_mobile_number = req['originalDetectIntentRequest']['payload']['AiSensyMobileNumber'][3:]
    whatsapp_customer_name = req['originalDetectIntentRequest']['payload']['AiSensyName']
        
        
    if intent_name == "Default Welcome Intent":
        
        date = datetime.datetime.now(tz).date().day
        
        if date>=6:
            
            cursor = db.First_Message.find({})
            for c in cursor:
                topic = c['Topic_Name']
                url = c['Image_URL']
                
            cursor = db.Leader_Board.find().sort([('Score', -1), ('Time', 1)])   # 1 for ascending order, -1 for descending order
            sorted_documents = list(cursor)

            for rank, document in enumerate(sorted_documents, start=1):

                db.Leader_Board.update_one({'_id': document['_id']}, {'$set': {'Rank': rank}})

            cursor = db.Leader_Board.find({"Mobile Number":whatsapp_mobile_number})
            for c in cursor:
                rank = c['Rank']

            total_count = db.Leader_Board.count_documents({})
            
            cursor = db.Leader_Board.find({"Rank":1})
            for c in cursor:
                first_place = c['Name']
                
            cursor = db.Leader_Board.find({"Rank":2})
            for c in cursor:
                second_place = c['Name']
                
            cursor = db.Leader_Board.find({"Rank":3})
            for c in cursor:
                third_place = c['Name']
            
            if len(first_place)<1:
                first_place = "Member"
                
            if len(second_place)<1:
                second_place = "Member"
                
            if len(third_place)<1:
                third_place = "Member"
            
            text = f"""Click ⬆ to read today's comic about Changing Times: *{topic}*

Today you are #{rank}/{total_count}

Who's leading this month? 👀
🥇 1st Place: {first_place}
🥈 2nd Place: {second_place}
🥉 3rd Place: {third_place}

Want to win prizes? 

Play today's quiz and level up!"""
            
        subtitle = "IMAGE"
        suggestions = ['Quiz Me','Tell Me More']
        
        return return_file_with_buttons(subtitle,text,url,suggestions)
        
        
        
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
            answer = req['queryResult']['parameters']['quiz_answer']
            cursor = db.Quiz_Question.find({})
            for c in cursor:
                text = c['Quiz_Question']
                Button1 = c['Button1']
                Button2 = c['Button2']
                Button3 = c['Button3']
                correct_answer = c['Correct_Answer']
                
            if answer == req['queryResult']['outputContexts'][0]['parameters']['correct_answer']:
                if db.Leader_Board.count_documents({"Mobile Number":str(whatsapp_mobile_number)})>0:
                    cursor = db.Leader_Board.find({"Mobile Number":str(whatsapp_mobile_number)})
                    for c in cursor:
                        score = int(c['Score'])
                        time = float(c['Time'])
                        
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
                                        "Score" : str(score+1),
                                        "Time":str(time+new_time)
                                    }
                                }
                            )
                
                    return return_only_text("Thank you for participating. Updated Score in "+str(score+1))
                
                else:
                    hours = datetime.datetime.now(tz).hour
                    minutes = datetime.datetime.now(tz).minute
                    seconds = datetime.datetime.now(tz).second

                    new_time = (hours*60)+minutes+(seconds/60)
                    
                    db.Leader_Board.insert_one({
                    "Mobile Number":whatsapp_mobile_number,
                    "Name":whatsapp_customer_name,
                    "Score":str(1),
                    "Time":str(new_time)
                    })
                    
                    return return_only_text("Thank you for participating.")
                
            else:
                text = "Opps! Incorrect answer"
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
        
@app.route('/api/', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))


if __name__ == '__main__':
    app.run()
    #app.run(host="0.0.0.0",port = 8000)