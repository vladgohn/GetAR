function getAspectRatio() {
  const widthInput = document.querySelector('#ar_input_real_w input');
  const heightInput = document.querySelector('#ar_input_real_h input');
  const width = parseInt(widthInput.value, 10);
  const height = parseInt(heightInput.value, 10);

  if (!isNaN(width) && !isNaN(height) && height !== 0) {
    return width / height;
  }
  return null;
}

function updateHeight() {
  const aspectRatio = getAspectRatio();
  if (aspectRatio) {
    const widthInput = document.querySelector('#input_calc_w input');
    const heightOutput = document.querySelector('#input_calc_h input');
    const width = parseInt(widthInput.value, 10);
    if (!isNaN(width)) {
      const height = Math.round(width / aspectRatio);
      heightOutput.value = height;
    }
  }
}

function updateWidth() {
  const aspectRatio = getAspectRatio();
  if (aspectRatio) {
    const heightInput = document.querySelector('#input_calc_h input');
    const widthOutput = document.querySelector('#input_calc_w input');
    const height = parseInt(heightInput.value, 10);
    if (!isNaN(height)) {
      const width = Math.round(height * aspectRatio);
      widthOutput.value = width;
    }
  }
}

// Функция для установки обработчиков событий
function setupEventListeners() {
  const widthInputElement = document.querySelector('#input_calc_w input');
  const heightInputElement = document.querySelector('#input_calc_h input');
  if (widthInputElement && heightInputElement) {
    widthInputElement.addEventListener('input', updateHeight);
    heightInputElement.addEventListener('input', updateWidth);
    clearInterval(checkExistInterval); // Очистка интервала после установки обработчиков
  }
}

// Периодическая проверка наличия элементов и установка обработчиков событий
const checkExistInterval = setInterval(setupEventListeners, 500);
