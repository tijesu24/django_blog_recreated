
$(document).ready(function () {
    // Check if there are messages with ID "password-reset-messages"
    var messages = $('#password-reset-messages');
    if (messages.length > 0) {
        // Extract the first message text
        var messageText = messages.find('li.message:first-child').text();

        // Create the Bootstrap alert element
        var alertHtml = '<div class="alert alert-success alert-dismissible fade show" role="alert">'
            + messageText +
            '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
            + '</div>';

        // Append the alert element to the div with ID "alert-message"
        $('#alert-message').html(alertHtml);

        // Optionally, remove the message after a delay
        setTimeout(function () {
            $('.alert').alert('close');
        }, 8000); // 5000 milliseconds (5 seconds) delay before closing the alert
    }


    // Optionally, remove the message after displaying the alert
    messages.remove();
});


