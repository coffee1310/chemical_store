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

