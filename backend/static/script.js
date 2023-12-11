function showPopup() {
    var popup = document.getElementById("popup");
    popup.style.display = "block";
    popup.parentNode.style.display = "flex";
    setTimeout(function () {
        hidePopup();
    }, 3000);
}

function hidePopup() {
    var popup = document.getElementById("popup");
    popup.style.display = "none";
    popup.parentNode.style.display = "none";
}