<?php

use Appwrite\Client;
use Appwrite\InputFile;
use Appwrite\Query;
// You can remove imports of services you don't use
use Appwrite\Services\Account;
use Appwrite\Services\Avatars;
use Appwrite\Services\Databases;
use Appwrite\Services\Functions;
use Appwrite\Services\Health;
use Appwrite\Services\Locale;
use Appwrite\Services\Storage;
use Appwrite\Services\Teams;
use Appwrite\Services\Users;

require_once 'vendor/autoload.php';
require_once 'utils.php';

/*
  '$req' variable has:
    'headers' - object with request headers
    'payload' - request body data as a string
    'variables' - object with function variables

  '$res' variable has:
    'send(text, status)' - function to return text response. Status code defaults to 200
    'json(obj, status)' - function to return JSON response. Status code defaults to 200

  If an error is thrown, a response with code 500 will be returned.
*/

return function($req, $res) {
  $client = new Client();

  // You can remove services you don't use
  $account = new Account($client);
  $avatars = new Avatars($client);
  $database = new Databases($client);
  $functions = new Functions($client);
  $health = new Health($client);
  $locale = new Locale($client);
  $storage = new Storage($client);
  $teams = new Teams($client);
  $users = new Users($client);

  if(!$req['variables']['APPWRITE_FUNCTION_ENDPOINT'] || !$req['variables']['APPWRITE_FUNCTION_API_KEY']) {
    echo('Environment variables are not set. Function cannot use Appwrite SDK.');
  } else {
    $client
      ->setEndpoint($req['variables']['APPWRITE_FUNCTION_ENDPOINT'])
      ->setProject($req['variables']['APPWRITE_FUNCTION_PROJECT_ID'])
      ->setKey($req['variables']['APPWRITE_FUNCTION_API_KEY'])
      ->setSelfSigned(true);
  }

  $sessionId = '6374a0530cecab0cf787';
  $databaseId = '6361668457d4ac7662fe';

  $session = $database->getDocument($databaseId, '6361670a04b612e88077', $sessionId);
  
  $judgeListIds = $session['judgeListIds'];
  $arbitratorListIds = $session['arbitratorListIds'];

  $competitorList = $database->listDocuments($databaseId, '63620f139fa54f3c5754', [
    Query::equal('sessionId', $sessionId),
  ]);

  $scoreList = $database->listDocuments($databaseId, '636fb027bc44b3b389b4', [
    Query::equal('sessionId', $sessionId),
  ]);

  $deductionList = $database->listDocuments($databaseId, '6370d5eaf144b7909698', [
    Query::equal('sessionId', $sessionId),
  ]);

  $juryNameList = $users->list([
    Query::equal('$id', array_merge($judgeListIds, $arbitratorListIds)),
  ]);
  
  $out = [];
  
  foreach ($competitorList['documents'] as $doc) {
    $id = $doc['$id'];
    $number = $doc['number'];
    $name = $doc['name'];
    $discipline = $doc['discipline'];
    $age = $doc['age'];
    $scores = [];
    $deduction = [];
    $total = 0.0;
    $place = 0;
      
    foreach ($judgeListIds as $judgeId) {
      $judgeName = getUserNames($juryNameList['users'], $judgeId);
      $value = searchScore($scoreList['documents'], $id, $judgeId);

      $scores[$judgeName] = $value;
    }

    foreach ($arbitratorListIds as $arbitratorId) {
      $arbitratorName = getUserNames($juryNameList['users'], $arbitratorId);
      $value = searchDeduction($deductionList['documents'], $id, $arbitratorId);

      $deduction[$arbitratorName] = $value;
    }
  
    $total = sumTotal($scores, $deduction);

    $out[] = [
      'number' => $number,
      'name' => $name,
      'discipline' => $discipline,
      'age' => $age,
      // 'scores' => $scores,
      // 'deduction' => $deduction,
      // 'total' => $total,
      // 'place' => $place,
    ];

    foreach ($scores as $key => $value) {
      $out[count($out) - 1][$key] = $value;
    }

    foreach ($deduction as $key => $value) {
      $out[count($out) - 1][$key] = $value;
    }

    $out[count($out) - 1]['total'] = $total;
    $out[count($out) - 1]['place'] = $place;
  }
  
  uasort($out, function($a, $b) {
    if ($a['total'] == $b['total']) {
      return 0;
    }

    return $a['total'] < $b['total'] ? 1 : -1;
  });
  $out  = array_values($out);
  
  $place = 1;
  foreach ($out as $key => $value) {
    $out[$key]['place'] = $place;
    $place++;
  }
    
  // $headerStart = ['№', 'Фамилия Имя', 'Дисциплина', 'Возраст'];
  // $headerJudge = array_values($out[0]['scores']);
  // $headerArbitrator = array_values($out[0]['deduction']);
  // $headerEnd = ['Общий балл', 'Место'];

  // $header = array_merge($headerStart, $headerJudge, $headerArbitrator, $headerEnd);

  // var_dump($header);
  var_dump($out);

  // var_dump($headerJudge);
  // echo PHP_EOL;
  // var_dump($headerArbitrator);

  // $books = [
  //   ['ISBN', 'title', 'author', 'publisher', 'ctry' ],
  //   [618260307, 'The Hobbit', 'J. R. R. Tolkien', 'Houghton Mifflin', 'USA'],
  //   [908606664, 'Slinky Malinki', 'Lynley Dodd', 'Mallinson Rendel', 'NZ']
  // ];

  $xlsx = Shuchkin\SimpleXLSXGen::fromArray( $out );
  $xlsx->saveAs('books.xlsx');
  $result = $storage->createFile('637922611c551cb7d2fb', 'unique()', InputFile::withPath('books.xlsx'));

  $res->json([
    'areDevelopersAwesome' => true,
    // 'userList' => $userList,
    // 'result' => $result,
  ]);
};