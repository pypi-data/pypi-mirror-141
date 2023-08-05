import os
import time
import datetime
import logging
from io import BytesIO
from datetime import datetime

import json

from urllib.request import urlopen
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from croniter import croniter
from flask.wrappers import Response

import jwt
import boto3
import flask
import requests

from .renderer.excel import ExcelRenderer
from .constants import DATETIME_FORMAT
logger = logging.getLogger(__name__)

BASE_API_URL = os.getenv('DATA_API_BASE_URL', '')
API_RETRY = int(os.getenv('API_RETRY', 3))
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BASE_API_URL = os.getenv('DATA_API_BASE_URL', '')
PLATFORM_ROUTE = os.getenv("PLATFORM_ROUTE")

storage_name = os.getenv('STORAGE_NAME')

global ACCESS_KEY_ID, SECRET_ACCESS_KEY, REGION_NAME, BUCKET_NAME
ACCESS_KEY_ID = ''
SECRET_ACCESS_KEY = ''
REGION_NAME = ''
BUCKET_NAME = ''

if storage_name == 's3_storage':
    ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    REGION_NAME = os.getenv('REGION_NAME')
    BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
elif storage_name == 'ceph_storage':
    ACCESS_KEY_ID = os.getenv('CEPH_ACCESS_KEY_ID')
    SECRET_ACCESS_KEY = os.getenv('CEPH_SECRET_ACCESS_KEY')
    BUCKET_NAME = os.getenv('CEPH_BUCKET_NAME')
    REGION_NAME = os.getenv('CEPH_REGION_NAME')
else:
    logger.info("No storages are found")


def get_token():
    headers = {"Content-Type" : "application/x-www-form-urlencoded" , "Accept" : "application/json"};
    post_data = {"grant_type": "client_credentials", "client_id" : API_KEY, "client_secret" : API_SECRET};
    token_url = BASE_API_URL + "/auth/oauth/token";
    response = requests.post(token_url,data=post_data,headers=headers,verify=False);
    json = response.json();
    auth = str(json["access_token"])
    return auth


def get_headers():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_token()}'
    }

    return headers


def call_requests(method, url, params=None, data=None, json=None, verify=True):
    headers = get_headers()
    retry = 1
    resp = None
    while retry <= API_RETRY:
        try:
            resp = requests.request(method, url, params=params, data=data, json=json, headers=headers, verify=verify)
            if not resp.ok:
                time.sleep(retry * 2)
                retry+=1
                continue
        except requests.exceptions.ConnectionError:
            time.sleep(retry * 2)
            retry+=1
            continue

        return resp
    
    return resp

def call_get_requests(url, params=None, verify=True):
    return call_requests('GET', url, params, verify=verify)


def call_post_requests(url, params=None, data=None, verify=True):
    return call_requests('POST', url, params, data, verify=verify)


def get_epoc_from_datetime_string(str_datetime):
    timestamp = datetime.strptime(str_datetime, DATETIME_FORMAT).timestamp()
    return timestamp


def get_result_by_run(run_id, field=None, default_value=None):
    try:
        s3 = get_s3_client()
        run_id= f'analytics-apps/{PLATFORM_ROUTE}/json/{run_id}'
        res_object = s3.get_object(Bucket=BUCKET_NAME,Key=run_id)
        serializedObject = res_object['Body'].read()
        result = json.loads(serializedObject)
        if field:
            result = result.get(field, default_value)
        return result
    except Exception:
        logger.error('An error occurred (NoSuchKey) when calling the GetObject operation: The specified key does not exist')
        pass


def get_ses_client():
    return boto3.client('ses',
                        region_name=REGION_NAME,
                        aws_access_key_id=ACCESS_KEY_ID,
                        aws_secret_access_key=SECRET_ACCESS_KEY)


def get_s3_client():
    return boto3.client('s3',
                        region_name=REGION_NAME,
                        aws_access_key_id=ACCESS_KEY_ID,
                        aws_secret_access_key=SECRET_ACCESS_KEY)
    

def send_email(subject, from_email, to_emails, body, attachment=None):
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_emails

    # message body
    part = MIMEText(body, 'html')
    message.attach(part)

    if attachment:
        attachment_body = urlopen(attachment).read()
        part = MIMEApplication(attachment_body)
        part.add_header('Content-Disposition', 'attachment', filename=attachment)
        message.attach(part)

    resp = get_ses_client().send_raw_email(
        Source=message['From'],
        Destinations=to_emails.split(','),
        RawMessage={
            'Data': message.as_string()
        }
    )

    return resp


def upload_to_s3(content, location):
    '''
    :param: content: bytes
    :param: location: str
    '''
    s3 = boto3.resource('s3',
                        region_name=REGION_NAME,
                        aws_access_key_id=ACCESS_KEY_ID,
                        aws_secret_access_key=SECRET_ACCESS_KEY)
    object_url = f'https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{location}'

    try:
        s3.Bucket(BUCKET_NAME).put_object(Body=content,
                                             Key=location)
        return object_url
    except Exception:
        pass
    

def generate_pdf(analysis_run):
    logger.info('Entered into pdf generation process')
    url = os.getenv("PDF_SERVICE")
    # analysis_run = json.dumps(analysis_run)
    data = {
        'domain': BASE_API_URL,
        'report': PLATFORM_ROUTE,
        'run': analysis_run,
        'route': '/full-view',
        'token': get_token(),
        'size': 'A4'
    }

    res = requests.post(url, data=data).json()
    logger.info('Pdf response is: %s', res)
    return res



def generate_excel(analysis_run, file_name=None):
    try:
        excel_renderer = ExcelRenderer(analysis_run)
        workbook = excel_renderer.render()
    except Exception as ex:
        raise ex

    if file_name:
        output = None
        workbook.save(file_name)
    else:
        output = BytesIO()
        workbook.save(output)

    return output


def update_results_url(response, analysisRunId):
        result_path=f'analytics-apps/{PLATFORM_ROUTE}/json/'
        location=result_path + analysisRunId
        result_url = upload_to_s3(json.dumps(response).encode(), location)
        logger.info('Compute results url is %s', result_url)
        url = BASE_API_URL + f'/api/v2/tenants/client_53/resources/{analysisRunId}'
        data={ 
                "description" : result_url
             }
        
        res = call_post_requests(url , data=json.dumps(data), verify=False);
        logger.info('Database update response is %s', res)


#Upload excel file to s3
def upload_excel_s3(local_file, bucket, s3_file):
    s3 = get_s3_client()
    try:
        s3.upload_file(local_file, bucket, s3_file)
        url = f'https://{bucket}.s3.{REGION_NAME}.amazonaws.com/{s3_file}'
        logger.info('Upload successful, result url is %s', url)
        return True
    except FileNotFoundError:
        logger.info('File was not found')
        return False
    except NoCredentialsError:
        logger.info('Invalid credentials')
        return False


#Delete excel_file from local path
def delete_excel_file(source_path):
    try:
        os.remove(source_path)
        logger.info('Excel file successfully deleted')
    except OSError as e:
        logger.info(f'Failed to delete: %s : %s % {file_path, e.strerror}')



#Generate excel file
def generate_excel_file(run_id):
    logger.info('Entered into excel generation process')
    excel_data=get_result_by_run(run_id, 'excel-data', {})
    reportname = f"{PLATFORM_ROUTE}" + '-' + datetime.now().strftime('%Y-%m-%d-%I-%M-%S') + '.xlsx'
    filepath = './' + reportname
    generate_excel(excel_data, filepath)
    excel_file_location = f'analytics-apps/{PLATFORM_ROUTE}/excel/' + reportname
    
    upload_excel_s3(filepath, BUCKET_NAME, excel_file_location)
    
    delete_excel_file(filepath)


def upload_excel(analysis_run, excel_file):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    s3_path = f'{analysis_run.analysis.app.slug}/excel/{timestamp}.xlsx'

    return upload_to_s3(excel_file, s3_path)
