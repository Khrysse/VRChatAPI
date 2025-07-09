<?php
// Restrict access to localhost only
if ($_SERVER['REMOTE_ADDR'] !== '127.0.0.1' && $_SERVER['REMOTE_ADDR'] !== '::1') {
    http_response_code(403);
    exit('Forbidden');
}

$api_port = getenv('PORT') ?: '8000';
$status_url = "http://localhost:$api_port/api/status";
$status = json_decode(@file_get_contents($status_url), true);

if (!$status || empty($status['auth'])) {
    // Restart the Python process via supervisord
    shell_exec('supervisorctl restart python');

    // Send a Discord notification
    $webhook_url = getenv('DISCORD_WEBHOOK_URL');
    $discord_user_id = getenv('DISCORD_USER_ID');
    if ($webhook_url && $discord_user_id) {
        $discord_message = "<@$discord_user_id> : VRChat auth failed, Python system restarted automatically.";
        send_discord_webhook($webhook_url, $discord_message);
    }

    echo "Auth is invalid, Python system restarted and Discord notified!";
} else {
    echo "Auth is valid.";
}

function send_discord_webhook($webhook_url, $message) {
    $data = json_encode([
        "content" => $message
    ]);
    $options = [
        'http' => [
            'header'  => "Content-type: application/json\r\n",
            'method'  => 'POST',
            'content' => $data,
        ],
    ];
    $context  = stream_context_create($options);
    @file_get_contents($webhook_url, false, $context);
} 