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

function api_post($url, $data) {
    $options = [
        'http' => [
            'header'  => "Content-Type: application/json\r\n",
            'method'  => 'POST',
            'content' => json_encode($data),
            'timeout' => 5
        ]
    ];
    $context  = stream_context_create($options);
    $result = @file_get_contents($url, false, $context);
    return $result ? json_decode($result, true) : null;
}

$status = 'IDLE';
$last_error = null;
$message = null;
$form_type = null; 

$api_status = api_get($local_api_base . $api_path_prefix . '/status/short');
if ($api_status) {
    $status = $api_status['status'] ?? 'IDLE';
    $last_error = $api_status['last_error'] ?? null;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['login'])) {
        $username = trim($_POST['username'] ?? '');
        $password = trim($_POST['password'] ?? '');

        if ($username === '' || $password === '') {
            $message = "⚠️ Please fill in all fields of the login form.";
            $form_type = 'login';
        } else {
            $response = api_post($local_api_base . $api_path_prefix . '/login', [
                'username' => $username,
                'password' => $password
            ]);
            if ($response) {
                if (isset($response['message'])) {
                    $message = $response['message'];
                }
            } else {
                $message = "❌ Error communicating with the server.";
                $form_type = 'login';
            }
        }
    } elseif (isset($_POST['2fa'])) {
        $code = trim($_POST['code'] ?? '');

        if ($code === '') {
            $message = "⚠️ Please enter the 2FA code.";
            $form_type = '2fa';
        } else {
            $response = api_post($local_api_base . $api_path_prefix  . '/2fa', [
                'code' => $code
            ]);
            if ($response) {
                if (isset($response['message'])) {
                    $message = $response['message'];
                }
            } else {
                $message = "❌ Error communicating with the server.";
                $form_type = '2fa';
            }
        }
    }
} else {
    if ($status === 'NEED_CREDENTIALS') {
        $form_type = 'login';
    } elseif ($status === 'NEED_2FA') {
        $form_type = '2fa';
    }
}

$connected = null;
if ($status === 'CONNECTED') {
    $connected = api_get($local_api_base . $api_path_prefix . '/connected');
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VRChat Bridge</title>
    <link rel="icon" type="image/png" href="/assets/favicon/favicon-96x96.png" sizes="96x96" />
    <link rel="icon" type="image/svg+xml" href="/assets/favicon/favicon.svg" />
    <link rel="shortcut icon" href="/assets/favicon/favicon.ico" />
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/favicon/apple-touch-icon.png" />
    <meta name="apple-mobile-web-app-title" content="VRChat Bridge" />
    <link rel="manifest" href="/assets/favicon/site.webmanifest" />
    <link rel="stylesheet" href="assets/css/design.css">
    <script type="text/javascript" src="assets/js/poll.js"></script>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="header-content">
            <div class="logo">VB</div>
            <h1>VRChat Bridge</h1>
        </div>
    </header>

    <!-- Main Content -->
    <main class="main">
        <div class="card">
            <div class="card-header">
                <div class="card-logo">VB</div>
                <h2 class="card-title">Authentication</h2>
                <p class="card-description">Connect to VRChat API services via VRChat Bridge</p>
            </div>

            <div class="card-content">
                <!-- Loading State -->
                <div id="loading" class="loading">
                    <div class="spinner"></div>
                    <span>Loading...</span>
                </div>

                <!-- Error State -->
                <div id="error" class="alert hidden">
                    <span class="alert-text"></span>
                </div>

                <!-- Message Display -->
                <?php if ($message): ?>
                    <div class="alert <?php echo (strpos($message, '⚠️') !== false) ? 'warning' : ''; ?>">
                        <span class="alert-text"><?php echo htmlspecialchars($message); ?></span>
                    </div>
                <?php endif; ?>

                <!-- Connected State -->
                <div id="connected" class="connected-state hidden">
                    <div class="connected-icon">✅</div>
                    <p class="connected-text">Connected as</p>
                    <p class="connected-user" id="connected-user"></p>
                    <a id="connected-user-id" href="#" class="connected-user-id" target="_blank"></a>
                </div>

                <!-- Login Form -->
                <div id="form-login" class="hidden">
                    <form method="post" class="form">
                        <div class="form-group">
                            <label class="label" for="username">Username</label>
                            <input class="input" type="text" id="username" name="username" placeholder="Enter your username" required>
                        </div>
                        <div class="form-group">
                            <label class="label" for="password">Password</label>
                            <input class="input" type="password" id="password" name="password" placeholder="Enter your password" required>
                        </div>
                        <button type="submit" name="login" class="button">Log In</button>
                    </form>
                </div>

                <!-- 2FA Form -->
                <div id="form-2fa" class="hidden">
                    <form method="post" class="form">
                        <div class="form-group">
                            <label class="label" for="code">2FA Code</label>
                            <input class="input" type="text" id="code" name="code" placeholder="Enter your 2FA code" required>
                        </div>
                        <button type="submit" name="2fa" class="button">Validate 2FA</button>
                    </form>
                </div>

                <!-- No Connection State -->
                <div id="no-conn" class="idle-state hidden">
                    <div class="idle-icon">✅</div>
                    <p class="connected-text">No connections requested at this time.</p>
                </div>

                <!-- Last Error Display -->
                <div id="last-error" class="alert hidden">
                    <span class="alert-text"></span>
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <p class="footer-text">
                VRChat Bridge is not affiliated with, endorsed by, or connected to VRChat Inc. VRChat is a trademark of VRChat Inc. This is an independent third-party tool.
            </p>
            <p class="footer-small">For educational, personal and development purposes only.</p>
        </div>
    </footer>
</body>
</html>