document.getElementById('uploadForm').addEventListener('submit', function (event) {
    event.preventDefault();

    var fileInput = document.getElementById('codeFile');
    var file = fileInput.files[0];

    if (file) {
        var formData = new FormData();
        formData.append('codeFile', file);

        // Show loading spinner while waiting for the analysis
        showLoadingSpinner();

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/analyze', true);

        xhr.onload = function () {
            // Hide loading spinner once analysis is complete
            hideLoadingSpinner();

            if (xhr.status === 200) {
                try {
                    var result = JSON.parse(xhr.responseText);

                    // Display the result on the web page
                    displayResult(result.message);
                } catch (error) {
                    console.error('Error parsing JSON:', error);

                    // Display an error message on the web page
                    displayResult('An error occurred during analysis.');
                }
            } else {
                // Handle errors
                console.error('Error:', xhr.status, xhr.statusText);

                // Display an error message on the web page
                displayResult('An error occurred during analysis.');
            }
        };

        // Additional error handling for the request
        xhr.onerror = function () {
            console.error('An error occurred during the request.');
            hideLoadingSpinner();
            displayResult('An error occurred during the analysis.');
        };

        // Set a timeout for the request (in milliseconds)
        xhr.timeout = 30000; // Adjust the timeout value as needed

        // Additional timeout handling
        xhr.ontimeout = function () {
            console.error('Request timed out.');
            hideLoadingSpinner();
            displayResult('The analysis process took too long. Please try again.');
        };

        xhr.send(formData);
    }
});

function showLoadingSpinner() {
    // Create and append a loading spinner to the result container
    var spinner = document.createElement('div');
    spinner.className = 'loading-spinner';
    document.getElementById('result').appendChild(spinner);
}

function hideLoadingSpinner() {
    // Remove the loading spinner from the result container
    var spinner = document.querySelector('.loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

function displayResult(message) {
    // Clear previous results
    document.getElementById('result').innerHTML = '';

    // Create a new element to display the result
    var resultElement = document.createElement('div');
    resultElement.className = 'result-container';
    resultElement.textContent = message;

    // Append the new result to the result container
    document.getElementById('result').appendChild(resultElement);
}
