// Подключаем header, nav, footer
Promise.all([
    fetch('includes/header.html').then(r => r.text()),
    fetch('includes/nav.html').then(r => r.text()),
    fetch('includes/footer.html').then(r => r.text())
]).then(([headerHtml, navHtml, footerHtml]) => {
    document.getElementById('header-placeholder').innerHTML = headerHtml;
    document.getElementById('nav-placeholder').innerHTML = navHtml;
    document.getElementById('footer-placeholder').innerHTML = footerHtml;

    // Подсветка активной вкладки
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const tabs = document.querySelectorAll('.tab a');

    tabs.forEach(tab => {
        const tabHref = tab.getAttribute('href').replace(/^\//, '').split('/').pop() || 'index.html';
        if (tabHref === currentPage) {
            tab.parentElement.classList.add('active');
        } else {
            tab.parentElement.classList.remove('active');
        }
    });

    // Проверка сохранённой темы при загрузке
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
    document.body.classList.add('light-theme');
    const btn = document.querySelector('.btn-secondary');
    if (btn) btn.innerHTML = '<i class="fas fa-sun"></i> Тема';
    }
});

// Переключение темы
function toggleTheme() {
    const body = document.body;
    const btn = document.querySelector('.btn-secondary i');

    if (body.classList.contains('light-theme')) {
        body.classList.remove('light-theme');
        btn.classList.remove('fa-sun');
        btn.classList.add('fa-moon');
        document.querySelector('.btn-secondary').innerHTML = '<i class="fas fa-moon"></i> Тема';
        localStorage.setItem('theme', 'dark');
    } else {
        body.classList.add('light-theme');
        btn.classList.remove('fa-moon');
        btn.classList.add('fa-sun');
        document.querySelector('.btn-secondary').innerHTML = '<i class="fas fa-sun"></i> Тема';
        localStorage.setItem('theme', 'light');
    }
}
