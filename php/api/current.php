<?php
$api_port = getenv('PORT') ?: '8080';
$local_api_base = 'http://localhost:'.$api_port;
$api_path_prefix = '/webhook/auth';

function api_get($url) {
    $opts = ['http' => ['method' => "GET", 'timeout' => 5]];
    $context = stream_context_create($opts);
    $result = @file_get_contents($url, false, $context);
    return $result ? json_decode($result, true) : null;
}

header('Content-Type: application/json');

$type = $_GET['type'] ?? 'status';
if ($type === 'status') {
    echo json_encode(api_get($local_api_base . $api_path_prefix . '/status/short'));
} elseif ($type === 'connected') {
    echo json_encode(api_get($local_api_base . '/api/vrchat/connected'));
} else {
    echo json_encode(['error' => 'Unknown type']);
}
