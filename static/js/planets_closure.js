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
            let rowElem = document.createElement('tr');
            for(let planetData of [
                    planet.name,
                    planet.diameter,
                    planet.climate,
                    planet.terrain,
                    planet.surface_water,
                    planet.population
            ]) {
                let tdElem = document.createElement('td');
                let tdText = document.createTextNode(planetData);
                tdElem.appendChild(tdText);
                rowElem.appendChild(tdElem);
            }
            let tdElem = document.createElement('td'),
                tdText;
            if(planet.residents.length > 0) {
                tdText = document.createTextNode(`${planet.residents.length} residents`);
            } else {
                tdText = document.createTextNode('No known residents');
            }
            tdElem.appendChild(tdText);
            rowElem.appendChild(tdElem);
            tableBodyElem.appendChild(rowElem);
        }
    }

    function loadPage(page) {
        if(page === null) {
            page = indexPage;
        }

        $.ajax({
            type: 'GET',
            url: page,
            success: function(returnObj) {
                nextPage = returnObj.next;
                previousPage = returnObj.previous;
                clearTable();
                displayPlanets(returnObj.results);
            }
        });
    }

    return {
        indexPage: 'http://swapi.co/api/planets',
        getNextPage: function() {return nextPage;},
        getPreviousPage: function() {return previousPage;},

        loadPage: function(page) {
            loadPage(page);
        }
    };
})();