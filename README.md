# ChatApp

ChatApp is a simple web application that allows users to create chat topics and exchange messages in real-time.

## Features

- **Create New Chat Topics:** Users can create new chat topics by entering a topic name.
- **Join Existing Chat Topics:** Users can join existing chat topics by clicking on the topic links.
- **Exchange Messages:** Users can send and receive messages within the selected chat topic without page reloads.
- **Real-Time Updates:** Messages are updated in real-time using AJAX, providing a seamless user experience.
- **Prevent Resubmission:** Form submissions are prevented from resubmission on page refreshes to avoid duplicate entries.

## Technologies Used

- **PHP:** Backend scripting language for server-side logic and database interaction.
- **MySQL:** Relational database management system for storing chat topics and messages.
- **HTML/CSS:** Frontend markup and styling for the user interface.
- **JavaScript:** Used for client-side scripting and AJAX requests to fetch and display new messages.

## Installation
Clone the Repository
Clone the ChatApp repository to your local machine:

**bash**
Copy code
git clone https://github.com/your-username/ChatApp.git

**Import Database**
Import the provided chatapp.sql file into your MySQL database management system.

**Configure Database Connection**
Update the database connection details in the db.php file with your MySQL credentials:

**Use the DB configuration:**

$host = 'localhost';
$username = 'root';
$password = 'your-password';
$database = 'chatapp';
Host the Application
Host the project on a PHP-enabled web server like Apache or Nginx. You can use tools like XAMPP or WAMP for local development.

Access the Application
Access the application through your web browser using the URL where it's hosted. You'll see the ChatApp homepage with options to create new chat topics and join existing ones.