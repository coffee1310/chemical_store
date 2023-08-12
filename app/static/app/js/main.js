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
  // Проверяем, является ли элемент кнопкой "-"
  if (event.target.textContent === '-') {
    const itemId = event.target.dataset.itemId;
    const quantitySpan = document.getElementById(`item-quantity-${itemId}`);
    let quantity = parseInt(quantitySpan.textContent);
    if (quantity > 1) {
      quantity--;
      updateQuantity(itemId, quantity);
    }
  }
}

function increaseQuantity(event) {
  // Проверяем, является ли элемент кнопкой "+"
  if (event.target.textContent === '+') {
    const itemId = event.target.dataset.itemId;
    const quantitySpan = document.getElementById(`item-quantity-${itemId}`);
    let quantity = parseInt(quantitySpan.textContent);
    quantity++;
    updateQuantity(itemId, quantity);
  }
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

function changeQuantity(event, diff, itemPrice) {
  const itemId = event.target.dataset.itemId;
  const quantitySpan = document.getElementById(`item-quantity-${itemId}`);
  let quantity = parseInt(quantitySpan.textContent);

  quantity += diff;
  if (quantity < 1) {
    return; // Предотвращаем уменьшение количества до отрицательных значений
  }

  quantitySpan.textContent = quantity;

  updateQuantity(itemId, quantity);

  const priceSpan = document.getElementById(`item-price-${itemId}`);
  let price = parseInt(itemPrice);
  let totalPrice = price * quantity;
  priceSpan.textContent = ''; 

  const subElement = document.createElement('sub');
  subElement.textContent = 'руб';

  priceSpan.appendChild(subElement);

  priceSpan.innerHTML = `${totalPrice} ${subElement.outerHTML}`;

  const defItemPriceSpan = document.getElementById(`def-item-price-${itemId}`);
  defItemPriceSpan.textContent = `${quantity} * ${price} руб`;
  
  const totalAmountSpan = document.getElementById('total-amount');
  let totalAmount = totalAmountSpan.textContent;
  if (diff === -1) {
    totalAmount -= quantity * price;
  }

}

function clearCart() {
  const clearCartUrl = '/cart/clear_cart/';
  const csrftoken = getCookie('csrftoken');

  fetch(clearCartUrl, {
    method: 'DELETE',
    headers: {
      'X-CSRFToken': csrftoken,
    },
  })
    .then(response => response.json())
    .then(data => {
      console.log(data.message);
      // Обновите информацию о корзине или выполните другие действия после очистки
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
