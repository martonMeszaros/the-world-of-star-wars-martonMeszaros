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

    function killEventListeners(DOMelem) {
        let newDOMElem = DOMelem.cloneNode(true);
        DOMelem.parentNode.replaceChild(newDOMElem, DOMelem);
        return newDOMElem;
    }

    function updatePaginationButtons() {
        let prevPageButton = document.getElementById('previous-page');
        let nextPageButton = document.getElementById('next-page');
        prevPageButton = killEventListeners(prevPageButton);
        nextPageButton = killEventListeners(nextPageButton);

        if(previousPage === null) {
            prevPageButton.classList.add('disabled');
        } else {
            prevPageButton.classList.remove('disabled');
            prevPageButton.addEventListener('click', function() {
                loadPage(previousPage);
            });
        }

        if(nextPage === null) {
            nextPageButton.classList.add('disabled');
        } else {
            nextPageButton.classList.remove('disabled');
            nextPageButton.addEventListener('click', function() {
                loadPage(nextPage);
            });

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
                updatePaginationButtons();
                clearTable();
                displayPlanets(returnObj.results);
            }
        });
    }

    return {
        indexPage: indexPage,
        getNextPage: () => nextPage,
        getPreviousPage: () => previousPage,

        loadPage: function(url) {loadPage(url);}
    };
})();