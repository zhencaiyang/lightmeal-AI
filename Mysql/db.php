<?php
$host = 'localhost';
$user = 'root';
$pwd  = '123456';
$db   = 'test';

$conn = mysqli_connect($host, $user, $pwd, $db);
mysqli_set_charset($conn, 'utf8mb4');
?>