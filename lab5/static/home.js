function getSensitiveData() {
    jQuery.get({
        url: dataUrl,
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (data) {
            jQuery("#sensitive-data-container").html(String(data.data));
        },
        error: function (data) {
            console.error(data);
        }
    })
}

function submitSensitiveData(event) {
    const data = jQuery("#sensitive-data-input").val();
    jQuery.ajax({
        url: dataUrl,
        type : 'PUT',
        contentType: "application/json",
        data: JSON.stringify({
            data
        }),
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (data) {
            jQuery("#sensitive-data-container").html(String(data.data));
        },
        error: function (data) {
            console.error(data);
        }
    })
}

$(document).ready(function() {
    getSensitiveData();
});