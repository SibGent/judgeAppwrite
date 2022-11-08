<?php

use Appwrite\Client;
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

  if(!$req['variables']['APPWRITE_FUNCTION_ENDPOINT'] || !$req['variables']['APPWRITE_FUNCTION_API_KEY']) {
    echo('Environment variables are not set. Function cannot use Appwrite SDK.');
  } else {
    $client
      ->setEndpoint($req['variables']['APPWRITE_FUNCTION_ENDPOINT'])
      ->setProject($req['variables']['APPWRITE_FUNCTION_PROJECT_ID'])
      ->setKey($req['variables']['APPWRITE_FUNCTION_API_KEY'])
      ->setSelfSigned(true);
  }

  $userList = [];

  $result = $users->list();
  foreach ($result['users'] as $user) {
    $userList[] = [
      'id' => $user['$id'],
      'name' => $user['name'],
    ];
  }

  $res->json([
    'users' => $userList,
  ]);
};