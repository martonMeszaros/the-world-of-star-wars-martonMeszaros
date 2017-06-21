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
            let residentsCell;
            if(planet.residents.length > 0) {
                residentsCell = generateDOM.newElem('button', `${planet.residents.length} residents`);
                residentsCell.classList.add('btn', 'btn-default');
                residentsCell.setAttribute('type', 'button');
                residentsCell.dataset.toggle='modal';
                residentsCell.dataset.target='#residents-modal';
                residentsCell.addEventListener('mouseenter', function(){
                    residents.load(planet)
                });
                let tdElem = generateDOM.newElem('td');
                tdElem.appendChild(residentsCell);
                rowElem.appendChild(tdElem);
            } else {
                residentsCell = 'No known residents';
                rowElem.appendChild(generateDOM.newElem('td', residentsCell));
            }
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