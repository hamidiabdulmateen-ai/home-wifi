<?php
$botToken = "8416601223:AAFR42VtKLQivbihzQNSutUS-hQ4nTNy_oQ"; // توکن رباتت
$chatId = "6689313262";     // Chat ID خودت
$message = isset($_GET['msg']) ? $_GET['msg'] : 'تغییری در سایت رخ داد!';

file_get_contents("https://api.telegram.org/bot$botToken/sendMessage?chat_id=$chatId&text=" . urlencode($message));
?>
