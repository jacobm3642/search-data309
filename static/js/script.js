document.addEventListener("DOMContentLoaded", function () {
    const queryInput = document.getElementById("query");
    const sendBtn = document.getElementById("sendBtn");
    const topkSelect = document.getElementById("topk");
    const resultsDiv = document.getElementById("results");

    function displayResults(results) {
        resultsDiv.innerHTML = "";

        if (!results.length) {
            resultsDiv.innerHTML = "<p style='color:#888;text-align:center;'>No results found.</p>";
            return;
        }

        results.forEach(item => {
            const card = document.createElement("div");
            card.style.cssText = "background:#fff; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.1); padding:15px; margin-bottom:15px;";

            card.innerHTML = `
                <h3 style="margin:0; color:#4f46e5;">${item.title}</h3>
                <p style="margin:5px 0; font-size:14px; color:#555;">
                    ${item.author} • ${item.year}
                </p>
                <p style="margin:10px 0; font-size:15px;">${item.abstract}</p>
                <p>
                    <a href="${item.link}" target="_blank" style="color:#2563eb; text-decoration:underline;">
                        View Original Paper
                    </a>
                </p>
                <span style="display:inline-block; padding:5px 10px; background:#e0e7ff; color:#1e3a8a; border-radius:6px; font-size:13px;">
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

        resultsDiv.innerHTML = "<p style='color:#666;text-align:center;'>Searching...</p>";

        fetch("/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: queryText, topk: topk })
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    resultsDiv.innerHTML = `<p style='color:red;text-align:center;'>${data.error}</p>`;
                } else {
                    displayResults(data.results || []);
                }
            })
            .catch(() => {
                resultsDiv.innerHTML = "<p style='color:red;text-align:center;'>Server error. Please try again.</p>";
            });
    }

    sendBtn.addEventListener("click", sendQuery);
    queryInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendQuery();
        }
    });
});
