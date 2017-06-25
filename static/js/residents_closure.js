const residents = (function() {
    function clearTable() {
        document.getElementById('residents-table-body').innerHTML = '';
    }

    function secureUrl(url) {
        return url.replace('http', 'https');
    }

    function displayResident(resident) {
        var trElem = generateDOM.newElem('tr');
        for(let residentData of [
                resident.name,
                resident.height,
                resident.mass,
                resident.hair_color,
                resident.skin_color,
                resident.eye_color,
                resident.birth_year,
                resident.gender
        ]) {
            trElem.appendChild(generateDOM.newElem('td', residentData));
        }
        document.getElementById('residents-table-body').appendChild(trElem);
    }

    function loadResidents(planet) {
        clearTable();
        for(let residentUrl of planet.residents) {
            $.ajax({
                type: 'GET',
                url: secureUrl(residentUrl),
                success: function(returnObj) {
                    displayResident(returnObj);
                }
            });
        }
    }

    return {
        load: function(planet) {
            loadResidents(planet);
        }
    };
})();