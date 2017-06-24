const vote = (function() {
    function voteForPlanet(planetId) {
        $.ajax({
            type: 'POST',
            url: `vote/${planetId}`,
            success: function() {
                alert('Successfully voted on planet!');
            },
            error: function() {
                alert('Voting failed!');
            }
        });
    }
    
    return {
        newVote: function(planetId) {voteForPlanet(planetId);}
    }
})();