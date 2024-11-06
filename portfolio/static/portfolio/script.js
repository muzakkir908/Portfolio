document.querySelectorAll('nav a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const target = this.getAttribute('href');
        if (!target.startsWith('#')) return; // Allow default behavior for non-anchor links
        e.preventDefault();
        document.querySelector(target).scrollIntoView({
            behavior: 'smooth'
        });
    });
});