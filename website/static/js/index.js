text_hue = 0
setInterval(rainbowText, 50);

function rainbowText() {
    var elementList = document.getElementsByClassName("rainbowText");
    for(var i = 0; i < elementList.length; i++) {
        var hsl = "hsl(" + (text_hue + ((360 / elementList.length) * i)) + ", 80%, 60%)", num = text_hue + 5;
        text_hue = num > 360 ? 0 : num, elementList[i].style.color = hsl;
    }
};