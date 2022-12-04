<?php

use Appwrite\Client;
use Appwrite\Query;
use Appwrite\Services\Databases;
use Appwrite\Services\Users;

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
  $users = new Users($client);
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

  $databaseId = '6361668457d4ac7662fe';
  $colMeta = '63848772123ad6bd5baa';
  
  $userIds = [];
  $userList = [];
  
  $result = $users->list([Query::limit(100)])['users'];
  
  foreach ($result as $user) {
      $userIds[] = $user['$id'];
  }
  
  $meta = $database->listDocuments($databaseId, $colMeta, [
    Query::equal('$id', $userIds),
    Query::limit(100),
  ])['documents'];
  
  
  foreach ($meta as $user) {
    $userList[] = [
      'id' => $user['$id'],
      'surname' => $user['surname'],
      'name' => $user['name'],
      'patronymic' => $user['patronymic'],
      'region' => $user['region'],
    ];
  }

  $res->json([
    'users' => $userList,
  ]);
};