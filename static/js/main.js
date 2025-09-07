let URL = "http://127.0.0.1:5000/"


function req_wrapper(route, jsonData, successCallback, errorCallback, methodType = "POST") {
    var jsonDataString = JSON.stringify(jsonData);

    $.ajax({
        url: URL + route,
        method: methodType,
        data: jsonDataString,
        contentType: "application/json",
        success: function(data) {
            if (successCallback) {
                successCallback(data);
            }
        },
        error: function(xhr, status, error) {
            if (errorCallback) {
                errorCallback(xhr.responseText);
            } else {
                alert("Error: " + xhr.responseText);
            }
        }
    });
}

function check_post_route(route) {
    req_wrapper(route, "hello there", x => alert(x), x => alert(x), methodType = "GET");
}

function add_p(text) {
  $("#body").innerHTML = "hello";
}


