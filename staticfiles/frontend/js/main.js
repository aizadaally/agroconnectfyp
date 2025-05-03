// frontend/static/frontend/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Update cart badge when page loads
    updateCartBadge();
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Function to update cart badge
function updateCartBadge() {
    fetch('/api/orders/cart/')
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Failed to fetch cart');
        })
        .then(data => {
            const cartBadge = document.getElementById('cart-badge');
            if (cartBadge) {
                const itemCount = data.items ? data.items.reduce((count, item) => count + item.quantity, 0) : 0;
                cartBadge.textContent = itemCount;
            }
        })
        .catch(error => {
            console.error('Error updating cart badge:', error);
        });
}

// Function to add product to cart
function addToCart(productId, quantity = 1) {
    fetch('/api/orders/cart/')
        .then(response => response.json())
        .then(cart => {
            return fetch(`/api/orders/${cart.id}/add_item/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: quantity
                })
            });
        })
        .then(response => {
            if (response.ok) {
                showAlert('Product added to cart successfully!', 'success');
                updateCartBadge();
                return response.json();
            }
            throw new Error('Failed to add to cart');
        })
        .catch(error => {
            showAlert('Error adding product to cart', 'danger');
            console.error('Error:', error);
        });
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to display alert message
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertContainer.style.zIndex = 1050;
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.body.appendChild(alertContainer);
    
    // Auto dismiss after 3 seconds
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertContainer);
        bsAlert.close();
    }, 3000);
}