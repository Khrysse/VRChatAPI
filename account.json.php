<?php
define('ACCESS_TOKEN', 'mon_token_de_securite_ici');

if (!isset($_GET['token']) || $_GET['token'] !== ACCESS_TOKEN) {
    header('HTTP/1.1 401 Unauthorized');
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

$jsonContent = <<<'JSON'
{
  "manual_username": "user123",
  "displayName": "User Display Name",
  "user_id": "abcdef123456",
  "auth": "xxxxxxxxxxxxxxx==",
  "auth_cookie": "yyyyyyyyyyyyyy",
  "created_at": "2025-06-22T14:00:00+00:00"
}
JSON;

header('Content-Type: application/json');
echo $jsonContent;

?>