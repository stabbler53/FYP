// frontend/main.js
document.getElementById('uploadForm').addEventListener('submit', async function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        document.getElementById('result').innerHTML = `<p>${result.message}</p>`;
    } catch (error) {
        console.error('Error analyzing code:', error);
    }
});
