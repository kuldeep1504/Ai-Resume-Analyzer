document.getElementById('analyzer-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const form = e.target;
    const btnText = document.getElementById('btn-text');
    const loader = document.getElementById('loader');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultsSection = document.getElementById('results-section');

    // UI Loading State
    btnText.textContent = "Analyzing...";
    loader.classList.remove('hidden');
    analyzeBtn.disabled = true;
    resultsSection.classList.add('hidden');

    try {
        const formData = new FormData(form);
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || "An error occurred during analysis.");
            throw new Error(data.error);
        }

        // Render Results
        renderResults(data);

    } catch (error) {
        console.error("Error analyzing resume:", error);
    } finally {
        // Reset UI State
        btnText.textContent = "Analyze Resume";
        loader.classList.add('hidden');
        analyzeBtn.disabled = false;
    }
});

function renderResults(data) {
    const resultsSection = document.getElementById('results-section');
    
    // Set Match Score
    const matchScoreSpan = document.getElementById('match-score');
    const scoreCircle = document.querySelector('.score-circle');
    
    matchScoreSpan.textContent = `${data.match_score}%`;
    scoreCircle.style.setProperty('--score', data.match_score);

    // Set Extracted Skills
    const extractedList = document.getElementById('extracted-skills');
    extractedList.innerHTML = '';
    if (data.extracted_skills.length > 0) {
        data.extracted_skills.forEach(skill => {
            const li = document.createElement('li');
            li.textContent = skill;
            extractedList.appendChild(li);
        });
    } else {
        extractedList.innerHTML = '<li>No technical skills explicitly identified.</li>';
    }

    // Set Missing Skills
    const missingList = document.getElementById('missing-skills');
    missingList.innerHTML = '';
    if (data.missing_skills.length > 0) {
        data.missing_skills.forEach(skill => {
            const li = document.createElement('li');
            li.textContent = skill;
            missingList.appendChild(li);
        });
    } else {
        missingList.innerHTML = '<li>You have all the required skills mentioned in the JD!</li>';
    }

    // Set Suggestions
    const suggestionsList = document.getElementById('suggestions-list');
    suggestionsList.innerHTML = '';
    data.suggestions.forEach(suggestion => {
        const li = document.createElement('li');
        li.textContent = suggestion;
        suggestionsList.appendChild(li);
    });

    // Show results
    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}
