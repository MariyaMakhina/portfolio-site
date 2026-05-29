// Ждем загрузку DOM
$(document).ready(function() {
    console.log('Document ready');
    
    // Даем время на рендеринг блоков Wagtail
    setTimeout(function() {
        initCarousels();
    }, 100);
    
    // Инициализация остальных функций
    initBookingForm();
    initActiveMenu();
    initStickyHeader();
    initSmoothScroll();
});

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// ========== КАРУСЕЛИ ==========
function initCarousels() {
    console.log('Initializing carousels');
    
    // Карусель меню
    if ($('.menu-carousel').length > 0) {
        console.log('Menu carousel found, slides:', $('.menu-carousel .menu-slide').length);
        
        if ($('.menu-carousel .menu-slide').length > 0) {
            $('.menu-carousel .menu-slide').css({
                'display': 'block',
                'visibility': 'visible',
                'opacity': '1'
            });
            
            $('.menu-carousel').slick({
                dots: true,
                infinite: true,
                speed: 500,
                slidesToShow: 1,
                slidesToScroll: 1,
                autoplay: false,
                arrows: true,
                swipe: true,
                adaptiveHeight: true,
                prevArrow: '<button type="button" class="slick-prev slick-light"></button>',
                nextArrow: '<button type="button" class="slick-next slick-light"></button>'
            });
        }
    }
    
    // Карусель галереи
    if ($('.gallery-carousel').length > 0) {
        console.log('Gallery carousel found, slides:', $('.gallery-carousel .gallery-slide').length);
        
        if ($('.gallery-carousel .gallery-slide').length > 1) {
            $('.gallery-carousel').slick({
                dots: true,
                infinite: true,
                speed: 500,
                slidesToShow: 1,
                slidesToScroll: 1,
                // autoplay: true,
                // autoplaySpeed: 5000,
                arrows: true,
                swipe: true,
                adaptiveHeight: true,
                prevArrow: '<button type="button" class="slick-prev slick-dark"></button>',
                nextArrow: '<button type="button" class="slick-next slick-dark"></button>'
            });
        }
    }
}

// ========== ФОРМА БРОНИРОВАНИЯ С ДИАЛОГОМ ==========
// ========== ФОРМА БРОНИРОВАНИЯ С ДИАЛОГОМ ==========
function initBookingForm() {
    const form = document.getElementById('booking-form');
    if (!form) return;
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        submitBtn.disabled = true;
        submitBtn.textContent = 'Отправка...';
        
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Берем сообщение из data-атрибута формы
                const successMessage = form.dataset.successMessage || 'Спасибо! Ваша заявка принята.';
                showDialog('success', successMessage);
                
                // Очищаем форму
                form.reset();
                
                // Убираем возможные старые ошибки
                const oldError = form.querySelector('.alert-error');
                if (oldError) oldError.remove();
                
            } else {
                // Показываем ошибки в диалоге
                const errorMessage = data.errors ? data.errors.join('\n') : (data.message || 'Произошла ошибка');
                showDialog('error', errorMessage);
                
                // Возвращаем кнопку в исходное состояние
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }
        } catch (error) {
            console.error('Error:', error);
            showDialog('error', 'Произошла ошибка при отправке. Попробуйте позже.');
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    });
}

// ========== ДИАЛОГОВОЕ ОКНО ==========
function showDialog(type, message) {
    // Удаляем предыдущий диалог, если был
    const oldDialog = document.getElementById('message-dialog');
    if (oldDialog) oldDialog.remove();
    
    // Создаем новое диалоговое окно
    const dialog = document.createElement('dialog');
    dialog.id = 'message-dialog';
    dialog.className = 'dialog-form';
    
    // Определяем заголовок и иконку
    let title = '';
    let icon = '';
    
    if (type === 'success') {
        title = 'Успешно!';
        icon = '✓';
    } else if (type === 'error') {
        title = 'Ошибка!';
        icon = '✗';
    } else {
        title = 'Сообщение';
        icon = 'ℹ';
    }
    
    // Формируем HTML диалога
    dialog.innerHTML = `
        <div class="dialog-content ${type}">
            <div class="dialog-header">
                <span class="dialog-icon">${icon}</span>
                <h2 class="dialog-title">${title}</h2>
                <button class="dialog-close" onclick="this.closest('dialog').close()">✕</button>
            </div>
            <div class="dialog-body">
                <p>${message.replace(/\n/g, '<br>')}</p>
            </div>
            <div class="dialog-footer">
                <button class="dialog-button" onclick="this.closest('dialog').close()">OK</button>
            </div>
        </div>
    `;
    
    // Добавляем в DOM
    document.body.appendChild(dialog);
    
    // Показываем диалог
    dialog.showModal();
    
    // Закрытие по клику вне диалога
    dialog.addEventListener('click', function(e) {
        const dialogDimensions = dialog.getBoundingClientRect();
        if (
            e.clientX < dialogDimensions.left ||
            e.clientX > dialogDimensions.right ||
            e.clientY < dialogDimensions.top ||
            e.clientY > dialogDimensions.bottom
        ) {
            dialog.close();
        }
    });
    
    // Закрытие по Escape (работает автоматически)
}

// ========== АКТИВНОЕ МЕНЮ ==========
function initActiveMenu() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    const mobileIcons = document.querySelectorAll('.mobile-icon');
    const allLinks = [...navLinks, ...mobileIcons];
    
    if (sections.length === 0 || allLinks.length === 0) return;
    
    function updateActiveMenu() {
        let current = '';
        const scrollY = window.scrollY;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 150;
            const sectionBottom = sectionTop + section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollY >= sectionTop && scrollY < sectionBottom - 100) {
                current = sectionId;
            }
            
            if (scrollY < 200) {
                current = 'section-hero';
            }
        });
        
        allLinks.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href').replace('#', '');
            if (href === current) {
                link.classList.add('active');
            }
        });
    }
    
    updateActiveMenu();
    window.addEventListener('scroll', updateActiveMenu);
}

// ========== ЛИПКИЙ ХЕДЕР ==========
function initStickyHeader() {
    console.log('Initializing sticky header');
    const header = document.querySelector('header');
    
    if (header) {
        console.log('Header found:', header);
        
        function checkScroll() {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
                console.log('Added scrolled class');
            } else {
                header.classList.remove('scrolled');
                console.log('Removed scrolled class');
            }
        }
        
        // Проверяем при загрузке
        checkScroll();
        
        // Проверяем при скролле
        window.addEventListener('scroll', checkScroll);
    } else {
        console.log('Header not found!');
    }
}


// ========== ОБРАБОТКА ИЗМЕНЕНИЯ РАЗМЕРА ЭКРАНА ==========
$(window).on('resize', function() {
    if ($('.menu-carousel').hasClass('slick-initialized')) {
        $('.menu-carousel').slick('resize');
    }
    if ($('.gallery-carousel').hasClass('slick-initialized')) {
        $('.gallery-carousel').slick('resize');
    }
});