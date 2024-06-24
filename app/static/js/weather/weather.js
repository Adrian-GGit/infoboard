document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('html');
    const imagePath = `url('/static/img/weather/background/${currentWeatherDescription}.jpg')`;
    container.style.backgroundImage = imagePath;
});

// refresh information every 5 minutes
setTimeout(() => {
    window.location.reload();
}, 300000);

// slide in animation
$(".forecast-item").each(function(index){
    $(this).css({
        'animation-delay' : 0.1 * (1+index) + 's'
    });
});
