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

  $databaseId = '6361668457d4ac7662fe';
  $colSession = '6361670a04b612e88077';
  $colCompetitor = '63620f139fa54f3c5754';
  $colScore = '636fb027bc44b3b389b4';
  $colDeduction = '6370d5eaf144b7909698';
  $colJudge = '637aece8101af4477b11';
  
  $sessionId = '637b6e6709dc00c94feb';
  
  $session = $database->getDocument($databaseId, '6361670a04b612e88077', $sessionId);
  $judgeIds = $session['judgeListIds'];
  $arbitratorIds = $session['arbitratorListIds'];
  
  $competitorList = $database->listDocuments($databaseId, $colCompetitor, [
      Query::equal('sessionId', $sessionId),
  ])['documents'];
  
  $scoreList = $database->listDocuments($databaseId, $colScore, [
      Query::equal('sessionId', $sessionId),
  ])['documents'];
  
  $deductionList = $database->listDocuments($databaseId, $colDeduction, [
      Query::equal('sessionId', $sessionId),
  ])['documents'];
  
  $judgeList = $database->listDocuments($databaseId, $colJudge, [
      Query::equal('sessionId', $sessionId),
  ])['documents'];
  
  $out = [];
  $judgeIds_A = getJudgeIds($judgeList, 'role', 'artistic');
  $judgeIds_E = getJudgeIds($judgeList, 'role', 'execution');
  $judgeIds_D = getJudgeIds($judgeList, 'role', 'difficulty');
  
  foreach ($competitorList as $competitor) {
    $id = $competitor['$id'];
    $number = $competitor['number'];
    $name = $competitor['name'];
    $city = $competitor['city'];
    $scoreArtistic = getScore($scoreList, $judgeIds_A, $id);
    $meanArtistic = getMeanScore($scoreArtistic);
    $scoreExecution = getScore($scoreList, $judgeIds_E, $id);
    $meanExecution = getMeanScore($scoreExecution);
    $scoreDifficulty = getScore($scoreList, $judgeIds_D, $id);
    $meanDifficulty = getMeanScore($scoreDifficulty);
    $deduction = getDeduction($deductionList, $arbitratorIds, $id);
    $total = getTotal($meanArtistic, $meanDifficulty, $meanExecution, $deduction);

    $out[] = [
      'number' => $number,
      'name' => $name,
      'city' => $city,
      'scoreArtistic' => $scoreArtistic,
      'meanArtistic' => $meanArtistic,
      'scoreExecution' => $scoreExecution,
      'meanExecution' => $meanExecution,
      'scoreDifficulty' => $scoreDifficulty,
      'meanDifficulty' => $meanDifficulty,
      'deduction' => $deduction,
      'total' => $total,
    ];
  }
  
  $out = sortByTotal($out);

  $place = 1;
  foreach ($out as $key => $value) {
      $out[$key]['place'] = $place;
      $place++;
  }
 
  var_dump($out);
  
  $res->json([
    'areDevelopersAwesome' => true,
  ]);
};