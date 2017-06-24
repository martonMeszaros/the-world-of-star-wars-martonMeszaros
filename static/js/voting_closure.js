const vote = (function() {
    function voteForPlanet(planetId) {
        $.ajax({
            type: 'POST',
            url: `/vote/${planetId}`,
            success: function() {
                alert('Successfully voted on planet!');
                loadVotes();
            },
            error: function() {
                alert('Voting failed!');
            }
        });
    }

    function clearTable() {
        document.getElementById('votes-table-body').innerHTML = '';
    }

    function populateTable(votesData) {
        var tableBodyElem = document.getElementById('votes-table-body');
        for(let vote of votesData.results) {
            let trElem = generateDOM.newElem('tr');
            for(let tdText of [vote.planet, vote.count]) {
                trElem.appendChild(generateDOM.newElem('td', tdText));
            }
            tableBodyElem.appendChild(trElem);
        }
    }

    function loadVotes() {
        clearTable();
        $.ajax({
            type: 'GET',
            url: '/votes',
            success: function(returnObj) {
                populateTable(JSON.parse(returnObj));
            }
        });

    }
    
    return {
        newVote: function(planetId) {voteForPlanet(planetId);},
        loadVotes: function() {loadVotes();}
    }
})();