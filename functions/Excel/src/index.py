from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.services.users import Users
from appwrite.input_file import InputFile

from appwrite.query import Query

from .report import *
from .protocol import *

"""
  'req' variable has:
    'headers' - object with request headers
    'payload' - request body data as a string
    'variables' - object with function variables

  'res' variable has:
    'send(text, status)' - function to return text response. Status code defaults to 200
    'json(obj, status)' - function to return JSON response. Status code defaults to 200

  If an error is thrown, a response with code 500 will be returned.
"""

def main(req, res):
  client = Client()
  database = Databases(client)
  storage = Storage(client)
  users = Users(client)

  if not req.variables.get('APPWRITE_FUNCTION_ENDPOINT') or not req.variables.get('APPWRITE_FUNCTION_API_KEY'):
    print('Environment variables are not set. Function cannot use Appwrite SDK.')
  else:
    (
    client
      .set_endpoint(req.variables.get('APPWRITE_FUNCTION_ENDPOINT', None))
      .set_project(req.variables.get('APPWRITE_FUNCTION_PROJECT_ID', None))
      .set_key(req.variables.get('APPWRITE_FUNCTION_API_KEY', None))
      .set_self_signed(True)
    )
  
  # init params
  sessionId = str(req.payload)
  
  databaseId = '6361668457d4ac7662fe'
  colSession = '6361670a04b612e88077'
  colCompetitor = '63620f139fa54f3c5754'
  colScore = '636fb027bc44b3b389b4'
  colDeduction = '6370d5eaf144b7909698'
  colMeta = '63848772123ad6bd5baa'

  # work it
  session = database.get_document(databaseId, colSession, sessionId)

  equalSessionId = [Query.equal('sessionId', sessionId), Query.limit(100)]
  competitorList = database.list_documents(databaseId, colCompetitor, equalSessionId)['documents']
  scoreList = database.list_documents(databaseId, colScore, equalSessionId)['documents']
  deductionList = database.list_documents(databaseId, colDeduction, equalSessionId)['documents']
  main_judge = database.get_document(databaseId, colMeta, session['mainJudgeId'])
  secretary = database.list_documents(databaseId, colMeta, [Query.equal('$id', session['secretaryListIds']), Query.limit(1)])['documents'][0]

  judge_name = f'{main_judge["surname"]} {main_judge["name"]} {main_judge["patronymic"]} ({main_judge["region"]})'
  secretary_name = f'{secretary["surname"]} {secretary["name"]} {secretary["patronymic"]} ({main_judge["region"]})'
  
  bucketId = '637922611c551cb7d2fb'
  report_data = get_report_data(session, competitorList, scoreList, deductionList)
  build_protocol('protocol.xlsx', report_data, judge_name, secretary_name)
  file_meta = storage.create_file(bucketId, 'unique()', InputFile.from_path('protocol.xlsx'))
  
  return res.json(file_meta)