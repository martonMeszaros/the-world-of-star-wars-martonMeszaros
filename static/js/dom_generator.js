const generateDOM = (function() {
    function createNewDOMElement (tag, innerText) {
        var newElement = document.createElement(tag);
        if(innerText !== null) {
            newElement.appendChild(document.createTextNode(innerText));
        }
        return newElement;
    }
    
    return {
        newElem: function(tag, innerText=null) {return createNewDOMElement(tag, innerText);}
    };
})();