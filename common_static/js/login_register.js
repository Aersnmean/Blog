$(function () {
    var phonList = /^1[3456789]\d{9}$/;
    //手机号格式校验
    $('input[type="tel"]').blur(function(){
        if($(this).val().length==0){
            $(this).next('.tips').text("手机号不能为空");
        }else if(!phonList.test($(this).val())){
            $(this).next('.tips').text("手机号格式不正确");
        }else{
            $(this).next('.tips').text("");
        }
    });
    //密码格式校验
    $('input[type="password"]').blur(function(){
        if($(this).val().length==0){
            $(this).next('.tips').text("密码不能为空");
        }else if($(this).val().length>0 && $(this).val().length<6){
            $(this).next('.tips').text("长度只能在6-20个字符之间");
        }else{
            $(this).next('.tips').text("");
        }
    });
    //昵称格式校验
    $('#register_form input').eq(1).blur(function(){
        if($(this).val().length==0){
            $(this).next('.tips').text("昵称不能为空");
        }else if($(this).val().length<2 || $(this).val().length>20){
            $(this).next('.tips').text("长度只能在2-20个字符之间");
        }else{
            $(this).next('.tips').text("");
        }
    });
    //确认密码校验
    $('#register_form input').eq(3).blur(function(){
        if($(this).val() != $('#register_form input').eq(2).val()){
            $(this).next('.tips').text("两次密码不一致");
        }else{
            $(this).next('.tips').text("");
        }
    });
    //登录按钮提交
    $('#login_btn').on('click', function (e) {
        e.preventDefault();
        if ($('#login_form .tips').text() == '') {
            let data = $('#login_form').serializeArray();
            let datas = {};
            for(let i = 0; i < data.length; i++){
                datas[data[i].name] = data[i].value;
            }
            console.log(datas);
            $.ajax({
                url: '/log/',
                type: 'get',
                data: datas,
                dataType: 'json',
                success:function (res) {
                    res = JSON.parse(res);
                    console.log(res);
                    if (res.status == 200) {
                        window.location.href = "/";
                    }else {
                        $('#login_form .tips').eq(1).text(res.msg);
                        $('#login_form input[type="password"]').val('');
                    }
                }
            });
        }
    });
    // 注册校验手机号是否已注册
    $('#register_form input[type="tel"]').blur(function(){
        if ($(this).next('.tips').text() == '') {
            $.ajax({
                url: '/validate_tel/',
                type: 'get',
                data: {'account': $(this).val()},
                dataType: 'json',
                success:function (res) {
                    res = JSON.parse(res);
                    console.log(res);
                    if (res.status == 405) {
                        $('#register_form input[type="tel"]').next('.tips').text(res.msg);
                    }
                }
            });
        }
    });
    // 注册按钮提交
    $('#register_btn').on('click', function (e) {
        e.preventDefault();
        if ($('#register_form .tips').text() == '') {
            let data = $('#register_form').serializeArray();
            let datas = {};
            for(let i = 0; i < 3; i++){
                datas[data[i].name] = data[i].value;
            }
            $.ajax({
                url: '/reg/',
                type: 'post',
                data: datas,
                dataType: 'json',
                success:function (res) {
                    res = JSON.parse(res);
                    console.log(res);
                    if (res.status == 200) {
                        alert('注册成功');
                        window.location.href = "/";
                    }else {
                        alert('注册失败');
                    }
                }
            });
        }
    });
});