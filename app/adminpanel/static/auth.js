// auth.js

// Функция для добавления заголовка Authorization к каждому запросу
function addAuthHeaderToFetch() {
    const originalFetch = window.fetch;
    
    window.fetch = function(url, options = {}) {
        const token = localStorage.getItem('access_token');  // Получаем токен JWT
        options.headers = options.headers || {};
        options.headers['Authorization'] = `Bearer ${'access_token'}`;  // Добавляем заголовок

        // Прокси функция вызова fetch с измененными заголовками
        return originalFetch(url, options);
    };
}

// Запуск функции после загрузки страницы
window.onload = addAuthHeaderToFetch;