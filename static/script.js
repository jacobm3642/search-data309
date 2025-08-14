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

    // Function to display search results returned by Pinecone or your backend
    function displayResults(results) {
        results.forEach(item => {
            let resultCard = `
                <div class="card my-2">
                    <div class="card-body">
                        <h5 class="card-title">${item.title || "Untitled"}</h5>
                        <p class="card-text">${item.snippet || item.query || "No description available."}</p>
                    </div>
                </div>
            `;
            $('#chat-container').append(resultCard);
        });
    }

    // Handle Send button click
    $('#send-btn').click(function () {
        const input = $('#user-input');
        const message = input.val().trim();
        if (message === '') return;

        // Add user message to chat
        addMessage(message, 'user');
        input.val('');

        // Create JSON payload
        let jsonData = {
            id: Date.now().toString(),       
            metadata: { query: message } 
        };

        // Send JSON to Pinecone
        $.ajax({
            url: "/send-query", 
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(jsonData),
            success: function (response) {
                displayResults(response.results || []);
            },
            error: function (xhr, status, error) {
                console.error("Error sending query:", error);
                addMessage("Error sending query.", 'system');
            }
        });
    });

    // Also allow Enter key to send
    $('#user-input').on('keypress', function (e) {
        if (e.which === 13) {
            $('#send-btn').click();
        }
    });

});
