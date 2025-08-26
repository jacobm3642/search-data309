$(document).ready(function () {

    // Add a chat bubble to the UI
    function addMessage(text, sender = 'user') {
        const bubble = $('<div>')
            .addClass(`p-2 my-2 rounded ${sender === 'user' ? 'bg-primary text-white text-end' : 'bg-secondary text-white text-start'}`)
            .text(text);
        
        const row = $('<div>').addClass('row').append(bubble);
        $('#chat-container').append(row);

        $('#chat-container').scrollTop($('#chat-container')[0].scrollHeight);
    }

    // Display search results returned from backend
    function displayResults(results) {
        results.forEach(item => {
            let resultCard = `
                <div class="card my-2">
                    <div class="card-body">
                        <h5 class="card-title">${item.title || "Untitled"}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">
                            ${item.author || "Unknown author"} • ${item.year || "N/A"}
                        </h6>
                        <p class="card-text">${item.abstract || "No abstract available."}</p>
                        <span class="badge bg-info text-dark">
                            Similarity: ${item.similarity ?? "N/A"}
                        </span>
                    </div>
                </div>
            `;
            $('#chat-container').append(resultCard);
        });

        // Auto-scroll to bottom
        $('#chat-container').scrollTop($('#chat-container')[0].scrollHeight);
    }

    // Handle Send button / Enter key
    $('#search-form').submit(function (event) {
        event.preventDefault();

        const input = $('#user-input');
        const message = input.val().trim();
        if (message === '') return;

        // Add user message to chat
        addMessage(message, 'user');
        input.val('');

        // === MOCK DATA FOR TESTING ===
        const dummyResults = [
            {
                title: "Understanding AI",
                author: "Alice Smith",
                year: 2021,
                abstract: "An overview of artificial intelligence concepts and methods.",
                similarity: 0.95
            },
            {
                title: "Deep Learning in Practice",
                author: "Bob Johnson",
                year: 2022,
                abstract: "Practical applications of deep learning in real-world scenarios.",
                similarity: 0.92
            },
            {
                title: "Natural Language Processing Basics",
                author: "Carol Lee",
                year: 2020,
                abstract: "Introduction to NLP techniques for text analysis.",
                similarity: 0.89
            }
        ];

        // Display mock results instead of calling backend
        displayResults(dummyResults);

        // === END MOCK DATA ===
    });

});

//         // Create JSON payload for backend
//         const jsonData = { query: message };

//         // Send JSON to Flask endpoint
//         $.ajax({
//             url: "/search",
//             type: "POST",
//             contentType: "application/json",
//             data: JSON.stringify(jsonData),
//             success: function (response) {
//                 displayResults(response.results || []);
//             },
//             error: function () {
//                 addMessage("Error communicating with server.", 'system');
//             }
//         });
//     });

// });
