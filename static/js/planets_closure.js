const planets = (function() {
    var indexPage = 'http://swapi.co/api/planets',
        nextPage = null,
        previousPage = null;

    function clearTable() {
        document.getElementById('planets-table-body').innerHTML = '';
    }

    function displayPlanets(planets) {
        var tableBodyElem = document.getElementById('planets-table-body');
        for(let planet of planets) {
            let rowElem = generateDOM.newElem('tr');
            for(let planetData of [
                    planet.name,
                    planet.diameter,
                    planet.climate,
                    planet.terrain,
                    planet.surface_water,
                    planet.population
            ]) {
                rowElem.appendChild(generateDOM.newElem('td', planetData));
            }
            let residents;
            if(planet.residents.length > 0) {
                residents = `${planet.residents.length} residents`;
            } else {
                residents = 'No known residents';
            }
            rowElem.appendChild(generateDOM.newElem('td', residents));
            tableBodyElem.appendChild(rowElem);
        }
    }

    function loadPage(url) {
        if(url === null) {
            url = indexPage;
        }
        $.ajax({
            type: 'GET',
            url: url,
            success: function(returnObj) {
                nextPage = returnObj.next;
                previousPage = returnObj.previous;
                clearTable();
                displayPlanets(returnObj.results);
            }
        });
    }

    return {
        indexPage: indexPage,
        getNextPage: function() {return nextPage;},
        getPreviousPage: function() {return previousPage;},

        loadPage: function(url) {loadPage(url);}
    };
})();