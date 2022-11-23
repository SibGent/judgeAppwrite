from appwrite.client import Client

# You can remove imports of services you don't use
from appwrite.services.account import Account
from appwrite.services.avatars import Avatars
from appwrite.services.databases import Databases
from appwrite.services.functions import Functions
from appwrite.services.health import Health
from appwrite.services.locale import Locale
from appwrite.services.storage import Storage
from appwrite.services.teams import Teams
from appwrite.services.users import Users

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

  # You can remove services you don't use
  account = Account(client)
  avatars = Avatars(client)
  database = Databases(client)
  functions = Functions(client)
  health = Health(client)
  locale = Locale(client)
  storage = Storage(client)
  teams = Teams(client)
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
  
  import xlsxwriter
  workbook = xlsxwriter.Workbook('demo.xlsx')
  worksheet = workbook.add_worksheet()
  worksheet.set_column('A:A', 20)
  bold = workbook.add_format({'bold': True})
  worksheet.write('A1', 'Hello')
  worksheet.write('A2', 'World', bold)
  worksheet.write(2, 0, 123)
  worksheet.write(3, 0, 123.456)
  workbook.close()
  
  from appwrite.input_file import InputFile
  result = storage.create_file('637922611c551cb7d2fb', 'unique()', InputFile.from_path('demo.xlsx'))
  
  return res.json({
    "areDevelopersAwesome": True,
  })