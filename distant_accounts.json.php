<?php
$authorized_ip = '0.0.0.0';
$allowed_origin_prefix = 'https://vrchatapi-';
$allowed_origin_suffix = '.kvs.fyi';

$client_ip = $_SERVER['REMOTE_ADDR'] ?? '';
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';

function startsWith($haystack, $needle) {
    return substr($haystack, 0, strlen($needle)) === $needle;
}

function endsWith($haystack, $needle) {
    return substr($haystack, -strlen($needle)) === $needle;
}

$is_ip_allowed = $client_ip === $authorized_ip;
$is_origin_allowed = startsWith($origin, $allowed_origin_prefix) && endsWith($origin, $allowed_origin_suffix);

if (!$is_ip_allowed && !$is_origin_allowed) {
    header("Location: https://github.com/unstealable");
    exit;
}

$vrchat_token = [
    "manual_username" => "TonUsername",
    "displayName" => "TonDisplayName",
    "user_id" => "usr_abcdef1234567890",
    "auth" => "ZGF0YQ==",
    "auth_cookie" => "auth_cookie_valeur"
];

header('Content-Type: application/json');
echo json_encode($vrchat_token, JSON_PRETTY_PRINT);
