document.addEventListener("DOMContentLoaded", function () {

    const analyzeBtn = document.getElementById("analyzeBtn");
    const resultBox = document.getElementById("predictionResult");

    analyzeBtn.addEventListener("click", async function () {

        const data = {
            type: document.getElementById("transactionType").value,
            amount: parseFloat(document.getElementById("amount").value),
            oldbalanceOrg: parseFloat(document.getElementById("oldbalanceOrg").value),
            newbalanceOrig: parseFloat(document.getElementById("newbalanceOrig").value),
            oldbalanceDest: parseFloat(document.getElementById("oldbalanceDest").value)
        };

        // Check input values
        if (
            isNaN(data.amount) ||
            isNaN(data.oldbalanceOrg) ||
            isNaN(data.newbalanceOrig) ||
            isNaN(data.oldbalanceDest)
        ) {
            resultBox.style.display = "block";
            resultBox.innerHTML = "Please enter all transaction values.";
            return;
        }

        // Show processing message
        resultBox.style.display = "block";
        resultBox.innerHTML = "Analyzing transaction...";

        try {

            const response = await fetch("/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (!response.ok) {
                resultBox.innerHTML =
                    "Prediction Error: " + result.error;
                return;
            }

            // Display prediction
            resultBox.innerHTML =
                "<strong>Prediction:</strong> " + result.result;

        } catch (error) {

            console.error(error);

            resultBox.style.display = "block";
            resultBox.innerHTML =
                "Unable to connect to the ML backend.";

        }

    });

});
