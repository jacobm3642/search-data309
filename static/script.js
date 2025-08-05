$(document).ready(function () {

    // Function to add a chat message to the page
    function addMessage(text, sender = 'user') {
        const bubble = $('<div>')
            .addClass(`p-2 my-2 rounded ${sender === 'user' ? 'bg-primary text-white text-end' : 'bg-secondary text-white text-start'}`)
            .text(text);
        
        const row = $('<div>').addClass('row').append(bubble);
        $('#chat-container').append(row);

        // Auto-scroll to bottom
        $('#chat-container').scrollTop($('#chat-container')[0].scrollHeight);
    }

    // When "Send" button is clicked
    $('#send-btn').click(function () {
        const input = $('#user-input');
        const message = input.val().trim();

        if (message !== '') {
            addMessage(message, 'user');
            input.val('');

            // Simulate a reply from system after a short delay
            setTimeout(() => {
                addMessage("You said: " + message, 'system');
            }, 400);
        }
    });

    // Also allow pressing Enter key to send
    $('#user-input').on('keypress', function (e) {
        if (e.which === 13) {
            $('#send-btn').click();
        }
    });
});
