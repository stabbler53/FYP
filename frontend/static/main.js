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

            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    try {
                        var result = JSON.parse(xhr.responseText);

                        if ('message' in result) {
                            // Display the result on the web page
                            displayResult(result);
                        } else if ('error' in result) {
                            // Display an error message on the web page
                            displayResult(result.error);
                        } else {
                            console.error('Unexpected response format:', result);
                            displayResult('An unexpected error occurred during analysis.');
                        }
                    } catch (error) {
                        console.error('Error parsing JSON:', error);

                        // Display an error message on the web page
                        displayResult('An error occurred during analysis.');
                    }
                } else {
                    // Handle unexpected status codes
                    console.error('Unexpected status code:', xhr.status);

                    // Log the response text for debugging purposes
                    console.log('Response text:', xhr.responseText);

                    // Display an error message on the web page
                    displayResult('An unexpected error occurred during analysis.');
                }
            }
        };

        // Additional error handling for the request
        xhr.onerror = function () {
            console.error('An error occurred during the request. Check the browser console for more details.');

            // Log additional details about the error
            console.log('XHR status:', xhr.status);
            console.log('XHR response:', xhr.responseText);

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

// ... (rest of the functions remain the same)

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

function displayResult(result) {
    // Clear previous results
    var resultContainer = document.getElementById('result');
    resultContainer.innerHTML = '';

    // Create a new element to display the result
    var resultElement = document.createElement('div');
    resultElement.className = 'result-container';

    // Display Pylint output
    var pylintOutputElement = document.createElement('div');
    pylintOutputElement.textContent = 'Pylint Output: ' + result.message;
    resultElement.appendChild(pylintOutputElement);

    // Display linting comments, if any
    if (result.linting_comments && result.linting_comments.length > 0) {
        var commentsElement = document.createElement('div');
        commentsElement.textContent = 'Linting Comments:';

        var commentsList = document.createElement('ul');
        result.linting_comments.forEach(function (comment) {
            var commentItem = document.createElement('li');
            commentItem.textContent = comment;
            commentsList.appendChild(commentItem);
        });

        commentsElement.appendChild(commentsList);
        resultElement.appendChild(commentsElement);
    } else {
        // Display a message when there are no linting comments
        var noCommentsElement = document.createElement('div');
        noCommentsElement.textContent = 'No linting comments.';
        resultElement.appendChild(noCommentsElement);
    }

    // Append the new result to the result container
    resultContainer.appendChild(resultElement);
}
