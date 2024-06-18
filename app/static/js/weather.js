document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('html');
    const imagePath = `url('/static/img/weather/background/${currentWeatherDescription}.jpg')`;
    container.style.backgroundImage = imagePath;
});

setTimeout(() => {
    window.location.reload();
}, 300000);
