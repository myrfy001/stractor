# coding:utf-8

from lxml import etree

from html5_parser import parse
# from dom_modifier import add_id_to_all_node


def dom_to_tuple(dom):
    add_id_to_all_node(dom)
    print(etree.tostring(dom))
    print(dom)
    print(dom[1][0])
    print(dom[1][0].text)
    for x in dom[1]:
        print(x, type(x))


def dom_to_tuple2(dom):
    print(dom)
    print(dom.docinfo.doctype)
    dom = dom.getroot()
    print(dom[1])
    print(dom[1][0])
    for x in dom[1][0]:
        print(x, type(x))


def dom_to_tuple1(dom):
    print(dom)
    print(dom[0])
    print(dom[0].text)
    for x in dom[1][0]:
        print(x, type(x))


if __name__ == '__main__':
    html = '''

<!DOCTYPE HTML>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta http-equiv="content-language" content="zh-CN" />
<meta name="applicable-device" content="pc,mobile">
<meta name="robots" content="all" />
<meta name="save" content="history" />

<title>关闭、打开金属门 - 声音 - 耳聆网 - (声音分享云|音效素材库)</title>
<meta name="keywords" content="门,近距离,金属,打开,关闭,处理,�" /> <meta name="description" content="关闭、打开金属门" /> <link rel="shortcut icon" href="https://www.ear0.com/public/images/favicon.ico" />

<link rel="stylesheet" type="text/css" href="https://www.ear0.com/public/css/base.css" />

<link rel="stylesheet" type="text/css" href="https://www.ear0.com/app/sound/skin/style.css">

<script>var siteUrl = 'https://www.ear0.com/'; //网站网址</script>
<script>var cdnUrl = 'http://cdn.ear0.com/'; //cdn网址</script>

<script src="https://www.ear0.com/public/js/jquery-1.8.3.min.js" type="text/javascript"></script>
<script src="https://www.ear0.com/public/js/js.cookie-2.1.4.min.js" type="text/javascript"></script>
<!--[if lt IE 9]>
<script src="https://www.ear0.com/public/js/html5shiv.min.js"></script>
<![endif]-->

<style>
</style>
</head>

<body>
<foo>Here is a CDATA section: <![CDATA[ < > & ]]> with all kinds of unescaped text.</foo>
<div class="header">
<div class="topbar">
	<a class="logo" href="https://www.ear0.com/" alt="耳聆网" title="耳聆网"></a>
	<div class="nav">
		<a  href="https://www.ear0.com/">首页</a>
		<a class="select" href="https://www.ear0.com/sound">声音</a>
		<a  href="https://www.ear0.com/pack">合辑</a>
	</div>
	<div class="search">
		<form method="POST" action="https://www.ear0.com/search">
			<input type="text" placeholder="搜索声音" />
			<a class="icon" href="https://www.ear0.com/search">
				<i class="iconfont icon-search"></i>
			</a>
			<input type="submit" style="display:none;" />
		</form>
	</div>
	<div class="user">
		<a href="https://www.ear0.com/user/message"><div class="notify"><span id="newmsg"></span><i class="iconfont icon-message"></i></div></a>
				<span class="logined">
			<a href="https://www.ear0.com/user">
				<img class="face" src="http://cdn.ear0.com/cache/user/0/18/64/9887_18734.png" alt="myrfy001">
				<span>myrfy001 <i class="iconfont icon-down c9"></i></span>
			</a>
			<div class="clear"></div>
			<div class="list">
				<a href="https://www.ear0.com/user/index">我的主页</a>
				<a href="https://www.ear0.com/user/sound">我的声音</a>
				<a href="https://www.ear0.com/user/pack">我的合辑</a>
				<a href="https://www.ear0.com/user/setting">用户设置</a>
				<a href="https://www.ear0.com/user/login/cx-out">退出</a>
			</div>
		</span>
				<a href="https://www.ear0.com/sound/add"><i class="iconfont icon-upload tips" title="上传声音"></i></a>
	</div>
</div>

</div>

<div class="main"><style type="text/css">
    .sound_data .author{
        width:1.20rem;
        margin-right:0.30rem;
        text-align: center;
        float:left;
    }
    .sound_data .author .face{
        width:1.20rem;
        height:1.20rem;
        margin-right:0.30rem;
        margin-bottom:0.10rem;
        border-radius: 0.60rem;
        box-shadow: 0 0 0.15rem 0 rgba(0, 0, 0, 0.15);
    }
    .sound_data .author .data{
        color:#999;
        padding:0 0.05rem;
    }
    .sound_data .data_bar{
        width:10.50rem;
        margin-top:0.20rem;
        margin-bottom: 0.20rem;
        float:left;
    }
    .sound_data .data_bar .username{
        font-size: 0.18rem;
        margin-left:0.05rem;
        float:left;
    }
    .sound_data .data_bar .data_num{
        width:4.50rem;
        float:right;
    }
    .sound_data .data_bar .data_num li{
        color: #999999;
        width: 0.90rem;
        text-align: center;
        float:left;
    }
    .sound_data .data_bar .data_num li .iconfont{
        color:#666;
        margin-right: 0.08rem;
    }
    .sound_data .data_bar .hr{
        width: 100%;
        height: 1px;
        background-color: #DDDDDD;
        clear:both;
        display: block;
        margin:0.10rem 0;
    }
    .sound_data .data_bar .upload_time,
    .sound_data .data_bar .type,
    .sound_data .data_bar .location{
        line-height: 0.20rem;
        margin-right:0.20rem;
        float:left;
    }
    .sound_data .data_bar .rate{
        margin-right:0.20rem;
        float:right;
    }
    .sound_data .data_bar .rate .score{
        background-color: #46B2E9;
        color: #FFFFFF;
        height:0.22rem;
        line-height: 0.22rem;
        width:0.32rem;
        margin-right: 0.10rem;
        text-align: center;
        border-radius: 0.05rem;
        float:left;
    }
    .sound_data .data_bar .rate .star{
        float:left;
    }
    .sound_data .data_bar .rate .num{
        color:#999999;
        margin-left:0.05rem;
        float:right;
    }
    .sound_data .sound_content{
        width:6.50rem;
        min-height: 1.40rem;
        font-size: 0.14rem;
        float:left;
    }
    .sound_data .comment{
        width:8.00rem;
        margin:0.30rem 0;
        float:left;
    }
    .sound_data .comment .face{
        width:0.64rem;
        height:0.64rem;
        border-radius: 0.32rem;
        margin-right:0.30rem;
        float:left;
    }
    .sound_data .comment .post_box{
        min-height: 0.65rem;
        width:7.00rem;
        background-color: #EEEEEE;
        float:left;
    }
    .sound_data .comment .post_box .word{
        width:7.00rem;
        line-height: 0.65rem;
        text-align: center;
        color:#999999;
        font-size: 16px;
        cursor: pointer;
    }
    .sound_data .comment .post_box .editor{
        display:none;
    }
    .sound_data .comment .post_box .editor textarea{
        height:1.00rem;
    }
    .sound_data .comment_list{
        width: 8.00rem;
        height: 8.00rem;
    }
    .sound_data .comment_list .face{
        width:0.48rem;
        height:0.48rem;
        border-radius: 0.24rem;
        margin-left:0.16rem;
        margin-right:0.30rem;
        float:left;
    }
    .sound_data .comment_list .comment_box{
        width:7.00rem;
        min-height: 0.30rem;
        padding-bottom: 0.20rem;
        margin-bottom: 0.25rem;
        border-bottom: 1px solid #EEEEEE;
        float:left;
    }
    .sound_data .comment_list .comment_box .username{

    }
    .sound_data .comment_list .comment_box .comment_content{
        font-size: 0.14rem;
        margin:0.08rem 0;
    }
    .sound_data .comment_list .comment_box .comment_content .refer {
        background-color: #FCF8E3;
        border: 1px solid #FBEED5;
        color: #C09853;
        margin-right: 10px;
        margin-bottom: 5px;
        padding: 8px;
    }
    .sound_data .data_right{
        width: 3.60rem;
        margin-top: 0.20rem;
        float: right;
    }
    .sound_data .data_right .license{

    }
    .sound_data .data_right .license img{
        opacity: 0.4;
    }
    .sound_data .data_right .license .iconfont{
        font-size: 0.32rem;
        margin-top: -0.05rem;
        margin-left: 0.05rem;
    }
</style>

<div id="sound17000" class="soundbox-full">
    <div class="box_bg"></div>
    <div class="mask"></div>
    <div class="midder">
        <div class="cover"><img src="http://cdn.ear0.com/cache/sound_photo/0/17/380/173574_17000.jpeg"></div>
        <div class="waveform" onclick="setPosition('17000',8.789,$(this),event);">
            <div class="progress">
                <div class="value" style="background:url('https://www.ear0.com/file/sound_waveform/full/0/17/17000.png') no-repeat;"></div>
            </div>
            <img src="https://www.ear0.com/file/sound_waveform/full_bg/0/17/17000.png" />
        </div>
        <div class="box_top">
            <div class="title nowrap" title="关闭、打开金属门">关闭、打开金属门</div>
            <div class="clear"></div>
            <div class="tags">
                                <a href="https://www.ear0.com/tag/show/cx-sound/tagid-1804">门</a>
                                <a href="https://www.ear0.com/tag/show/cx-sound/tagid-1010">近距离</a>
                                <a href="https://www.ear0.com/tag/show/cx-sound/tagid-1055">金属</a>
                                <a href="https://www.ear0.com/tag/show/cx-sound/tagid-1899">打开</a>
                                <a href="https://www.ear0.com/tag/show/cx-sound/tagid-1942">关闭</a>
                                <a href="https://www.ear0.com/tag/show/cx-sound/tagid-1022">处理</a>
                                <a href="https://www.ear0.com/tag/show/cx-sound/tagid-2185">开</a>
                            </div>
        </div>
        <div class="clear"></div>
        <div class="box_left">
            <a id="play_btn" class="control round-btn" href="javascript:void(0);" onclick="playSound('17000',$('#sound17000'),8.789,'d59a991b0122a98099029f39935cf9c7a7ab73f3');">
                <i class="iconfont icon-play blue"></i>
            </a>
            <a class="loop round-btn" onclick="loopSound($('#sound17000'));" title="循环播放">
                <i class="iconfont icon-loop"></i>
            </a>
            <a class="volume round-btn">
                <div class="bar" onmouseup="setVolume('17000',$(this),event);">
                    <div class="value"></div>
                </div>
                <i class="iconfont icon-volume" onclick="muteSound('17000',$(this));"></i>
            </a>
            <div class="duration"><span class="playtime">00:00</span> / <span class="endtime">00:00:000</span></div>
        </div>
        <div class="box_right">
            <div class="rate"></div>
            <div class="clear mb15"></div>
            <a class="share round-btn" href="javascript:void(0);" onclick="shareSound('关闭、打开金属门','http://cdn.ear0.com/cache/sound_photo/0/17/380/173574_17000.jpeg');" title="分享声音"><i class="iconfont icon-share"></i></a>
            <a class="download round-btn" href="javascript:void(0);" onclick="downloadSound(17000);" title="下载"><i class="iconfont icon-download"></i></a>
            <a class="comment round-btn" href="javascript:void(0);" onclick="commentSound(17000);" title="评论"><i class="iconfont icon-comment"></i></a>
            <a class="add round-btn" href="javascript:void(0);" onclick="addPackSound(17000);" title="加入合辑"><i class="iconfont icon-add"></i></a>
                        <a class="like round-btn" href="javascript:void(0);" onclick="likeSound(17000);" title="点赞"><i class="iconfont icon-like"></i></a>
                    </div>
        <div class="clear mb10"></div>

    </div>
</div>

<div class="clear mb20"></div>

<div class="midder sound_data">
    <div class="author">
        <a class="username" href="https://www.ear0.com/user/index/userid-5142"><img class="face" src="http://cdn.ear0.com/cache/user/0/5/120/805247_5142.png" alt=""></a>
    <!--测试期间关注数改为合辑数
        <div class="follow_num" title="关注数"><i class="iconfont icon-follow"></i> 0</div>
    -->
        <div class="data fl" title="声音数"><i class="iconfont icon-sound"></i> 9</div>
        <div class="data fr" title="合辑数"><i class="iconfont icon-pack"></i> 0</div>
        <div class="clear mb10"></div>
    <!--测试期间禁用关注模块
        <a class="follow btn size-MINI light" href="javascript:void(0);" onclick="follow(5142);">+ 关注</a>
    -->
    </div>
    <div class="data_bar">
        <a class="username" href="https://www.ear0.com/user/index/userid-5142">Finnegan</a>
        <ul class="data_num">
            <li><i class="iconfont icon-play"></i>219<li>
            <li><i class="iconfont icon-like"></i>0</li>
            <li><i class="iconfont icon-add"></i>0</li>
            <li><i class="iconfont icon-comment"></i>1</li>
            <li><i class="iconfont icon-download"></i>4</li>
        </ul>
        <div class="clear"></div>
        <div class="hr"></div>
        <span class="upload_time"><span class="time">2018-06-11</span> 上传</span>
        <span class="type c9">类型: <a class="blue" href="https://www.ear0.com/sound/list/typeid-20">生活</a></span>
                <div class="rate">
            <div class="score">5.0</div>
            <div class="star"></div>
            <div class="num">(1)</div>
        </div>
    </div>

    <div class="data_right">
                    <a class="license" href="https://www.ear0.com/home/info/keyword-license#by" title="此声音采用 BY 保留署名协议 [署名：bewagne]">
                <img class="grid4" src="https://www.ear0.com/public/images/cc.jpg" />
                <i class="iconfont icon-cc_by fl"></i>
            </a>
        
        <a class="grid5 btn fr" href="javascript:void(0);" onclick="downloadSound(17000);"><i class="iconfont icon-download"></i> 下载</a>
        <div class="clear mb20"></div>
        <div class="info_box sound_info">
            <div class="title">音频信息 <a class="c9 fr" href="" title="信息说明"><i class="iconfont icon-info"></i></a></div>
            <table class="table table-bg table-striped">
                <tbody>
                <tr>
                    <td width="38%">音频格式</td>
                    <td>wav/wav</td>
                </tr>
                <tr>
                    <td>文件大小</td>
                    <td>2.42 MB</td>
                </tr>
                <tr>
                    <td>比特率</td>
                    <td>2304 kbps</td>
                </tr>
                <tr>
                    <td>采样率</td>
                    <td>48000 Hz (24 bit)</td>
                </tr>
                <tr>
                    <td>声道</td>
                    <td>立体声(2声道)</td>
                </tr>
                <tr>
                    <td>编码方式</td>
                    <td>CBR</td>
                </tr>
                </tbody>
            </table>
        </div>
        <div class="info_box">
            <div class="title">
                相似的声音
                <a class="fr fs12 blue" href="https://www.ear0.com/sound/similar/soundid-17000">浏览更多</a>
            </div>
            <ul class="similar_list"></ul>
        </div>
        <!--    测试阶段关闭合辑功能
        <div class="info_box sound_add">
            <div class="title">包含此声音的合辑</div>
        </div>
        -->
    </div>

    <div class="sound_content">
        
<p>关闭、打开金属门</p>
    </div>

    <div class="comment">
        <img class="face" src="http://cdn.ear0.com/cache/user/0/18/64/9887_18734.png" alt="myrfy001">
        <div class="post_box" onclick="show_commentBox();">
            <div class="word">发表评论</div>
            <div class="editor fs12">
                <textarea name="comment" id="cxeditor"></textarea>
                <a class="btn size-S w100" href="javascript:void(0);" onclick="commentSound(17000,null,cxeditor);">发表评论</a>
            </div>
        </div>
        <div class="clear mb20"></div>
    </div>
    <div class="comment_list"></div>
</div>

<script type="text/javascript">
    $(document).ready(function() {
        //格式化声音时长
        $('.soundbox-full').find('.endtime').html( formatTime(8.789 * 1000) );
        //获取封面图片地址
        var soundbox_bg = $('.cover img').attr('src');
        //判断为ie浏览器时不使用淡入背景
        if(!!window.ActiveXObject || "ActiveXObject" in window){
            var duration = 0;
        }else{
            var duration = 1600;
        }
        $('.soundbox-full .box_bg').backgroundBlur({
            imageURL: soundbox_bg,
            blurAmount: 30,
            imageClass : 'box_bg_img',
            duration: duration,
        });
        //修复移动端背景无法宽100%问题
        if($('.soundbox-full .box_bg').width() != $(document).width()){
            $('.soundbox-full .box_bg').css('width',$(document).width()+'px');
            $('.soundbox-full .box_bg .box_bg_img').css('margin-left','0');
        }
        //配图防遮挡
        $('.soundbox-full .cover').hover(function(){
            $('.soundbox-full .waveform').stop().animate({opacity:'0.38'});
        },function(){
            $('.soundbox-full .waveform').stop().animate({opacity:'1'});
        });
        //星星打分
        cxRate(17000,$('.soundbox-full .rate'),5.0,'big');
        cxRate(17000,$('.sound_data .rate .star'),5.0,'small');
        //加载声音评论
        loadSoundComment($('.comment_list'),17000,1);
        //加载相似声音
        loadSimilar($('.similar_list'),17000,20,'门,近距离,金属,打开,关闭,处理,开');
        //键盘控制
        Mousetrap.bind('space', function(e){
            e.preventDefault();
            $('#play_btn').trigger('click');
        });
        Mousetrap.bind('right', function(e){
            e.preventDefault();
            fastForward(17000);
        });
        Mousetrap.bind('left', function(e){
            e.preventDefault();
            fastBackward(17000);
        });
        //延迟加载高德地图API
        jQuery.getScript("https://swebapi.amap.com/maps?v=1.4.0&key=6a41f6492dfc8ef47d3d10af2b4577b0&plugin=AMap.Geocoder");
    });

    var map_layer;
    function show_location(lng,lat){
        map_layer = layer.open({
            type:1,
            area: ['8.00rem', '5.00rem'],
            title:false,
            content: '<div id="map" style="width:100%;height:100%;"></div>'
        });
        if(lng && lat){
            var geotag = [lng,lat];
        }else{
            return false;
        }
        var map = new AMap.Map('map',{
            resizeEnable: true
        });
        map.plugin(['AMap.ToolBar'], function() {
            //设置地位标记为自定义标记
            var toolBar = new AMap.ToolBar();
            map.addControl(toolBar);
        });
        var marker = new AMap.Marker({
            map: map,
            position: geotag,        //坐标大小
            icon: new AMap.Icon({
                size: new AMap.Size(32, 34),  //图标大小
                image: "https://www.ear0.com/public/images/marker.png",
            })
        });
        map.setFitView();
    }

    function show_commentBox(){
                    $('.post_box .editor').slideDown();
            $('.post_box .word').hide();
            }

    //下载后弹出用户贡献引导
    function contribute(soundid){
        $.get('https://www.ear0.com/index.php?app=sound&ac=download&cx=contribute&soundid='+soundid, function(rs){
            layer.closeAll();
            layer.open({
                type:1,
                area: ['6.80rem', ''],
                title: false,
                content: rs,
            });
        });
    }
</script>

<script type="text/javascript">
        var cxeditor = undefined;
        $(document).ready(function(){
            cxeditor = new wangEditor("cxeditor");
            cxeditor.config.emotions = {"default": {title: "默认", data: [{"icon":"https://www.ear0.com/public/images/emoticon/emoji-001.png","value":"[emoji001]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-002.png","value":"[emoji002]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-003.png","value":"[emoji003]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-004.png","value":"[emoji004]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-005.png","value":"[emoji005]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-006.png","value":"[emoji006]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-007.png","value":"[emoji007]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-008.png","value":"[emoji008]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-009.png","value":"[emoji009]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-010.png","value":"[emoji010]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-011.png","value":"[emoji011]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-012.png","value":"[emoji012]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-013.png","value":"[emoji013]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-014.png","value":"[emoji014]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-015.png","value":"[emoji015]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-016.png","value":"[emoji016]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-017.png","value":"[emoji017]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-018.png","value":"[emoji018]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-019.png","value":"[emoji019]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-020.png","value":"[emoji020]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-021.png","value":"[emoji021]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-022.png","value":"[emoji022]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-023.png","value":"[emoji023]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-024.png","value":"[emoji024]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-025.png","value":"[emoji025]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-026.png","value":"[emoji026]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-027.png","value":"[emoji027]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-028.png","value":"[emoji028]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-029.png","value":"[emoji029]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-030.png","value":"[emoji030]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-031.png","value":"[emoji031]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-032.png","value":"[emoji032]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-033.png","value":"[emoji033]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-034.png","value":"[emoji034]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-035.png","value":"[emoji035]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-036.png","value":"[emoji036]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-037.png","value":"[emoji037]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-038.png","value":"[emoji038]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-039.png","value":"[emoji039]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-040.png","value":"[emoji040]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-041.png","value":"[emoji041]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-042.png","value":"[emoji042]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-043.png","value":"[emoji043]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-044.png","value":"[emoji044]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-045.png","value":"[emoji045]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-046.png","value":"[emoji046]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-047.png","value":"[emoji047]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-048.png","value":"[emoji048]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-049.png","value":"[emoji049]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-050.png","value":"[emoji050]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-051.png","value":"[emoji051]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-052.png","value":"[emoji052]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-053.png","value":"[emoji053]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-054.png","value":"[emoji054]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-055.png","value":"[emoji055]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-056.png","value":"[emoji056]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-057.png","value":"[emoji057]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-058.png","value":"[emoji058]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-059.png","value":"[emoji059]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-060.png","value":"[emoji060]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-061.png","value":"[emoji061]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-062.png","value":"[emoji062]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-063.png","value":"[emoji063]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-064.png","value":"[emoji064]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-065.png","value":"[emoji065]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-066.png","value":"[emoji066]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-067.png","value":"[emoji067]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-068.png","value":"[emoji068]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-069.png","value":"[emoji069]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-070.png","value":"[emoji070]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-071.png","value":"[emoji071]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-072.png","value":"[emoji072]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-073.png","value":"[emoji073]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-074.png","value":"[emoji074]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-075.png","value":"[emoji075]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-076.png","value":"[emoji076]"},{"icon":"https://www.ear0.com/public/images/emoticon/emoji-077.png","value":"[emoji077]"}]}};
            cxeditor.config.menus = ['emotion','bold','italic','strikethrough','eraser','link','unlink'];
            cxeditor.config.pasteText = true;        //仅粘贴为纯文本
            cxeditor.config.uploadImgUrl = "https://www.ear0.com/index.php?app=pubs&ac=plugin&plugin=editor&in=upload&item=sound_commemt&cx=photo";
            cxeditor.config.uploadImgFileName = "photo";
            cxeditor.create();
        });
	</script>
</div>

<div class="clear"></div>

<div class="clear mb50"></div>
<div class="footer">

<p>
    <a href="https://www.ear0.com/home/info/keyword-license">许可协议</a> |
    <a href="https://www.ear0.com/home/info/keyword-standard">声音规范</a> |
    <a href="https://www.ear0.com/home/info/keyword-copyright">版权声明</a> |
    <a href="https://www.ear0.com/home/info/keyword-agreement">用户条款</a> |
    <a href="https://www.ear0.com/home/info/keyword-private">隐私申明</a> |
    <a href="https://www.ear0.com/home/info/keyword-about">关于我们</a> |
    <a href="https://www.ear0.com/article/read">相关阅读</a>
</p>

<p>
    Copyright © 2013-2019    <a target="_blank" href="https://www.ear0.com/">耳聆网</a> All Rights Reserved
    <a class="c9" rel="external nofollow" href="http://www.miitbeian.gov.cn/">粤ICP备14013323号</a>
</p>

<!--	<p><span style="font-size:0.83em;">Processed in 0.001784 second(s)</span></p>		-->

</div>

<script src="https://www.ear0.com/public/js/common.js" type="text/javascript"></script>

<script src="https://www.ear0.com/app/sound/js/extend.func.js" type="text/javascript"></script>

<script src="https://www.ear0.com/public/js/sweetalert/sweet-alert.min.js" type="text/javascript"></script>
<link rel="stylesheet" href="https://www.ear0.com/public/js/sweetalert/sweet-alert.css" type="text/css">

<script src="https://www.ear0.com/public/js/layer/layer.min.js"></script>

<script src="https://www.ear0.com/public/js/legitRipple/ripple.min.js" type="text/javascript"></script>
<link rel="stylesheet" href="https://www.ear0.com/public/js/legitRipple/ripple.min.css" type="text/css">

<script src="https://www.ear0.com//public/js/raty/jquery.raty.js" type="text/javascript"></script>

<script src="https://www.ear0.com/public/js/background-blur/background-blur.min.js" type="text/javascript"></script>

<script src="https://www.ear0.com/public/js/wordcloud2/wordcloud2.min.js" type="text/javascript"></script>

<link href="https://www.ear0.com/public/js/wangEditor/css/wangEditor.min.css" type="text/css" rel="stylesheet" />
<script src="https://www.ear0.com/public/js/wangEditor/wangEditor.min.js" type="text/javascript"></script>

<link href="https://www.ear0.com/public/js/share/css/share.min.css" type="text/css" rel="stylesheet" />
<script src="https://www.ear0.com/public/js/share/js/jquery.share.min.js" type="text/javascript"></script>

<script src="https://www.ear0.com/public/js/randomColor/randomColor.min.js" type="text/javascript"></script>
<script src="https://www.ear0.com/public/js/mousetrap/mousetrap.min.js" type="text/javascript"></script>

<!--[if lt IE 9]>
<script src="https://www.ear0.com/public/js/rem/rem.min.js" type="text/javascript"></script>
<![endif]-->

<!--[if lt IE 8]>
<script src="https://www.ear0.com/public/js/anti-ie/anti-ie.js" type="text/javascript"></script>
<![endif]-->

<link href="https://www.ear0.com/public/css/iconfont/iconfont.css" type="text/css" rel="stylesheet" />

<style type="text/css">
    .feedback{position:fixed;right:0;top:30%;text-align:center;width:20px;height:auto;padding:8px 6px;z-index:100;background-color:#1B9FE0;opacity:0.6;filter:alpha(opacity=60); }
    .feedback:hover{opacity:1;filter:alpha(opacity=100);transition:all 0.2s;}
    .feedback a{color:#FFFFFF;font-size: 12px;}
    .sidebar{position:fixed;width:48px;height:auto;right:0;bottom:10%;z-index:100;display:none;}
    .sidebar ul li{width:48px;height:48px;line-height:48px;float:left;position:relative;}
    .sidebar ul li .sidebox{position:absolute;width:48px;height:48px;top:0;right:0;transition:all 0.3s;background:#c8c8c8;color:#fff;font-size:14px;overflow:hidden;}
    .sidebar ul li .sidetop{width:48px;height:48px;line-height:48px;display:inline-block;background:#c8c8c8;transition:all 0.3s;}
    .sidebar ul li .sidetop:hover{background:#ffa07a;}
    .sidebar ul li img{float:left;width:28px;height:28px;padding:10px;}
</style>
<!--测试期间显示feedback-->
<div class="feedback">
    <a href="https://www.ear0.com/home/feedback">
        意<br>见<br>反<br>馈<br>
        <img class="w100 mt5" src="https://www.ear0.com/plugins/pubs/sidebar/images/feedback.png" />
    </a>
</div>
<div class="sidebar">
    <ul>
        <!--//隐藏图标
        <li><a href="https://www.ear0.com/article/help"><div class="sidebox"><img src="https://www.ear0.com/plugins/pubs/sidebar/images/help.png">帮助中心</div></a></li>
        -->
        <li><a href="https://www.ear0.com/home/feedback"><div class="sidebox"><img src="https://www.ear0.com/plugins/pubs/sidebar/images/feedback.png">意见反馈</div></a></li>
        <li><a href="javascript:void(0);" onclick="donate();"><div class="sidebox"><img src="https://www.ear0.com/plugins/pubs/sidebar/images/donate.png">捐助平台</div></a></li>
        <li style="border:none;"><a href="javascript:goTop();" class="sidetop"><img src="https://www.ear0.com/plugins/pubs/sidebar/images/top.png"></a></li>
    </ul>
</div>

<script type="text/javascript">

    $(document).ready(function(){

        show_sidebar();
        $(window).bind("scroll resize",function(){
            show_sidebar();
        });

        $(".sidebar ul li").hover(function(){
            $(this).find(".sidebox").stop().animate({"width":"120px"},200).css("background","#5d78aa");
        },function(){
            $(this).find(".sidebox").stop().animate({"width":"48px"},200).css("background","#c8c8c8");
        });

    });

    //回到顶部
    function goTop(){
        $('html,body').animate({'scrollTop':0},600);
        $(this).blur();
    }

    function show_sidebar(){
        var showTime;
        $('.sidebar').hide();
        clearTimeout(showTime);
        showTime = setTimeout(function(){
            if($(window).scrollTop() >= $(window).height()/2){
                $('.sidebar').fadeIn();
            }
        },800);
    }

</script>
<!--百度统计和url推送代码-->
<script>
    //百度统计代码
    var _hmt = _hmt || [];
    (function() {
        var hm = document.createElement("script");
        hm.src = "https://hm.baidu.com/hm.js?ca7878677a94bf7a293315510fd64fd1";
        var s = document.getElementsByTagName("script")[0];
        s.parentNode.insertBefore(hm, s);
    })();

    //百度搜索url推送代码
    (function(){
        var bp = document.createElement('script');
        var curProtocol = window.location.protocol.split(':')[0];
        if (curProtocol === 'https'){
            bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
        }
        else{
            bp.src = 'http://push.zhanzhang.baidu.com/push.js';
        }
        var s = document.getElementsByTagName("script")[0];
        s.parentNode.insertBefore(bp, s);
    })();

    //360搜索url推送代码
    (function(){
        var src = (document.location.protocol == "http:") ? "http://js.passport.qihucdn.com/11.0.1.js?c8e5c854da741bfe36b5608d83bbf40c":"https://jspassport.ssl.qhimg.com/11.0.1.js?c8e5c854da741bfe36b5608d83bbf40c";
        document.write('<script src="' + src + '" id="sozz"><\/script>');
    })();
</script>

</body>
</html>'''
    dom_to_tuple(parse(html))
