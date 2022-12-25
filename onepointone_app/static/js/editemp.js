
var baseURL = "/";

var employee_name = "";
var dob = "";
var join_date = "";
var gender = "";
var designation = "";
var rights = "";
var attachment = "";
var password = "";
var mail = "";

function validateForm() {
    unique_id = $("#unique_id").val()

    employee_name = $("#employee_name").val();

    mail = $("#mail").val();
    password = $("#password").val();
    designation = $("#designation").val();
    gender = $("input[name='gender']:checked").val();
    join_date = $("#join_date").val();
    dob = $("#dob").val();
    rights = $("#rights").val();
    attachment = $("#attachment")[0].files[0];


//    if (employee_name === "") {
//        $(".mob_errorr").html("Please enter employee Name.");
//        $(".mob_errorr").stop().fadeIn(400).delay(3000).fadeOut(400);
//    }
//
//
//    else if (mail === "") {
//        $(".mob_errorr").html("Please enter mail id ");
//        $(".mob_errorr").stop().fadeIn(400).delay(3000).fadeOut(400);
//    }
//
//    else if (password === "") {
//        $(".mob_errorr").html("Please enter password ");
//        $(".mob_errorr").stop().fadeIn(400).delay(3000).fadeOut(400);
//    }
//
//    else if (designation === "") {
//        $(".mob_errorr").html("Please designation");
//        $(".mob_errorr").stop().fadeIn(400).delay(3000).fadeOut(400);
//    }
//
//
//    else if (gender === "") {
//        $(".mob_errorr").html("Please select gender");
//        $(".mob_errorr").stop().fadeIn(400).delay(3000).fadeOut(400);
//    }
//
//    else if (join_date === "") {
//        $(".mob_errorr").html("Please select join_date ");
//        $(".mob_errorr").stop().fadeIn(400).delay(3000).fadeOut(400);
//    }
//
//    else if (rights === "") {
//        $(".mob_errorr").html("Please select rights ");
//        $(".mob_errorr").stop().fadeIn(400).delay(3000).fadeOut(400);
//    }
//    else{
    SubmitFeedbackForm();
//    }


}
function SubmitFeedbackForm() {
    var feedbackForm = new FormData();
    postdata = JSON.stringify(
            {
                "employee_name": employee_name,
                "password": password,
                "mail": mail,
                "designation": designation,
                "gender": gender,
                "join_date": join_date,
                "dob":dob,
                "rights": rights,
                "unique_id":unique_id
            });

    console.log(postdata);

    feedbackForm.append('requestData', (postdata));
    feedbackForm.append('files', attachment);

    try
    {
        request = $.ajax({
            "async": true,
            "crossDomain": true,
            "url": baseURL + "saveEditEmp",
            "method": "POST",
            "headers": {
                "cache-control": "no-cache"
            },
            "processData": false,
            "contentType": false,
            "mimeType": "multipart/form-data",
            "data": feedbackForm,

            beforeSend: function () {
            },
            complete: function () {
            },
            success: function () {

                alert("User has been submitted successfully");
                 window.location.href = baseURL + "onepointone";
            }

        })
    } catch (exception)
    {
        //console.log("exception " + exception);

    }
}
