$(document).ready(function() {
    let jsMain = document.getElementById('js-main');
    if(jsMain.dataset.user === "true") {
        planets.setUserLoggedIn(true);
    } else {
        planets.setUserLoggedIn(false);
    }
    planets.loadPage(planets.indexPage);
});