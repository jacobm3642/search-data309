document.addEventListener("DOMContentLoaded", function () {
    const queryInput = document.getElementById("query");
    const sendBtn = document.getElementById("sendBtn");
    const topkSelect = document.getElementById("topk");
    const resultsDiv = document.getElementById("results");

    function displayResults(results) {
        resultsDiv.innerHTML = "";

        if (!results.length) {
            resultsDiv.innerHTML = "<p class='placeholder'>No results found.</p>";
            return;
        }

        // Sort by similarity descending; nulls at the end
        results.sort((a, b) => {
            if (a.similarity == null && b.similarity == null) return 0;
            if (a.similarity == null) return 1;
            if (b.similarity == null) return -1;
            return b.similarity - a.similarity;
        });

        results.forEach(item => {
            const card = document.createElement("div");
            card.className = "result-card";

            card.innerHTML = `
                <h3 class="result-title">
                    <a href="${item.arxiv_url}" target="_blank">${item.title}</a>
                </h3>
                <p class="result-meta">Category: ${item.category} • Published: ${item.date_published}</p>
                <p class="result-abstract">${item.abstract}</p>
                <p class="result-keywords"><strong>Keywords:</strong> ${item.keyword}</p>
                <div class="result-links">
                    ${item.pdf_url ? `<a href="${item.pdf_url}" target="_blank" class="pdf-btn">📄 View PDF</a>` : ""}
                </div>
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

        if (!queryText) return;

        resultsDiv.innerHTML = "<p class='placeholder'>Searching...</p>";

        fetch("/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: queryText, topk: topk })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultsDiv.innerHTML = `<p class='placeholder' style="color:red;">${data.error}</p>`;
            } else {
                displayResults(data.results || []);
            }
        })
        .catch(() => {
            resultsDiv.innerHTML = "<p class='placeholder' style='color:red;'>Server error. Please try again.</p>";
        });
    }

    sendBtn.addEventListener("click", sendQuery);
    queryInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") sendQuery();
    });
});
