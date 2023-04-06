import json
import boto3
import time
import urllib.parse
import random
from elasticsearch import Elasticsearch, RequestsHttpConnection
from aws_requests_auth.aws_auth import AWSRequestsAuth



s3 = boto3.client('s3')

def lambda_handler(event, context):
    label_list=[]
    access_key = ""
    secret_key = ""
    host = ""
    region = "us-east-1"
    service = "es"
    awsauth = AWSRequestsAuth(aws_access_key = access_key, aws_secret_access_key = secret_key,
        aws_region = region, aws_service = service, aws_host = host)
        
    es = Elasticsearch(hosts = [{'host': host, 'port': 443}],
                       http_auth = awsauth, use_ssl = True,
                       verify_certs = True, connection_class = RequestsHttpConnection)
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

    print(bucket)
    print(key)
              
    print('reading image: {} from s3 bucket {}'.format(key, bucket))
    client = boto3.client('rekognition')
    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        MaxLabels=12,
        MinConfidence=80,
    )
    
    print('Detected labels for ' + key)
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))
        label_list.append(label['Name'])
    
    ts = time.gmtime()
    created_time = time.strftime("%Y-%m-%dT%H:%M:%S", ts)
    print('Image created at {}....'.format(created_time))
    
    image_object = {
        'objectKey':key,
        'bucket':bucket,
        'createdTimestamp':created_time,
        'labels':label_list
    }
    print(image_object)
    # es = data_index.connect_to_elastic_search()
    es.index(index="photos", doc_type="_doc", id=created_time, body=image_object)

    response = es.get(index="photos", doc_type="_doc", id=created_time)
   
    return response   
