$(document).ready(function(){
    $("#upload-form").change(function(){
        var formData = new FormData($('#upload-form')[0]);
        $("#upload-label").html(formData.entries().next().value[1].name);
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            dataType: 'json',
            processData: false,
            contentType : false,
            success: function(data, textStatus){
                $("#verify-btn-div").css("display", "inline");
                console.log("success!")
                console.log(data)
                console.log(textStatus)
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                console.log("error!")
                console.log(XMLHttpRequest)
                console.log(textStatus)
                console.log(errorThrown)
            }
        })
    });

    $("#verify-btn").click(function(){
        $("#original-img")[0].src = "http://127.0.0.1:5000/static/sources/first_class/origin.jpg";
        // $.ajax({
        //     url: '/Verify1',
        //     type: 'POST',
        //     data: formData,
        //     dataType: 'json',
        //     processData: false,
        //     contentType : false,
        //     success: function(data, textStatus){
        //         $("#verify-btn-div").css("display", "inline");
        //         console.log("success!")
        //         console.log(data)
        //         console.log(textStatus)
        //     },
        //     error: function (XMLHttpRequest, textStatus, errorThrown) {
        //         console.log("error!")
        //         console.log(XMLHttpRequest)
        //         console.log(textStatus)
        //         console.log(errorThrown)
        //     }
        // })
    });
});