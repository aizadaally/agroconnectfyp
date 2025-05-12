// frontend/static/frontend/js/dashboard-animations.js
class DashboardAnimations {
    constructor() {
        this.init();
    }

    init() {
        this.setupHeroAnimation();
        this.setupStatsAnimation();
        this.setupTableAnimations();
        this.setupCardHovers();
    }

    setupHeroAnimation() {
        gsap.timeline({ delay: 0.3 })
            .from('.dashboard-title', { 
                opacity: 0, 
                y: 50, 
                duration: 1, 
                ease: 'power3.out' 
            })
            .from('.dashboard-subtitle', { 
                opacity: 0, 
                y: 30, 
                duration: 0.8, 
                ease: 'power3.out' 
            }, '-=0.5')
            .from('.dashboard-action-btn', { 
                opacity: 0, 
                scale: 0.9, 
                duration: 0.6, 
                ease: 'back.out(1.7)' 
            }, '-=0.3');
    }

    setupStatsAnimation() {
        gsap.utils.toArray('.stat-card').forEach((card, index) => {
            gsap.from(card, {
                opacity: 0,
                y: 60,
                duration: 0.8,
                delay: index * 0.2,
                ease: 'power3.out',
                scrollTrigger: {
                    trigger: card,
                    start: 'top 90%',
                    end: 'bottom 70%',
                    toggleActions: 'play none none reverse'
                }
            });
        });

        // Animate counter numbers
        this.animateCounters();
    }

    animateCounters() {
        const counters = document.querySelectorAll('.stat-value');
        counters.forEach(counter => {
            const target = +counter.innerText.replace(/\D/g, '');
            const speed = target > 1000 ? 20 : 100; // Adjust speed based on value
            let current = 0;
            
            const updateCount = setInterval(() => {
                const increment = target / speed;
                current += increment;
                
                if (current >= target) {
                    counter.innerText = target.toLocaleString();
                    clearInterval(updateCount);
                } else {
                    counter.innerText = Math.ceil(current).toLocaleString();
                }
            }, 20);
        });
    }

    setupTableAnimations() {
        gsap.utils.toArray('.table tbody tr').forEach((row, index) => {
            gsap.from(row, {
                opacity: 0,
                x: -30,
                duration: 0.5,
                delay: index * 0.1,
                ease: 'power2.out',
                scrollTrigger: {
                    trigger: row,
                    start: 'top 95%',
                    end: 'bottom 85%',
                    toggleActions: 'play none none reverse'
                }
            });
        });
    }

    setupCardHovers() {
        const cards = document.querySelectorAll('.product-card, .stat-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                gsap.to(card, {
                    y: -8,
                    boxShadow: '0 8px 30px rgba(0,0,0,0.12)',
                    duration: 0.3,
                    ease: 'power2.out'
                });
            });

            card.addEventListener('mouseleave', () => {
                gsap.to(card, {
                    y: 0,
                    boxShadow: '0 4px 20px rgba(0,0,0,0.05)',
                    duration: 0.3,
                    ease: 'power2.out'
                });
            });
        });
    }
}

// Initialize dashboard animations
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.dashboard-hero')) {
        new DashboardAnimations();
    }
});