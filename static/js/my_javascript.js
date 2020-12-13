
$(function(){
    // $(".login-action").click(function(){
    //     $("#action").fadeIn();
    // }),
    $("#log-ac").click(function(){
        $(".form-login").addClass('action');
    }),
    $("#log-ac").hover(function(){
        $("#log-ac").text('LOGIN HERE!');
    },
    function(){
        $("#log-ac").text('Login here!');
    }
    )
})
