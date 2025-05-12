// frontend/static/frontend/js/product-animations.js
class ProductAnimations {
    constructor() {
        this.init();
    }

    init() {
        this.setupProductCards();
        this.setupFilterAnimations();
        this.setupAddToCartAnimation();
        this.setupImageEffects();
    }

    setupProductCards() {
        gsap.utils.toArray('.product-card').forEach((card, index) => {
            gsap.from(card, {
                opacity: 0,
                y: 50,
                scale: 0.95,
                duration: 0.8,
                delay: index * 0.1,
                ease: 'power3.out',
                scrollTrigger: {
                    trigger: card,
                    start: 'top 90%',
                    end: 'bottom 70%',
                    toggleActions: 'play none none reverse'
                }
            });
        });
    }

    setupFilterAnimations() {
        const filters = document.querySelectorAll('.category-card');
        filters.forEach((filter, index) => {
            gsap.from(filter, {
                opacity: 0,
                x: -30,
                duration: 0.6,
                delay: index * 0.1,
                ease: 'power2.out'
            });
        });
    }

    setupAddToCartAnimation() {
        const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
        addToCartButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.animateAddToCart(button);
            });
        });
    }

    animateAddToCart(button) {
        const cart = document.querySelector('.cart-badge');
        if (!cart) return;

        // Create flying product
        const productCard = button.closest('.product-card');
        const productImage = productCard.querySelector('.product-image img');
        const flyingItem = productImage.cloneNode(true);
        
        // Style the flying item
        Object.assign(flyingItem.style, {
            position: 'fixed',
            width: '80px',
            height: '80px',
            objectFit: 'cover',
            borderRadius: '50%',
            zIndex: '9999',
            transition: 'all 1s cubic-bezier(0.4, 0, 0.2, 1)',
            pointerEvents: 'none'
        });

        // Set initial position
        const rect = productImage.getBoundingClientRect();
        flyingItem.style.left = rect.left + 'px';
        flyingItem.style.top = rect.top + 'px';
        
        document.body.appendChild(flyingItem);

        // Animate to cart
        const cartRect = cart.getBoundingClientRect();
        
        setTimeout(() => {
            flyingItem.style.left = cartRect.left + 'px';
            flyingItem.style.top = cartRect.top + 'px';
            flyingItem.style.transform = 'scale(0.1)';
            flyingItem.style.opacity = '0';
        }, 50);

        // Remove after animation
        setTimeout(() => {
            flyingItem.remove();
            
            // Update cart badge
            const currentCount = parseInt(cart.textContent) || 0;
            cart.textContent = currentCount + 1;
            
            // Cart shake effect
            gsap.to(cart, {
                scale: 1.3,
                duration: 0.2,
                ease: 'power2.out',
                yoyo: true,
                repeat: 1
            });
        }, 1050);

        // Button success state
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="bi bi-check-circle me-1"></i> Added!';
        button.classList.add('btn-success');
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.classList.remove('btn-success');
        }, 2000);
    }

    setupImageEffects() {
        const images = document.querySelectorAll('.product-image img');
        images.forEach(img => {
            const card = img.closest('.product-card');
            
            card.addEventListener('mouseenter', () => {
                gsap.to(img, {
                    scale: 1.1,
                    duration: 0.5,
                    ease: 'power2.out'
                });
            });
            
            card.addEventListener('mouseleave', () => {
                gsap.to(img, {
                    scale: 1,
                    duration: 0.5,
                    ease: 'power2.out'
                });
            });
        });
    }
}

// Initialize product animations
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.products-section')) {
        new ProductAnimations();
    }
});