<?php
// ===== تنظیمات ربات =====
$botToken = "8416601223:AAFR42VtKLQivbihzQNSutUS-hQ4nTNy_oQ"; // توکن ربات
$chatId   = "6689313262"; // Chat ID خودت

// ===== پیام دریافتی =====
$message = isset($_GET['msg']) ? $_GET['msg'] : 'تغییری در سایت رخ داد!';

// ===== ارسال پیام با cURL =====
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "https://api.telegram.org/bot$botToken/sendMessage");
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, [
    'chat_id' => $chatId,
    'text'    => $message
]);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);

// ===== بررسی نتیجه =====
if($response === false){
    $error = curl_error($ch);
    curl_close($ch);
    echo "خطا در ارسال پیام: $error";
} else {
    curl_close($ch);
    $result = json_decode($response, true);
    if($result['ok']){
        echo "پیام با موفقیت ارسال شد!";
    } else {
        echo "ارسال ناموفق: " . $result['description'];
    }
}
?>
