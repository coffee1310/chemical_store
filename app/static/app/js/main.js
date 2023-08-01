function increaseValue(counterId) {
  let counter = document.getElementById(counterId);
  if (counter) {
    let currentValue = parseInt(counter.innerText);
    if (!isNaN(currentValue)) {
      let newValue = currentValue + 1;
      counter.innerText = newValue;
    }
  }
}

function reduceValue(counterId) {
  let counter = document.getElementById(counterId);
  if (counter) {
    let currentValue = parseInt(counter.innerText);
    if (!isNaN(currentValue) && currentValue > 1) {
      let newValue = currentValue - 1;
      counter.innerText = newValue;
    }
  }
}

document.addEventListener('DOMContentLoaded', function() {
  // Add event listener to the cart-items container
  const cartItemsContainer = document.querySelector('.cart-items');
  cartItemsContainer.addEventListener('click', function(event) {
    // Check if the clicked element is a "-" button
    if (event.target.tagName === 'BUTTON' && event.target.textContent === '-') {
      decreaseQuantity(event);
    } else if (event.target.tagName === 'BUTTON' && event.target.textContent === '+') {
      increaseQuantity(event);
    }
  });
});

function updateQuantity(itemId, newQuantity) {
  // Send an AJAX request to update the quantity in the database
  fetch(`/cart/update_quantity/${itemId}/${newQuantity}/`)
    .then(response => response.json())
    .then(data => {
      // Update the quantity displayed on the page
      const quantitySpan = document.getElementById(`item-quantity-${itemId}`);
      quantitySpan.textContent = data.new_quantity;
    })
    .catch(error => console.error('Error:', error));
}

function decreaseQuantity(event) {
  const itemId = event.target.dataset.itemId;
  const quantitySpan = document.getElementById(`item-quantity-${itemId}`);
  let quantity = parseInt(quantitySpan.textContent);
  if (quantity > 1) {
    quantity--;
    updateQuantity(itemId, quantity);
  }
}

function increaseQuantity(event) {
  const itemId = event.target.dataset.itemId;
  const quantitySpan = document.getElementById(`item-quantity-${itemId}`);
  let quantity = parseInt(quantitySpan.textContent);
  quantity++;
  updateQuantity(itemId, quantity);
}

function removeItem(event) {
  const itemId = event.target.dataset.itemId;
  console.log(event.target.dataset.itemId);
  const url = `/cart/remove_ajax/${itemId}/`;

  // Get the CSRF token from the page's cookies
  const csrftoken = getCookie('csrftoken');

  fetch(url, {
      method: 'DELETE',
      headers: {
          'X-CSRFToken': csrftoken,
      }
  })
  .then(response => {
      if (response.ok) {
          // Reload the page or update the cart content dynamically
          location.reload(); // or update cart content using JavaScript
      } else {
          console.error('Error:', response.status);
      }
  })
  .catch(error => console.error('Error:', error));
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.startsWith(name + '=')) {
              cookieValue = cookie.substring(name.length + 1);
              break;
          }
      }
  }
  return cookieValue;
} 





