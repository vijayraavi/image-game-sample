var origImageID = null

function makeXMLHttpRequest(url, method, body, onLoadCallback)
{
    var req = new XMLHttpRequest();
    req.onload = onLoadCallback;
    req.open(method, url, false);
    req.send(body);
}

function rotate(side)
{
    var optionEl = document.getElementById('option-image');

    // Create the json payload for appropriate direction
    var direction = ((side == 'right') ? 'clock' : 'counter');
    var jsonBody = {'image' : optionEl.src, 'direction' : direction}

    // On load function for the request
    var onLoad = function() {
        var optionImgJson = JSON.parse(this.responseText);
        optionEl.src = optionImgJson['encoded_image'];
    };
    // TODO: Make this point to the actual URL of the Azure Function App
    makeXMLHttpRequest('http://localhost:7071/api/rotateimage', 'POST', JSON.stringify(jsonBody), onLoad);
}

function validate(val)
{
    var optionEl = document.getElementById('option-image');

    // Create the json payload with the image and the ID
    var jsonBody = {'image' : optionEl.src, 'id' : origImageID}

    // On load function for the request
    var onLoad = function() {
        // Get the modal contents to show the user
        var modalHeader = document.getElementById('model-content-header');
        var modalResult = document.getElementById('model-content-result');

        var valJson = JSON.parse(this.responseText);

        // Set the appropriate message dependent on the result
        if (valJson['match'])
        {
            modalHeader.innerHTML = 'You are good at this!'
            modalResult.innerHTML = 'Yay! Congratulations! You solved the puzzle. Close this and retry.'
        }
        else
        {
            modalHeader.innerHTML = 'Oh no! It happens.'
            modalResult.innerHTML = 'Unfortunately, you could not complete the puzzle. Close this and retry.'
        }
        $('.ui.modal').modal('show');
    };

    // TODO: Make this point to the actual URL of the Azure Function App
    makeXMLHttpRequest('http://localhost:7071/api/validateimage', 'POST', JSON.stringify(jsonBody), onLoad);
}

window.addEventListener('load', function() {
	var mainEL = document.getElementById('main-image');

	// On load function for the request
    var onLoadMainImage = function() {
        // Get the main element and set the image from the response
        var mainEL = document.getElementById('main-image');
        var mainImgJson = JSON.parse(this.responseText);
        mainEL.src = mainImgJson['encoded_image'];
        origImageID = mainImgJson['id']

        var onLoadRandomImage = function() {
            // Get the option choice element and set the image from the response
            var optionEl = document.getElementById('option-image');
            var optionImgJson = JSON.parse(this.responseText);
            optionEl.src = optionImgJson['encoded_image'];
        };

        // Create the payload to send for rotating
        var jsonBody = {'image' : mainImgJson['encoded_image']}

        // TODO: Make this point to the actual URL of the Azure Function App
        makeXMLHttpRequest('http://localhost:7071/api/randomrotate', 'POST', JSON.stringify(jsonBody), onLoadRandomImage);
    };

	// TODO: Make this point to the actual URL of the Azure Function App
    makeXMLHttpRequest('http://localhost:7071/api/fetchrandomimage', 'GET', null, onLoadMainImage);
});