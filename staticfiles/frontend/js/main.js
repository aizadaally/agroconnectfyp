// frontend/static/frontend/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    // Update cart badge when page loads
    updateCartBadge();
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize animated elements
    initAnimations();
    
    // Add loading indicators to forms
    initFormLoading();
    
    // Initialize copy buttons
    initCopyButtons();
    
    // Initialize category filters
    initCategoryFilters();
    
    // Initialize quantity selectors
    initQuantitySelectors();
    
    // Initialize delivery area selection in checkout
    initDeliveryAreaSelection();
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
    showLoading();
    
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
            hideLoading();
            if (response.ok) {
                showToast('Product added to cart successfully!', 'success');
                updateCartBadge();
                return response.json();
            }
            throw new Error('Failed to add to cart');
        })
        .catch(error => {
            hideLoading();
            showToast('Error adding product to cart', 'danger');
            console.error('Error:', error);
        });
}

// Function to add product to cart with specific quantity
function addToCartWithQuantity(productId) {
    const quantity = parseInt(document.getElementById('quantity').value) || 1;
    addToCart(productId, quantity);
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

// Toast notification system
function showToast(message, type = 'success') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type} show`;
    toast.innerHTML = `
        <div class="toast-header">
            <strong class="me-auto">${type === 'success' ? 'Success' : type === 'warning' ? 'Warning' : 'Error'}</strong>
            <button type="button" class="btn-close" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

// Loading indicators
function showLoading() {
    const loadingOverlay = document.createElement('div');
    loadingOverlay.className = 'loading-overlay';
    loadingOverlay.innerHTML = `
        <div class="loading-spinner"></div>
    `;
    document.body.appendChild(loadingOverlay);
    document.body.style.overflow = 'hidden';
}

function hideLoading() {
    const loadingOverlay = document.querySelector('.loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.remove();
        document.body.style.overflow = '';
    }
}

// Initialize form loading indicators
function initFormLoading() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                const originalText = submitButton.innerHTML;
                submitButton.disabled = true;
                submitButton.innerHTML = `
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    ${submitButton.textContent}
                `;
                
                // Store original text for restoration if needed
                submitButton.dataset.originalText = originalText;
            }
        });
    });
}

// Initialize animations
function initAnimations() {
    const animatedElements = document.querySelectorAll('.fade-in, .slide-up, .slide-in-right');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(element => {
        element.style.animationPlayState = 'paused';
        observer.observe(element);
    });
}

// Initialize copy buttons
function initCopyButtons() {
    const copyButtons = document.querySelectorAll('.copy-btn');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.dataset.clipboardText;
            navigator.clipboard.writeText(textToCopy)
                .then(() => {
                    // Change button icon temporarily to show success
                    const originalIcon = this.innerHTML;
                    this.innerHTML = '<i class="bi bi-check"></i>';
                    
                    setTimeout(() => {
                        this.innerHTML = originalIcon;
                    }, 2000);
                })
                .catch(err => {
                    console.error('Failed to copy text: ', err);
                });
        });
    });
}

// Initialize category filters
function initCategoryFilters() {
    const categoryButtons = document.querySelectorAll('.naryn-category-btn');
    const productItems = document.querySelectorAll('.naryn-product-item');
    
    if (categoryButtons.length && productItems.length) {
        categoryButtons.forEach(button => {
            button.addEventListener('click', () => {
                // Remove active class from all buttons
                categoryButtons.forEach(btn => btn.classList.remove('active'));
                // Add active class to clicked button
                button.classList.add('active');
                
                const category = button.dataset.category;
                
                // Filter products
                productItems.forEach(item => {
                    if (category === 'all' || item.dataset.categories.includes(category)) {
                        item.classList.remove('hidden');
                    } else {
                        item.classList.add('hidden');
                    }
                });
            });
        });
    }
}

// Initialize quantity selectors
function initQuantitySelectors() {
    const quantityControls = document.querySelectorAll('.quantity-controls');
    
    if (quantityControls.length) {
        quantityControls.forEach(control => {
            const minusBtn = control.querySelector('button:first-child');
            const plusBtn = control.querySelector('button:last-child');
            const input = control.querySelector('input');
            
            if (minusBtn && plusBtn && input) {
                minusBtn.addEventListener('click', () => {
                    let value = parseInt(input.value) || 0;
                    if (value > 1) {
                        input.value = value - 1;
                        const changeEvent = new Event('change');
                        input.dispatchEvent(changeEvent);
                    }
                });
                
                plusBtn.addEventListener('click', () => {
                    let value = parseInt(input.value) || 0;
                    const max = parseInt(input.max) || 999;
                    if (value < max) {
                        input.value = value + 1;
                        const changeEvent = new Event('change');
                        input.dispatchEvent(changeEvent);
                    }
                });
            }
        });
    }
}

// Initialize delivery area selection
function initDeliveryAreaSelection() {
    const deliveryAreas = document.querySelectorAll('input[name="delivery_area"]');
    const deliveryFeeElement = document.getElementById('delivery-fee');
    const orderTotalElement = document.getElementById('order-total');
    
    if (deliveryAreas.length && deliveryFeeElement && orderTotalElement) {
        const subtotalValue = parseFloat(orderTotalElement.textContent.replace(/[^\d.]/g, ''));
        
        deliveryAreas.forEach(area => {
            area.addEventListener('change', function() {
                let deliveryFee = 0;
                let feeText = 'Free';
                
                if (this.value === 'suburbs') {
                    deliveryFee = 50;
                    feeText = '50 сом';
                } else if (this.value === 'villages') {
                    deliveryFee = 100;
                    feeText = '100 сом';
                }
                
                deliveryFeeElement.textContent = feeText;
                orderTotalElement.textContent = (subtotalValue + deliveryFee).toFixed(2) + ' сом';
            });
        });
    }
}

// Function to update quantity in cart
function updateQuantity(itemId, change) {
    const input = document.getElementById(`item-qty-${itemId}`);
    const currentValue = parseInt(input.value) || 1;
    const newValue = Math.max(1, currentValue + change);
    input.value = newValue;
    
    // Update visual subtotals immediately before sending request
    calculateItemSubtotals();
    
    // Then send the update request
    updateItemQuantity(itemId, newValue);
}

function quantityChanged(itemId) {
    const input = document.getElementById(`item-qty-${itemId}`);
    const newValue = parseInt(input.value) || 1;
    input.value = Math.max(1, newValue);
    
    // Update visual subtotals immediately
    calculateItemSubtotals();
    
    // Then send the update request
    updateItemQuantity(itemId, input.value);
}

function updateItemQuantity(itemId, quantity) {
    // Get the cart ID from the page
    const cartId = document.querySelector('[data-cart-id]')?.dataset.cartId;
    
    if (!cartId) {
        console.error('Cart ID not found on the page');
        return;
    }
    
    fetch(`/api/orders/${cartId}/update_item_quantity/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            item_id: itemId,
            quantity: quantity
        })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Failed to update item');
    })
    .then(data => {
        // Don't reload the page, we've already updated the UI
        console.log('Item quantity updated successfully');
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error updating item quantity', 'danger');
    });
}

// Recalculate item subtotals and update the display
function calculateItemSubtotals() {
    let items = document.querySelectorAll('.cart-item');
    let total = 0;
    
    items.forEach(item => {
        // Get the price element and quantity input
        const priceText = item.querySelector('.cart-item-price')?.textContent;
        const quantity = parseInt(item.querySelector('.quantity-input')?.value) || 0;
        
        if (priceText) {
            // Extract the price value (remove 'сом' and other text)
            const priceMatch = priceText.match(/[\d.,]+/);
            const price = priceMatch ? parseFloat(priceMatch[0].replace(',', '.')) : 0;
            
            // Calculate subtotal
            const subtotal = price * quantity;
            total += subtotal;
            
            // Update the subtotal display
            const subtotalDisplay = item.querySelector('.cart-item-subtotal span');
            if (subtotalDisplay) {
                subtotalDisplay.textContent = subtotal.toFixed(2) + ' сом';
            }
        }
    });
    
    // Update total displays
    const summaryItems = document.getElementById('summary-items');
    const summaryTotal = document.getElementById('summary-total');
    
    if (summaryItems) {
        summaryItems.textContent = total.toFixed(2) + ' сом';
    }
    
    if (summaryTotal) {
        summaryTotal.textContent = total.toFixed(2) + ' сом';
    }
    
    // Update cart badge
    const cartBadge = document.getElementById('cart-badge');
    if (cartBadge) {
        let totalItems = 0;
        document.querySelectorAll('.quantity-input').forEach(input => {
            totalItems += parseInt(input.value) || 0;
        });
        cartBadge.textContent = totalItems;
    }
}

function removeItem(itemId) {
    if (confirm('Are you sure you want to remove this item from your cart?')) {
        // First visually remove the item for immediate feedback
        const itemElement = document.getElementById(`item-${itemId}`);
        if (itemElement) {
            itemElement.style.opacity = '0.5';
        }
        
        // Get the cart ID from the page
        const cartId = document.querySelector('[data-cart-id]')?.dataset.cartId;
        
        if (!cartId) {
            console.error('Cart ID not found on the page');
            return;
        }
        
        fetch(`/api/orders/${cartId}/remove_item/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                item_id: itemId
            })
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Failed to remove item');
        })
        .then(data => {
            // Remove the item from DOM
            if (itemElement) {
                itemElement.remove();
            }
            // Recalculate totals
            calculateItemSubtotals();
            
            // Update cart badge
            updateCartBadge();
            
            // Show success toast
            showToast('Item removed from cart', 'success');
            
            // If cart is now empty, reload to show empty cart message
            if (document.querySelectorAll('.cart-item').length === 0) {
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error removing item from cart', 'danger');
            // Restore the item visual if there was an error
            if (itemElement) {
                itemElement.style.opacity = '1';
            }
        });
    }
}

// Animated scroll to elements
function scrollToElement(elementId, offset = 80) {
    const element = document.getElementById(elementId);
    if (element) {
        const elementPosition = element.getBoundingClientRect().top + window.pageYOffset;
        const offsetPosition = elementPosition - offset;
        
        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }
}

// Function for product detail page quantity controls
function incrementQuantity() {
    const input = document.getElementById('quantity');
    if (input) {
        const max = parseInt(input.max) || 999;
        let value = parseInt(input.value) || 0;
        
        if (value < max) {
            input.value = value + 1;
        }
    }
}

function decrementQuantity() {
    const input = document.getElementById('quantity');
    if (input) {
        let value = parseInt(input.value) || 0;
        
        if (value > 1) {
            input.value = value - 1;
        }
    }
}




// // frontend/static/frontend/js/main.js
// document.addEventListener('DOMContentLoaded', function() {
//     // Update cart badge when page loads
//     updateCartBadge();
    
//     // Initialize tooltips
//     var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
//     tooltipTriggerList.map(function (tooltipTriggerEl) {
//         return new bootstrap.Tooltip(tooltipTriggerEl);
//     });
    
//     // Initialize animations for elements
//     initAnimations();
    
//     // Initialize category filtering for Naryn products
//     initCategoryFiltering();
    
//     // Initialize delivery area selection in checkout
//     initDeliveryAreaSelection();
    
//     // Initialize copy buttons
//     initCopyButtons();
    
//     // Add loading indicators to forms
//     initFormLoadingIndicators();
// });

// // Function to update cart badge
// function updateCartBadge() {
//     fetch('/api/orders/cart/')
//         .then(response => {
//             if (response.ok) {
//                 return response.json();
//             }
//             throw new Error('Failed to fetch cart');
//         })
//         .then(data => {
//             const cartBadge = document.getElementById('cart-badge');
//             if (cartBadge) {
//                 const itemCount = data.items ? data.items.reduce((count, item) => count + item.quantity, 0) : 0;
//                 cartBadge.textContent = itemCount;
//             }
//         })
//         .catch(error => {
//             console.error('Error updating cart badge:', error);
//         });
// }

// // Function to add product to cart
// function addToCart(productId, quantity = 1) {
//     // Show loading indicator
//     showLoadingOverlay();
    
//     fetch('/api/orders/cart/')
//         .then(response => response.json())
//         .then(cart => {
//             return fetch(`/api/orders/${cart.id}/add_item/`, {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                     'X-CSRFToken': getCookie('csrftoken')
//                 },
//                 body: JSON.stringify({
//                     product_id: productId,
//                     quantity: quantity
//                 })
//             });
//         })
//         .then(response => {
//             if (response.ok) {
//                 showToast('Product added to cart successfully!', 'success');
//                 updateCartBadge();
//                 hideLoadingOverlay();
//                 return response.json();
//             }
//             throw new Error('Failed to add to cart');
//         })
//         .catch(error => {
//             showToast('Error adding product to cart', 'danger');
//             console.error('Error:', error);
//             hideLoadingOverlay();
//         });
// }

// // Function to add product to cart with quantity from product detail page
// function addToCartWithQuantity(productId) {
//     const quantity = parseInt(document.getElementById('quantity').value) || 1;
//     addToCart(productId, quantity);
// }

// // Function to get CSRF token from cookies
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

// // Enhanced toast notification system
// function showToast(message, type = 'success') {
//     const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
//     const toast = document.createElement('div');
//     toast.className = `toast toast-${type} show slide-in-right`;
//     toast.innerHTML = `
//         <div class="toast-header">
//             <strong class="me-auto">${type === 'success' ? 'Success' : type === 'warning' ? 'Warning' : 'Error'}</strong>
//             <button type="button" class="btn-close" onclick="this.parentElement.parentElement.remove()"></button>
//         </div>
//         <div class="toast-body">
//             ${message}
//         </div>
//     `;
    
//     toastContainer.appendChild(toast);
    
//     // Auto remove after 3 seconds
//     setTimeout(() => {
//         toast.classList.add('fade-out');
//         setTimeout(() => {
//             toast.remove();
//         }, 300);
//     }, 3000);
// }

// function createToastContainer() {
//     const container = document.createElement('div');
//     container.className = 'toast-container';
//     document.body.appendChild(container);
//     return container;
// }

// // Legacy alert function for backward compatibility
// function showAlert(message, type = 'info') {
//     // Use the new toast system instead
//     showToast(message, type);
// }

// // Loading overlay
// function showLoadingOverlay() {
//     let overlay = document.getElementById('loading-overlay');
    
//     // Create overlay if it doesn't exist
//     if (!overlay) {
//         overlay = document.createElement('div');
//         overlay.id = 'loading-overlay';
//         overlay.className = 'loading-overlay';
//         overlay.innerHTML = '<div class="loading-spinner"></div>';
//         document.body.appendChild(overlay);
//     }
    
//     // Show the overlay
//     overlay.style.display = 'flex';
// }

// function hideLoadingOverlay() {
//     const overlay = document.getElementById('loading-overlay');
//     if (overlay) {
//         overlay.style.display = 'none';
//     }
// }

// // Initialize animations for staggered list items and scroll animations
// function initAnimations() {
//     // Add animation classes to staggered items
//     const staggerItems = document.querySelectorAll('.stagger-item');
//     staggerItems.forEach((item, index) => {
//         item.style.animationDelay = `${0.1 * (index + 1)}s`;
//     });
    
//     // Set up intersection observer for on-scroll animations
//     const animatedElements = document.querySelectorAll('.fade-in, .slide-up, .slide-in-right');
    
//     if (animatedElements.length > 0 && 'IntersectionObserver' in window) {
//         const observer = new IntersectionObserver((entries) => {
//             entries.forEach(entry => {
//                 if (entry.isIntersecting) {
//                     entry.target.classList.add('animated');
//                     observer.unobserve(entry.target);
//                 }
//             });
//         }, { threshold: 0.1 });
        
//         animatedElements.forEach(element => {
//             element.classList.add('animation-ready');
//             observer.observe(element);
//         });
//     }
// }

// // Category filtering for Naryn products
// function initCategoryFiltering() {
//     const categoryButtons = document.querySelectorAll('.naryn-category-btn');
//     const productItems = document.querySelectorAll('.naryn-product-item');
    
//     if (categoryButtons.length > 0 && productItems.length > 0) {
//         categoryButtons.forEach(button => {
//             button.addEventListener('click', () => {
//                 // Remove active class from all buttons
//                 categoryButtons.forEach(btn => btn.classList.remove('active'));
//                 // Add active class to clicked button
//                 button.classList.add('active');
                
//                 const category = button.dataset.category;
                
//                 // Filter products with animation
//                 productItems.forEach(item => {
//                     if (category === 'all' || item.dataset.categories.includes(category)) {
//                         item.classList.remove('hidden');
//                         item.style.opacity = '0';
//                         setTimeout(() => {
//                             item.style.opacity = '1';
//                         }, 50);
//                     } else {
//                         item.style.opacity = '0';
//                         setTimeout(() => {
//                             item.classList.add('hidden');
//                         }, 300);
//                     }
//                 });
//             });
//         });
//     }
// }

// // Cart quantity functions
// function updateQuantity(itemId, change) {
//     const input = document.getElementById(`item-qty-${itemId}`);
//     const currentValue = parseInt(input.value) || 1;
//     const newValue = Math.max(1, currentValue + change);
//     input.value = newValue;
    
//     // Update visual subtotals immediately before sending request
//     calculateItemSubtotals();
    
//     // Then send the update request with debounce
//     debounce(() => updateItemQuantity(itemId, newValue), 500)();
// }

// function quantityChanged(itemId) {
//     const input = document.getElementById(`item-qty-${itemId}`);
//     const newValue = parseInt(input.value) || 1;
//     input.value = Math.max(1, newValue);
    
//     // Update visual subtotals immediately
//     calculateItemSubtotals();
    
//     // Then send the update request with debounce
//     debounce(() => updateItemQuantity(itemId, input.value), 500)();
// }

// function updateItemQuantity(itemId, quantity) {
//     // Get the cart ID from the URL or data attribute
//     const cartId = document.querySelector('.cart-container').dataset.cartId;
    
//     fetch(`/api/orders/${cartId}/update_item_quantity/`, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': getCookie('csrftoken')
//         },
//         body: JSON.stringify({
//             item_id: itemId,
//             quantity: quantity
//         })
//     })
//     .then(response => {
//         if (response.ok) {
//             return response.json();
//         }
//         throw new Error('Failed to update item');
//     })
//     .then(data => {
//         // Don't reload the page, we've already updated the UI
//         console.log('Item quantity updated successfully');
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         showToast('Error updating item quantity', 'danger');
//     });
// }

// // Calculate cart subtotals and totals
// function calculateItemSubtotals() {
//     let items = document.querySelectorAll('.cart-item');
//     let total = 0;
    
//     items.forEach(item => {
//         // Get the price element and quantity input
//         const priceText = item.querySelector('.cart-item-price').textContent;
//         const quantity = parseInt(item.querySelector('.quantity-input').value) || 0;
        
//         // Extract the price value (remove 'сом' and other text)
//         const priceMatch = priceText.match(/[\d.,]+/);
//         const price = priceMatch ? parseFloat(priceMatch[0].replace(',', '.')) : 0;
        
//         // Calculate subtotal
//         const subtotal = price * quantity;
//         total += subtotal;
        
//         // Update the subtotal display
//         const subtotalDisplay = item.querySelector('.item-subtotal');
//         if (subtotalDisplay) {
//             subtotalDisplay.textContent = subtotal.toFixed(2) + ' сом';
//         }
//     });
    
//     // Update total displays
//     const summaryItems = document.getElementById('summary-items');
//     const summaryTotal = document.getElementById('summary-total');
    
//     if (summaryItems) {
//         summaryItems.textContent = total.toFixed(2) + ' сом';
//     }
    
//     if (summaryTotal) {
//         summaryTotal.textContent = total.toFixed(2) + ' сом';
//     }
    
//     // Update cart badge
//     const cartBadge = document.getElementById('cart-badge');
//     if (cartBadge) {
//         let totalItems = 0;
//         document.querySelectorAll('.quantity-input').forEach(input => {
//             totalItems += parseInt(input.value) || 0;
//         });
//         cartBadge.textContent = totalItems;
//     }
// }

// // Remove item from cart
// function removeItem(itemId) {
//     if (confirm('Are you sure you want to remove this item from your cart?')) {
//         // First visually remove the item for immediate feedback
//         const itemElement = document.getElementById(`item-${itemId}`);
//         if (itemElement) {
//             itemElement.style.opacity = '0.5';
//         }
        
//         // Get the cart ID from the URL or data attribute
//         const cartId = document.querySelector('.cart-container').dataset.cartId;
        
//         fetch(`/api/orders/${cartId}/remove_item/`, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': getCookie('csrftoken')
//             },
//             body: JSON.stringify({
//                 item_id: itemId
//             })
//         })
//         .then(response => {
//             if (response.ok) {
//                 return response.json();
//             }
//             throw new Error('Failed to remove item');
//         })
//         .then(data => {
//             // Remove the item from DOM with animation
//             if (itemElement) {
//                 itemElement.style.height = itemElement.offsetHeight + 'px';
//                 itemElement.classList.add('removing');
                
//                 setTimeout(() => {
//                     itemElement.style.height = '0';
//                     itemElement.style.padding = '0';
//                     itemElement.style.margin = '0';
                    
//                     setTimeout(() => {
//                         itemElement.remove();
//                         // Recalculate totals
//                         calculateItemSubtotals();
                        
//                         // If cart is now empty, reload to show empty cart message
//                         if (document.querySelectorAll('.cart-item').length === 0) {
//                             location.reload();
//                         }
//                     }, 300);
//                 }, 200);
//             }
            
//             showToast('Item removed successfully', 'success');
//             updateCartBadge();
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             showToast('Error removing item from cart', 'danger');
//             // Restore the item visual if there was an error
//             if (itemElement) {
//                 itemElement.style.opacity = '1';
//             }
//         });
//     }
// }

// // Delivery area selection in checkout
// function initDeliveryAreaSelection() {
//     const deliveryAreas = document.querySelectorAll('input[name="delivery_area"]');
//     const deliveryFeeElement = document.getElementById('delivery-fee');
//     const orderTotalElement = document.getElementById('order-total');
    
//     if (deliveryAreas.length > 0 && deliveryFeeElement && orderTotalElement) {
//         const subtotalText = orderTotalElement.textContent;
//         const subtotalMatch = subtotalText.match(/[\d.,]+/);
//         const subtotalValue = subtotalMatch ? parseFloat(subtotalMatch[0].replace(',', '.')) : 0;
        
//         deliveryAreas.forEach(area => {
//             area.addEventListener('change', function() {
//                 let deliveryFee = 0;
//                 let feeText = 'Free';
                
//                 if (this.value === 'suburbs') {
//                     deliveryFee = 50;
//                     feeText = '50 сом';
//                 } else if (this.value === 'villages') {
//                     deliveryFee = 100;
//                     feeText = '100 сом';
//                 }
                
//                 deliveryFeeElement.textContent = feeText;
//                 orderTotalElement.textContent = (subtotalValue + deliveryFee).toFixed(2) + ' сом';
                
//                 // Animate the total to draw attention
//                 orderTotalElement.classList.add('highlight');
//                 setTimeout(() => {
//                     orderTotalElement.classList.remove('highlight');
//                 }, 1500);
//             });
//         });
//     }
// }

// // Copy button functionality
// function initCopyButtons() {
//     const copyButtons = document.querySelectorAll('.copy-btn');
    
//     if (copyButtons.length > 0) {
//         copyButtons.forEach(button => {
//             button.addEventListener('click', function() {
//                 const textToCopy = this.dataset.clipboardText;
//                 navigator.clipboard.writeText(textToCopy)
//                     .then(() => {
//                         // Change button icon temporarily to show success
//                         const originalIcon = this.innerHTML;
//                         this.innerHTML = '<i class="bi bi-check"></i>';
                        
//                         setTimeout(() => {
//                             this.innerHTML = originalIcon;
//                         }, 2000);
//                     })
//                     .catch(err => {
//                         console.error('Failed to copy text: ', err);
//                     });
//             });
//         });
//     }
// }

// // Product detail page quantity controls
// function incrementQuantity() {
//     const input = document.getElementById('quantity');
//     if (!input) return;
    
//     const max = parseInt(input.max);
//     let value = parseInt(input.value) || 0;
    
//     if (value < max) {
//         input.value = value + 1;
//     }
// }

// function decrementQuantity() {
//     const input = document.getElementById('quantity');
//     if (!input) return;
    
//     let value = parseInt(input.value) || 0;
    
//     if (value > 1) {
//         input.value = value - 1;
//     }
// }

// // Smooth scrolling to elements
// function scrollToElement(elementId, offset = 80) {
//     const element = document.getElementById(elementId);
//     if (element) {
//         const elementPosition = element.getBoundingClientRect().top + window.pageYOffset;
//         const offsetPosition = elementPosition - offset;
        
//         window.scrollTo({
//             top: offsetPosition,
//             behavior: 'smooth'
//         });
//     }
// }

// // Add loading indicators to forms
// function initFormLoadingIndicators() {
//     const forms = document.querySelectorAll('form');
    
//     forms.forEach(form => {
//         form.addEventListener('submit', function() {
//             const submitButton = this.querySelector('button[type="submit"]');
//             if (submitButton) {
//                 const originalText = submitButton.innerHTML;
//                 submitButton.disabled = true;
//                 submitButton.innerHTML = `
//                     <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
//                     <span>${submitButton.textContent}</span>
//                 `;
                
//                 // Store original text for restoration if needed
//                 submitButton.dataset.originalText = originalText;
//             }
//         });
//     });
// }

// // Utility function for debouncing
// function debounce(func, wait) {
//     let timeout;
//     return function executedFunction(...args) {
//         const later = () => {
//             clearTimeout(timeout);
//             func(...args);
//         };
//         clearTimeout(timeout);
//         timeout = setTimeout(later, wait);
//     };
// }