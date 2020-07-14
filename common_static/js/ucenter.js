$(function () {

    if ($('#ucenter').css('display') == 'none') {
        $('#user, #ucenter').on('mouseenter', function () {
            $('#ucenter').slideDown();
        });
    }
    $('#ucenter').on('mouseleave', function () {
        $('#ucenter').slideUp();
    });

    $('.ucenter_li a').eq(0).on('click', function () {
        $('#change_password, #allb').show();
    });

    $('.ucenter_li a').eq(1).on('click', function () {
        $.ajax({
            url: 'http://127.0.0.1:8000/logout/',
            type: 'get',
            data: null,
            dataType: 'json',
            success:function (res) {
                console.log(res);
                if (res.status == 200) {
                    window.location.reload();
                }
            }
        });
    });

    $('.allb').on('click', function () {
        $('#change_password, #allb').hide();
    });

    // 修改密码
    $('#change_password_btn').on('click', function () {
        let data = $('.password').serializeArray();
        let datas = {};
        for(let i = 0; i < data.length; i++){
            datas[data[i].name] = data[i].value;
        }
        if (datas.old_password.length>=6&&datas.old_password.length<=20&&datas.new_password.length>=6&&datas.new_password.length<=20) {
            if (datas.old_password != datas.new_password) {
                if (datas.new_password == datas.replace_password) {
                    $.ajax({
                        url: 'http://127.0.0.1:8000/log/',
                        type: 'put',
                        data: datas,
                        dataType: 'json',
                        success:function (res) {
                            res = JSON.parse(res);
                            console.log(res);
                            if (res.status == 200) {
                                window.location.reload();
                            }else {
                                $('#change_password_massage').text(res.msg);
                            }
                        }
                    });
                }else {
                    $('#change_password_massage').text('两次密码不一致');
                }
            }else {
                $('#change_password_massage').text('新旧密码不能一致');
            }
        }else{
            $('#change_password_massage').text('长度只能在6-20个字符之间');
        }
    })
});