var counter = 0;

document.addEventListener("click", function() {
    counter++;
    document.getElementById("counter").innerText = counter;
})

if ("serviceWorker" in navigator) {
    window.addEventListener("load", function() {
        navigator.serviceWorker //intellisense wants to update thiis to this.navigator.serviceWorker...?
        .register("/js/serviceWorker.js")
        .then(function() {
            console.log("service worker registered")
        })
        .catch(function() {
            console.log("service worker not registered", err)
        })
    })
}