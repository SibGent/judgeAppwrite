<?php

use Appwrite\Client;
use Appwrite\Services\Databases;

require_once 'vendor/autoload.php';

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
  $database = new Databases($client);

  if(!$req['variables']['APPWRITE_FUNCTION_ENDPOINT'] || !$req['variables']['APPWRITE_FUNCTION_API_KEY']) {
    echo('Environment variables are not set. Function cannot use Appwrite SDK.');
  } else {
    $client
      ->setEndpoint($req['variables']['APPWRITE_FUNCTION_ENDPOINT'])
      ->setProject($req['variables']['APPWRITE_FUNCTION_PROJECT_ID'])
      ->setKey($req['variables']['APPWRITE_FUNCTION_API_KEY'])
      ->setSelfSigned(true);
  }

  $databaseId = "6361668457d4ac7662fe";
  $colSession = "6361670a04b612e88077";
  $colScore = "636fb027bc44b3b389b4";
  $colDeduction = "6370d5eaf144b7909698";

  $payload = json_decode($req['payload'], true);
  $sessionId = $payload['sessionId'];
  $competitorId = $payload['competitorId'];

  $session = $database->getDocument($databaseId, $colSession, $sessionId);
  $judgeScoreIds = array_merge($session['judgeArtisticListIds'], $session['judgeExecutionListIds']);
  $judgeDeductionIds = array_merge($session['judgeDifficultyListIds'], $session['arbitratorListIds']);

  foreach ($judgeScoreIds as $judgeId) {
    $database->createDocument($databaseId, $colScore, 'unique()', [
      'sessionId' => $sessionId,
      'userId' => $judgeId,
      'competitorId' => $competitorId,
      'value' => 0.0,
    ]);
  }

  var_dump($judgeDeductionIds);
  foreach ($judgeDeductionIds as $judgeId) {
    var_dump($judgeId);
    var_dump(PHP_EOL);
    $database->createDocument($databaseId, $colDeduction, 'unique()', [
      'sessionId' => $sessionId,
      'userId' => $judgeId,
      'competitorId' => $competitorId,
      'value' => 0.0,
    ]);
  }

  $res->json([
    'isExecuted' => true
  ]);
};