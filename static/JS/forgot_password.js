function sample() {
    var button = document.getElementById('button_click');
    
    button.disabled = true;

    var count = 3;
    var countdownInterval = setInterval(function() {
        button.textContent = 'Wait (' + count + ')';
        count--;

        if (count < 0) {
            clearInterval(countdownInterval);
            button.disabled = false;
            button.textContent = 'Send';
        }
    }, 1000);

    setTimeout(function() {
        clearInterval(countdownInterval);
    }, 4000);
    
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/sample");
    xhr.send();
}

// di an to gumagana. di ko mapagana yung js function at py code at the same time. shemay