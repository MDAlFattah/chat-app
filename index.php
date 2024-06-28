<?php
include_once 'db.php';

if (isset($_POST['new_topic'])) {
    $new_topic = $_POST['new_topic'];
    
    // Create a new table for the topic
    $query = "CREATE TABLE IF NOT EXISTS $new_topic (
        id INT(11) AUTO_INCREMENT PRIMARY KEY,
        sender VARCHAR(255) NOT NULL,
        message TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )";

    if ($db->query($query) === TRUE) {
        echo "Table $new_topic created successfully";
    } else {
        echo "Error creating table: " . $db->error;
    }

    // Redirect to the same page after form submission
    header("Location: {$_SERVER['PHP_SELF']}");
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatApp</title>
    <link rel="stylesheet" href="css/index.css">
</head>
<body>
    <div class="chat-container">
        <h1 class="existing-chats">Existing Chats</h1>
        <h4 class="topics-heading">Topics</h4>
        <div class="topics-list">
            <?php
            $query = "SHOW TABLES";
            $result = $db->query($query);

            if ($result->num_rows > 0) {
                while ($row = $result->fetch_assoc()) {
                    echo '<div class="topic"><a href="topic_details.php?topic=' . urlencode($row['Tables_in_chatapp']) . '">' . $row['Tables_in_chatapp'] . '</a></div>';
                }
            } else {
                echo '<div class="topic">No topics available</div>';
            }
            ?>
        </div>

        <h4 class="new-chat-topic">New Chat Topic</h4>
        <div class="new-chat-input">
            <form method="post" action="">
                <input type="text" name="new_topic" id="new-chat-topic-input" placeholder="Enter new chat topic...">
                <button type="submit">Create</button>
            </form>
        </div>

    </div>
</body>
</html>
