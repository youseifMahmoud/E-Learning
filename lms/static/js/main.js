document.addEventListener('DOMContentLoaded', function () {
    console.log('Custom JS loaded!');
});

// Replace with your actual API key from newsapi.org
const apiKey = '7bc5819029f640ca8b6ba28158a090c1';
const newsContainer = document.querySelector('.news-grid');

// Fetch the latest news
async function fetchNews() {
    const url = `https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=${apiKey}`;
    
    try {
        const response = await fetch(url);
        const data = await response.json();

        if (data.status === "ok") {
            displayNews(data.articles.slice(0, 3)); // Limit to 3 articles
        } else {
            console.error("Error fetching news:", data.message);
        }
    } catch (error) {
        console.error("Network error:", error);
    }
}

// Function to display the news articles on the website
function displayNews(articles) {
    // Clear the container first
    newsContainer.innerHTML = '';

    // Loop through each article and create the HTML structure for each news item
    articles.forEach(article => {
        const newsItem = document.createElement('div');
        newsItem.classList.add('news-item');

        // Create HTML structure for the news item
        newsItem.innerHTML = `
            <img src="${article.urlToImage || 'placeholder.jpg'}" alt="News Image">
            <h3>${article.title}</h3>
            <p>${article.description || 'No description available.'}</p>
            <a href="${article.url}" target="_blank">Read More</a>
        `;

        // Append the news item to the news grid
        newsContainer.appendChild(newsItem);
    });
}

// Call the fetchNews function when the page loads
window.onload = fetchNews;

// ============================================================

const saveButton = document.querySelector('.save-btn');
const card = saveButton.closest('.card');

saveButton.addEventListener('click', () => {
  card.classList.toggle('saved');
});

// لتفعيل أو تعطيل حساب المعلم
document.getElementById('activateSwitch').addEventListener('change', function() {
    if (this.checked) {
        alert('Teacher account activated!');
    } else {
        alert('Teacher account deactivated.');
    }
});

// شيفرة للتفاعل مع عناصر معينة إذا لزم الأمر
$(document).ready(function() {
    console.log("Ready!");
    // يمكن إضافة أحداث إضافية هنا إذا احتاج المشروع
});

// البحث عن معلم في البطاقات
document.querySelector('.input-group button').addEventListener('click', function() {
    const searchQuery = document.querySelector('.input-group input').value.toLowerCase();
    const cards = document.querySelectorAll('.teacher-card');

    cards.forEach(card => {
        const teacherName = card.querySelector('.card-title').innerText.toLowerCase();
        if (teacherName.includes(searchQuery)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});

// تفعيل الـ tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

