document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var file = document.getElementById('codeFile').files[0];

    if (file) {
        var formData = new FormData();
        formData.append('codeFile', file);

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/analyze', true);  // Change the endpoint to '/analyze'

        xhr.onload = function() {
            if (xhr.status === 200) {
                var result = JSON.parse(xhr.responseText);
                // Display the result on the web page
                document.getElementById('result').innerHTML = result.message;  // Access 'message' property
            } else {
                // Handle errors
                console.error('Error:', xhr.status, xhr.statusText);
            }
        };

        xhr.send(formData);
    }
});
