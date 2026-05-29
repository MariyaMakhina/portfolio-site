// Проверяем, соглашался ли пользователь уже
if (!localStorage.getItem('cookiesAccepted')) {
    // Создаём баннер
    const banner = document.createElement('div');
    banner.id = 'cookie-banner';
    banner.innerHTML = `
        <div class="cookie-glass">
            <p class="cookie-text">🍪 Мы используем cookies для улучшения работы сайта. Продолжая использовать сайт, вы соглашаетесь с этим.</p>
            <button id="accept-cookies" class="cookie-btn">Принять</button>
        </div>
    `;
    document.body.appendChild(banner);

    // Обработчик кнопки
    document.getElementById('accept-cookies').addEventListener('click', function() {
        localStorage.setItem('cookiesAccepted', 'true');
        banner.style.display = 'none';
    });
}