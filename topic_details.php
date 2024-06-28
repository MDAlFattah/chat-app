<?php
include_once 'db.php';

// Check if the topic is provided in the URL parameters
if (isset($_GET['topic'])) {
    $topic = $_GET['topic'];

    // Function to fetch new messages from the server
    function fetchNewMessages() {
        global $db, $topic;
        $query = "SELECT sender, message, timestamp FROM $topic ORDER BY timestamp ASC";
        $result = $db->query($query);
        $messages = [];
        if ($result->num_rows > 0) {
            while ($row = $result->fetch_assoc()) {
                $messages[] = $row;
            }
        }
        return $messages;
    }

    // Display messages
    function displayMessages() {
        $messages = fetchNewMessages();
        if (!empty($messages)) {
            echo '<div class="messages-container">';
            echo '<h2 class="messages-heading">Messages</h2>';
            echo '<table>';
            echo '<tr><th>Sender</th><th>Message</th><th>Timestamp</th></tr>';
            foreach ($messages as $message) {
                echo '<tr>';
                echo '<td>' . htmlspecialchars($message['sender']) . '</td>';
                echo '<td>' . htmlspecialchars($message['message']) . '</td>';
                echo '<td>' . htmlspecialchars($message['timestamp']) . '</td>';
                echo '</tr>';
            }
            echo '</table>';
            echo '</div>';
        } else {
            echo '<p>No messages available</p>';
        }
    }

    // Insert new message if form is submitted
    if (isset($_POST['submit'])) {
        $sender = $_POST['sender'];
        $message = $_POST['message'];

        // Prepare the SQL statement with parameter placeholders
        $query = "INSERT INTO $topic (sender, message) VALUES (?, ?)";
        $stmt = $db->prepare($query);

        if ($stmt) {
            // Bind parameters to the prepared statement
            $stmt->bind_param("ss", $sender, $message);

            // Execute the statement
            if ($stmt->execute()) {
                // Redirect to a different URL to prevent form resubmission
                header('Location: topic_details.php?topic=' . urlencode($topic));
                exit(); // Ensure that no further code is executed after redirection
            } else {
                echo "Error: " . $stmt->error;
            }
        } else {
            echo "Error preparing statement: " . $db->error;
        }
    }
} else {
    // If topic is not found
    echo '<p>Topic not found</p>';
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Topic Details</title>
    <link rel="stylesheet" href="css/topic_details.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <div class="chat-container">
        <?php if (isset($topic)) displayMessages(); ?>

        <!-- Chat form section -->
        <div class="chat-form">
            <form id="message-form" method="post" action="">
                <input type="text" name="sender" placeholder="Your Name">
                <textarea name="message" placeholder="Type your message"></textarea>
                <button type="submit" name="submit">Send</button>
            </form>
        </div>

        <!-- Back button -->
        <div class="back-button-container" style="margin-top: 20px; text-align: center;">
            <a href="index.php" class="back-button" style="display: inline-block; margin: 10px auto; padding: 10px 20px; background-color: #337ab7; color: #fff; text-decoration: none; border-radius: 5px;">Back to Home</a>
        </div>
    </div>

    <!-- Script for periodic updates -->
    <script>
        function fetchAndDisplayMessages() {
            $.ajax({
                url: 'topic_details.php?topic=<?php echo isset($topic) ? $topic : ''; ?>',
                type: 'GET',
                dataType: 'html',
                success: function(response) {
                    $('.messages-container').html($(response).find('.messages-container').html());
                },
                error: function(xhr, status, error) {
                    console.error('Error fetching new messages:', error);
                }
            });
        }

        // Periodically fetch and update messages every 3 seconds
        setInterval(fetchAndDisplayMessages, 3000);
    </script>
</body>
</html>
