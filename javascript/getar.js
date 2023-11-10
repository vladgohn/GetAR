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

let isProgrammaticChange = false;

function updateHeight() {
  if (isProgrammaticChange) return; // Предотвращаем рекурсивный вызов

  const aspectRatio = getAspectRatio();
  if (aspectRatio) {
    const widthInput = document.querySelector('#input_calc_w input');
    const heightOutput = document.querySelector('#input_calc_h input');
    const width = parseInt(widthInput.value, 10);
    if (!isNaN(width)) {
      const height = Math.round(width / aspectRatio);

      isProgrammaticChange = true; // Устанавливаем флаг перед программным изменением
      heightOutput.value = height;
      heightOutput.dispatchEvent(new Event('input', { bubbles: true }));
      isProgrammaticChange = false; // Сбрасываем флаг после изменения
    }
  }
}

function updateWidth() {
  if (isProgrammaticChange) return; // Предотвращаем рекурсивный вызов

  const aspectRatio = getAspectRatio();
  if (aspectRatio) {
    const heightInput = document.querySelector('#input_calc_h input');
    const widthOutput = document.querySelector('#input_calc_w input');
    const height = parseInt(heightInput.value, 10);
    if (!isNaN(height)) {
      const width = Math.round(height * aspectRatio);

      isProgrammaticChange = true; // Устанавливаем флаг перед программным изменением
      widthOutput.value = width;
      widthOutput.dispatchEvent(new Event('input', { bubbles: true }));
      isProgrammaticChange = false; // Сбрасываем флаг после изменения
    }
  }
}


function setupEventListeners() {
  const widthInputElement = document.querySelector('#input_calc_w input');
  const heightInputElement = document.querySelector('#input_calc_h input');
  if (widthInputElement && heightInputElement) {
    widthInputElement.addEventListener('input', updateHeight);
    heightInputElement.addEventListener('input', updateWidth);
    clearInterval(checkExistInterval);
  }
}

function resetInputFields() {
  const realWidthInput = document.querySelector('#ar_input_real_w input');
  const realHeightInput = document.querySelector('#ar_input_real_h input');
  const aspectRatioInput = document.querySelector('#ar_calc_aspect input');
  
  if (realWidthInput) {
    realWidthInput.value = '';
    realWidthInput.dispatchEvent(new Event('input', { bubbles: true }));
  }
  if (realHeightInput) {
    realHeightInput.value = '';
    realHeightInput.dispatchEvent(new Event('input', { bubbles: true }));
  }
  if (aspectRatioInput) {
    aspectRatioInput.value = '';
    aspectRatioInput.dispatchEvent(new Event('input', { bubbles: true }));
  }
}

const checkExistInterval = setInterval(setupEventListeners, 500);
