

$("#closeBtn").click(function() {
    $('#newTaskDialog').hide();
});
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$('#newTaskBtn').click(function() {
   $('#newTaskDialog').show();
});

$("#createTaskBtn").click(function() {

    var platform = $("#platform").val();
    var modelFile = $('#uploaded-filename').text()

    if (modelFile === "no file" || modelFile === "now, please run uploadHelper to select file") {
        alert('please upload file');
        return;
    }
    if (platform === "") {
        alert('please select platform')
        return;
    }

    var formData = new FormData();
    formData.append('platform', platform);
    formData.append('modelFile', modelFile);

    $.ajax({
        type: 'POST',
        url: '/create_task/',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            $('#uploaded-filename').text("no file");
            alert('Task completed');
            location.reload();
        },
        error: function(xhr, status, error) {
            $('#uploaded-filename').text("no file");
            alert('Error occurred while creating task');
        }
    });
});

$('#uploadBtn').click(function(){
    startUploadService()
});
var startUploadService = function() {
    $.ajax({
        url: '/start_upload_service/',
        type: 'POST',
        processData: false,
        contentType: false,
        success: function(response) {
            console.log(response);
            $('#uploaded-filename').text("now, please run uploadHelper to select file");
            get_uploaded_filename()
        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
};

function get_uploaded_filename() {
  $.ajax({
    url: '/get_uploaded_filename/',
    success: function(data) {
      $('#uploaded-filename').text(data);
    },
    error: function() {
      console.log('获取文件名失败');
    }
  });
}

//var tip = document.getElementById('tip');
//var toggleArrow = document.getElementById('toggleArrow');
//
//toggleArrow.addEventListener('click', function() {
//    var isTipCollapsed = toggleArrow.innerHTML.charCodeAt(0) === 9664; // Check if the arrow is right-pointing
//    if (isTipCollapsed) {
//        // Expand the tip and change the arrow to left-pointing
//        tip.style.right = '0';
//        toggleArrow.innerHTML = '&#9654;'; // Left-pointing arrow
//    } else {
//        // Collapse the tip and change the arrow to right-pointing
//        tip.style.right = '-450px'; // Adjust as needed to hide the tip box, leaving only the arrow visible
//        toggleArrow.innerHTML = '&#9664;'; // Right-pointing arrow
//    }
//});


