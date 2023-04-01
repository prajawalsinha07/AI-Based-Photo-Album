import json
import dateutil.parser
import datetime
import time
import os
import boto3
import requests
import urllib.parse
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection

headers = {"Content-Type": "application/json"}
access_key = "AKIAYSUV7W6CS2CDHDMV"
secret_key = "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"
host = "search-photos-crojucj44o6khrrkqarxezqmge.us-east-1.es.amazonaws.com"
region = "us-east-1"
service = "es"
awsauth = AWSRequestsAuth(aws_access_key = access_key, aws_secret_access_key = secret_key, aws_region = region, aws_service = service, aws_host = host)
es = Elasticsearch(hosts = [{'host': host, 'port': 443}], http_auth = awsauth, use_ssl = True, verify_certs = True, connection_class = RequestsHttpConnection)
lex = boto3.client('lex-runtime', region_name=region)

def lambda_handler(event, context):
    print(event)
    q1 = event['q']
    print("q1:", q1 )
    labels = get_labels(q1)
    print("labels", labels)
    if len(labels) != 0:
        img_paths = get_photo_path(labels)

    if not img_paths:
        return{
            'statusCode':200,
            "headers": {"Access-Control-Allow-Origin":"*"},
            'body': json.dumps('No Results found')
        }
    else:    
        return{
            'statusCode': 200,
            'headers': {"Access-Control-Allow-Origin":"*"},
            'body': {
                'imagePaths':img_paths,
                'userQuery':q1,
                'labels': labels,
            },
            'isBase64Encoded': False
        }
        
    # query = event.get("currentIntent").get("slots")
    # utterance = event.get("inputTranscript")
    # print(query)
    # print(utterance)
    # slotOne = query.get("slotOne")
    # slotTwo = query.get("slotTwo")
    # slotThree = query.get("slotThree")
    
    # labels = []
    
    # if slotOne != 'None':
    #     labels.append(slotOne)
        
    # if slotTwo != 'None':
    #     labels.append(slotTwo)
        
    # if slotThree != 'None':
    #     labels.append(slotThree)
        
    # if len(labels) != 0:
    #     img_paths = get_photo_path(labels)

    # print(img_paths)
    # if not img_paths:
    #     return{
    #         'statusCode':200,
    #         "headers": {"Access-Control-Allow-Origin":"*"},
    #         'body': json.dumps('No Results found')
    #     }
    # else:    
    #     return{
    #         'statusCode': 200,
    #         'headers': {"Access-Control-Allow-Origin":"*"},
    #         'body': {
    #             'imagePaths':img_paths,
    #             'userQuery':utterance,
    #             'labels': labels,
    #         },
    #         'isBase64Encoded': False
    #     }

def get_labels(query):
    response = lex.post_text(
        botName='CloudProject',                 
        botAlias='$LATEST',
        userId="string",           
        inputText=query
    )
    print("lex-response", response)
    
    labels = []
    if 'slots' not in response:
        print("No photo collection for query {}".format(query))
    else:
        print ("slot: ",response['slots'])
        slot_val = response['slots']
        for key,value in slot_val.items():
            if value!=None:
                labels.append(value)
    return labels
    
def get_photo_path(keys):
    resp = []
    for key in keys:
        if (key is not None) and key != '':
            searchData = es.search({"query": {"match": {"labels": key}}})
            resp.append(searchData)
    print(resp)
    output = []
    for r in resp:
        if 'hits' in r:
             for val in r['hits']['hits']:
                key = val['_source']['objectKey']
                if key not in output:
                    output.append('https://cloud-project-photos.s3.amazonaws.com/'+key)
    return output   