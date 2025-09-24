document.addEventListener('DOMContentLoaded', () => {
    const llmForm = document.getElementById('llm-form');
    llmForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const requestData = Object.fromEntries(formData.entries());

        const resultContainer = document.getElementById('result-container');
        const resultText = document.getElementById('result-text');
        const errorMessage = document.getElementById('error-message');
        const spinner = document.getElementById('spinner');
        const submitBtn = document.getElementById('submit-btn');

        resultContainer.classList.remove('hidden');
        resultText.textContent = '';
        errorMessage.classList.add('hidden');
        spinner.classList.remove('hidden');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Düşünülüyor...';

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP hatası! Durum: ${response.status}`);
            }

            const data = await response.json();
            resultText.textContent = data.text;
            
        } catch (error) {
            console.error('LLM isteği hatası:', error);
            errorMessage.textContent = `Hata: ${error.message}`;
            errorMessage.classList.remove('hidden');
        } finally {
            spinner.classList.add('hidden');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Yanıt Üret';
        }
    });
});