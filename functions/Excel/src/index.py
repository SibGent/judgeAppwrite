from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.services.users import Users

from appwrite.query import Query

from .utils import *

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
  
  databaseId = '6361668457d4ac7662fe'
  colSession = '6361670a04b612e88077'
  colCompetitor = '63620f139fa54f3c5754'
  colScore = '636fb027bc44b3b389b4'
  colDeduction = '6370d5eaf144b7909698'
  colJudge = '637aece8101af4477b11'

  sessionId = '637b6e6709dc00c94feb'

  # read from database
  session = database.get_document(databaseId, colSession, sessionId)
  judgeIds = session['judgeListIds']
  arbitratorIds = session['arbitratorListIds']

  equalSessionId = [Query.equal('sessionId', sessionId)]
  competitorList = database.list_documents(databaseId, colCompetitor, equalSessionId)['documents']
  scoreList = database.list_documents(databaseId, colScore, equalSessionId)['documents']
  deductionList = database.list_documents(databaseId, colDeduction, equalSessionId)['documents']
  judgeList = database.list_documents(databaseId, colJudge, equalSessionId)['documents']

  # get ids of judges
  judgeIds_A = [judge['userId'] for judge in judgeList if judge['role'] == 'artistic']
  judgeIds_E = [judge['userId'] for judge in judgeList if judge['role'] == 'execution']
  judgeIds_D = [judge['userId'] for judge in judgeList if judge['role'] == 'difficulty']

  out = []

  for competitor in competitorList:
      _id = competitor['$id']
      number = competitor['number']
      name = competitor['name']
      city = competitor['city']
      
      scoreArtistic = getScore(scoreList, judgeIds_A, _id)
      scoreExecution = getScore(scoreList, judgeIds_E, _id)
      scoreDifficulty = getScore(scoreList, judgeIds_D, _id)
      
      meanArtistic = getMeanScore(scoreArtistic)
      meanExecution = getMeanScore(scoreExecution)
      meanDifficult = getMeanScore(scoreDifficulty)
      
      deduction = getDeduction(deductionList, arbitratorIds, _id)
      total = getTotal(meanArtistic, meanExecution, meanDifficult, deduction)

      out.append({
          'number': number,
          'name': name,
          'city': city,
          'scoreArtistic': scoreArtistic,
          'meanArtistic': meanArtistic,
          'scoreExecution': scoreExecution,
          'meanExecution': meanExecution,
          'scoreDifficulty': scoreDifficulty,
          'meanDifficult': meanDifficult,
          'deduction': deduction,
          'total': total,
      })

  # sort by total
  sortedOut = sorted(out, key=lambda d: d['total'], reverse=True)

  # added place
  place = 1
  for x in sortedOut:
      x['place'] = place
      place += 1
    
  print(sortedOut)

  return res.json({
    "areDevelopersAwesome": True,
  })