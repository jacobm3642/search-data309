document.addEventListener("DOMContentLoaded", function () {
    const queryInput = document.getElementById("query");
    const sendBtn = document.getElementById("sendBtn");
    const topkSelect = document.getElementById("topk");
    const resultsDiv = document.getElementById("results");

    function displayResults(results) {
        resultsDiv.innerHTML = "";

        if (!results.length) {
            resultsDiv.innerHTML = "<p class='no-results'>No results found.</p>";
            return;
        }

        results.forEach(item => {
            const card = document.createElement("div");
            card.className = "result-card";

            card.innerHTML = `
                <h3 class="result-title">${item.title}</h3>
                <p class="result-meta">
                    ${item.author} • ${item.year}
                </p>
                <p class="result-abstract">${item.abstract}</p>
                <p>
                    <a href="${item.link}" target="_blank" class="result-link">
                        View Original Paper
                    </a>
                </p>
                <span class="similarity-badge">
                    Similarity: ${item.similarity !== null ? item.similarity.toFixed(3) : "N/A"}
                </span>
            `;
            resultsDiv.appendChild(card);
        });
    }

    function sendQuery() {
        const queryText = queryInput.value.trim();
        const topk = parseInt(topkSelect.value, 10);

        if (queryText === "") return;

        resultsDiv.innerHTML = "<p class='searching'>Searching...</p>";

        fetch("/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: queryText, topk: topk })
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    resultsDiv.innerHTML = `<p class='error-msg'>${data.error}</p>`;
                } else {
                    displayResults(data.results || []);
                }
            })
            .catch(() => {
                resultsDiv.innerHTML = "<p class='error-msg'>Server error. Please try again.</p>";
            });
    }

    sendBtn.addEventListener("click", sendQuery);
    queryInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendQuery();
        }
    });
});
