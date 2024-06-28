<?php
// Database configuration
$dbHost = 'mysql'; // Hostname or IP address of the MySQL server (service name in Docker Compose)
$dbUsername = 'chatuser'; // MySQL username
$dbPassword = 'chatpassword'; // MySQL password
$dbName = 'chatapp'; // Name of the database

// Create database connection
$db = new mysqli($dbHost, $dbUsername, $dbPassword, $dbName);

// Check connection
if ($db->connect_error) {
    die("Connection failed: " . $db->connect_error);
}
?>
