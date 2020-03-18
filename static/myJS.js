function Control(x, id){
    if(x=='start'){
        document.getElementById(id).play();
    }else{
        document.getElementById(id).load();
    }
}

function playByPlayer(_id, _videoPath){
    var xmlhttp;
    xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState==4 && xmlhttp.status==200){
            if (xmlhttp.responseText=="No set player"){
                alert('尚未設定播放器')
            }else{
                var _newUserVideoInfo = xmlhttp.responseText.split(',');
                document.getElementById(_id[0]).innerHTML = _newUserVideoInfo[0];
                document.getElementById(_id[1]).innerHTML = _newUserVideoInfo[1];
            }
        }
    }
    xmlhttp.open("GET","/playByPlayer?videoPath="+_videoPath,true);
    xmlhttp.send();
}

function setPlayerPathGUI(){
    stopWeb();
    var _xmlhttp;
    _xmlhttp = new XMLHttpRequest();
    _xmlhttp.onreadystatechange=function(){
        if (_xmlhttp.readyState==4 && _xmlhttp.status==200){
            var _HTML = '';
            var _json = eval( "(" + _xmlhttp.responseText + ")" );
            for(i=0; i<_json.playerList.length; i++){
                var _playerStr = _json.playerList[i][0];
                var _playerPath = _json.playerList[i][1];
                _playerPath = _playerPath.replace(/\\/g, '/');
                _HTML += '<div id="' + _playerStr + '" class="selectVideoPathItem" onclick="setPlayerPath(\'setPlayerPath\', \'' + _playerPath + '\')">' + _playerStr + '</div>';
            }
            document.getElementById("showLog").innerHTML = _HTML;

            var _showLogHeight = _json.playerList.length*(30+22);
            var _newWindow = _showLogHeight + 60;
            document.getElementById("newWindow").style = "top:20%;left:35%;width:30%;height:" + _newWindow + "px;";
            document.getElementById("newWindow").style.display = "block";
            document.getElementById("showLog").style = "border:0px;overflow:hidden;width:95%;height:" + _showLogHeight + "px;";
            document.getElementById("showLog").style.display = "block";
            document.getElementById("btnBrowse").style.display = "block";
            document.getElementById("btnOK").style.display = "none";
            //document.getElementById("processDegree").style.display = "none";
            document.getElementById("processDegreeBorder").style.display = "none";
        }
    }
    _xmlhttp.open("GET","/setPlayer?action=showSetting",true);
    _xmlhttp.send();
}

function setPlayerPath(_action, _playerPath=''){
    var _xmlhttp;
    _xmlhttp = new XMLHttpRequest();
    _xmlhttp.onreadystatechange=function(){
        if (_xmlhttp.readyState==4 && _xmlhttp.status==200){
            document.getElementById("playerPath").innerHTML = _xmlhttp.responseText;
            document.getElementById("newWindow").style.display = "none";
            avtiveWeb();
        }
    }
    _xmlhttp.open("GET","/setPlayer?action=" + _action + "&playerPath=" + _playerPath, true);
    _xmlhttp.send();
}

var isSideMenuOpen = new Boolean(false);
var oldOpenTable = '';
function showVideoTag(_id, _videoPath){
    var _videoId = _id.split("_");
    _tagTxtID = "tagTxtID_" + _videoId[1];
    _videoNameId = "videoName_" + _videoId[1];
    _videoTableId = "videoTable_" + _videoId[1];
    cancelAllSelect();
    document.getElementById("editTagVideoName").innerHTML = document.getElementById(_videoNameId).title;
    document.getElementById("editTagVideoName").style.color = "#FF5C0F";
    document.getElementById("editTagVideoName").style.fontweight = "bolder";
    document.getElementById(_tagTxtID).style = "color:#FF9460; font-weight:bold; font-size:15px;";
    document.getElementById(_videoTableId).style.border = "solid 5px #FF9460";
    document.getElementById(_videoTableId).style.boxShadow = "5px 5px 8px rgba(10%,10%,10%,0.8)";
    document.getElementById(_videoTableId).style.borderRadius = "0px 0px 15px 15px";

    if( oldOpenTable == _videoTableId ){
        if( isSideMenuOpen ){
            isSideMenuOpen = false;
            closeSideMenu();
            document.getElementById("editTagVideoName").innerHTML = '';
            document.getElementById(_videoTableId).style.border = "0px";
            document.getElementById(_videoTableId).style.boxShadow = "0px 0px 0px rgba(20%,20%,20%,0)";
            updateTagShow('showAllTag', '', '', '');
            return true;
        }else{
            isSideMenuOpen = true;
            openSideMenu();
        }
    }else{
        isSideMenuOpen = true;
        openSideMenu();
        oldOpenTable = _videoTableId;
    }
    updateTagShow('showVideoTag', _id, _videoPath, '');
}

var isNowEdit = new Boolean(false)
function editAllTag(){
    if(isNowEdit == false){
        isNowEdit = true;
        document.getElementById("clickEditTag").innerHTML = '[完成]';
        cancelAllSelect();
        updateTagShow('edit', '', '', '');
    }else{
        isNowEdit = false;
        document.getElementById("clickEditTag").innerHTML = '[編輯]';
        updateTagShow('showAllTag', '', '', '');
    }

}

function cancelAllSelect(){
    document.getElementById("editTagVideoName").innerHTML = '';
    var videoTableList = document.getElementsByName('videoTable');
    var tagTxtList = document.getElementsByClassName('flipTag');
    for (i = 0; i < videoTableList.length; i++) {
            videoTableList[i].style.border = "0px";
            videoTableList[i].style.boxShadow = "0px 0px 0px rgba(20%,20%,20%,0)";
    }
    for (i = 0; i < tagTxtList.length; i++) {
            tagTxtList[i].style = "color:#000; font-weight:normal;";
    }
    updateTagShow('showAllTag', '', '', '');
}

function addVideoTag(_id, _videoPath, _newTag){
    updateTagShow('add', _id, _videoPath, _newTag);}

function deleteVideoTag(_id, _videoPath, _Tag){
    updateTagShow('delete', _id, _videoPath, _Tag);}

function addNewTagToDB(_id, _videoPath){
    _newTag = document.getElementById("newTagFromVideo").value;
    if( _newTag != '' ){
        updateTagShow('add', _id, _videoPath, _newTag);
    }else{
        alert('請輸入標籤名稱');
    }
}

function editAddNewTagToDB(_id){
    _newTag = document.getElementById("newTagFromEdit").value;
    if( _newTag != '' ){
        updateTagShow('editAdd', _id, '', _newTag);
    }else{
        alert('請輸入標籤名稱');
    }
}
function editDeleteTagFromDB(_tag){
    updateTagShow('editDelete', '', '', _tag);
}
function editChangeTagFromDB(_id, _tag){
    var _newTag = document.getElementById("tag_" + _id).value;
    var _tagChange = _tag + ',' + _newTag
    updateTagShow('editChange', '', '', _tagChange);
}

function updateTagShow(_action, _id, _videoPath, _newTag){
    var _xmlhttp;
    _xmlhttp = new XMLHttpRequest();
    _xmlhttp.onreadystatechange=function(){
        if (_xmlhttp.readyState==4 && _xmlhttp.status==200){
            var _webReturnData;
            document.getElementById("editTag").innerHTML = _xmlhttp.responseText;
            var _responseStr = _xmlhttp.responseText;
            _tagNum = getInnerHTMLfromCloseTag(_responseStr, '<tagNum>');
            document.getElementById(_id).innerHTML = _tagNum;
            var _videoTag = document.getElementById("tagList").innerHTML;
            _videoTag = _videoTag.substring(1, _videoTag.length-1);
            _videoTag = _videoTag.replace(new RegExp('\'', 'g'), '');
            document.getElementById("videoTag").innerHTML = _videoTag;
        }
    }
    _xmlhttp.open("GET","/editTag?action="+_action+"&id="+_id+"&videoPath="+_videoPath+"&newTag="+_newTag, true);
    _xmlhttp.send();
}

function openSideMenu() {
    getSysInfo();
    document.getElementById("videoList").style.marginLeft = "300px";
    document.getElementById("videoList").style.width = "70%";
    document.getElementById("sideMenu").style.width = "300px";
}
function closeSideMenu() {
    cancelAllSelect();
    document.getElementById("videoList").style.marginLeft = "0%";
    document.getElementById("videoList").style.width = "80%";
    document.getElementById("sideMenu").style.width = "0px";
}

function getSysInfo(){
    var _xmlhttp;
    _xmlhttp = new XMLHttpRequest();
    _xmlhttp.onreadystatechange = function(){
        if (_xmlhttp.readyState==4 && _xmlhttp.status==200){
            var _jsonData = eval( "(" + _xmlhttp.responseText + ")" );
            document.getElementById("playerPath").innerHTML = _jsonData.playerPath;
            document.getElementById("totalVideoNum").innerHTML = _jsonData.videoNum;
            var _videoPathListToWeb = "";
            for( i=0; i<_jsonData.videoPathList.length; i++ ){
                _videoPathListToWeb += _jsonData.videoPathList[i] + "<br>";
            }
            document.getElementById("videoPathList").innerHTML = _videoPathListToWeb;
        }
    }
    _xmlhttp.open("GET","/getSysInfo",true);
    _xmlhttp.send();
}

function toggleSideMenu(){
    var sideMenuOpenStatus = document.getElementById("sideMenu").style.width;
    if( sideMenuOpenStatus == '300px' ){

        closeSideMenu();
    }else{
        openSideMenu();
    }
}

function stopWeb(_URL=''){
    var _body = document.getElementsByTagName('body');
    var _html = document.getElementsByTagName('html');
    var _mask = document.getElementById('mask');
    _body[0].style = "overflow-x:hidden;overflow-y:hidden;";
    _html[0].style = "overflow-x:hidden;overflow-y:hidden;";
    _mask.style.display = "block";
    if( _URL!='' )
        reDirect(_URL);
}

function reDirect(_URL){
    document.location.href = _URL;
}

function getInnerHTMLfromCloseTag(_inputStr, _startTag){
    var _endTag = _startTag.replace('<', '</');
    var _startTagIdx = _inputStr.indexOf(_startTag);
    var _endTagIdx = _inputStr.indexOf(_endTag);
    return _inputStr.substring(_startTagIdx+_startTag.length, _endTagIdx);
}

function inputChanged(_id){
    var _originalName = document.getElementById(_id).name;
    var _newName = document.getElementById(_id).value;
    var _tagId = _id.split("_");
    _tagId = "tagChangeIcon_" + _tagId[1];
    if( _originalName != _newName ){
        document.getElementById(_id).style.background = "#FFFF8C";
        document.getElementById(_tagId).style.display = "inline-block";
    }else{
        document.getElementById(_id).style.background = "#FFFFFF";
        document.getElementById(_tagId).style.display = "none";
    }
}

function loadTopSearch(){
    var _xmlhttp;
    _xmlhttp = new XMLHttpRequest();
    _xmlhttp.onreadystatechange = function(){
        if (_xmlhttp.readyState==4 && _xmlhttp.status==200){
            document.getElementById("topSearch").innerHTML = _xmlhttp.responseText;
        }
    }
    _xmlhttp.open("GET","/topSearch", true);
    _xmlhttp.send();
}

function loadSideMenu(){
    var _xmlhttp;
    _xmlhttp = new XMLHttpRequest();
    _xmlhttp.onreadystatechange = function(){
        if (_xmlhttp.readyState==4 && _xmlhttp.status==200){
            document.getElementById("sideMenu").innerHTML = _xmlhttp.responseText;
        }
    }
    _xmlhttp.open("GET","/sideMenu", true);
    _xmlhttp.send();
}

function textLenMAX(_targetName, _length){
    var _fullCharPxLength = 16;
    var _halfCharPxLength = 8;
    var _displayMAXlength = _length;
    var _videoNameList = document.getElementsByName(_targetName);
    for( i=0; i<_videoNameList.length; i++ ){
        var _videoName = _videoNameList[i].innerHTML;
        var _charRealPxLength = 0;
        var _newVideoName = '';
        for(var j=0; j<_videoName.length; j++){
            _newVideoName += _videoName[j];
            if( _videoName.charCodeAt(j) >= 255 ){
                _charRealPxLength += _fullCharPxLength;
            }else{
                _charRealPxLength += _halfCharPxLength;
            }
            if( _charRealPxLength>=_displayMAXlength ){
                _newVideoName += ' ...';
                break;
            }
        }
        _videoNameList[i].innerHTML = _newVideoName;
    }
}

function makeTrailer(){
    stopWeb();
    var _xmlhttp;
    _xmlhttp = new XMLHttpRequest();
    _xmlhttp.onreadystatechange = function(){
        if (_xmlhttp.readyState==4 && _xmlhttp.status==200){
            _HTML = _xmlhttp.responseText;
            if( _HTML == 'cancel' ){
                avtiveWeb();
            }else{
                document.getElementById("newWindow").style = "top:10%;left:10%;width:80%;height:80%;";
                document.getElementById("newWindow").style.display = "block";
                document.getElementById("showLog").style = "border:solid 1px #DDD;overflow:suto;width:95%;height:83%;";
                document.getElementById("showLog").style.display = "block";
                document.getElementById("btnBrowse").style.display = "none";
                document.getElementById("btnOK").style.display = "none";
                //document.getElementById("processDegree").style.display = "block";
                document.getElementById("processDegree").style.width = '0%';
                document.getElementById("processDegreeBorder").style.display = "block";
                document.getElementById("showLog").innerHTML = _xmlhttp.responseText;
                waitUntilMakeTrailerOK();
            }
        }
    }
    _xmlhttp.open("GET","/addNewVideo?action=newPath", true);
    _xmlhttp.send();
}

var _startMakeTrailer = new Boolean(false);
function waitUntilMakeTrailerOK(){
    var _xmlhttp;
    _xmlhttp = new XMLHttpRequest();
    _xmlhttp.onreadystatechange = function(){
        if (_xmlhttp.readyState==4 && _xmlhttp.status==200){
            var _HTML = _xmlhttp.responseText;
            if( _HTML != '' ){
                console.log(_HTML);
                _HTML = _HTML.replace(/\n/g, '<br>');
                document.getElementById("showLog").innerHTML = _HTML;
                document.getElementById("showLog").scrollTop = document.getElementById("showLog").scrollHeight;
                _HTML = _HTML.split('<br>');i
                _HTML = _HTML[_HTML.length-2].split(',');
                if( _HTML[1] == 0 ){
                    document.getElementById("showLog").innerHTML = '找不到影像檔';
                    document.getElementById("processDegree").style.width = '100%';
                    document.getElementById("btnOK").style.display = "block";
                    return;
                }
                var num = new Number((_HTML[0]/_HTML[1])*100);
                num = num.toFixed();
                document.getElementById("processDegree").style.width = num + '%';
                console.log(num + '%');
                if( num >= 100 ){
                    document.getElementById("btnOK").style.display = "block";
                    //clearTimeout(timer);
                }else{
                    var timer = setTimeout("waitUntilMakeTrailerOK()", 100);
                }
            }else{
                var timer = setTimeout("waitUntilMakeTrailerOK()", 100);
            }
        }else{
            if( _startMakeTrailer == false ){
                console.log('?');
                _startMakeTrailer = true;
                document.getElementById("showLog").innerHTML = '<div class="videoNameCSS">Loading...</div>';
            }
        }
    }
    _xmlhttp.open("GET","/addNewVideo?action=chkStatus", true);
    _xmlhttp.send();
}

function avtiveWeb(){
    var _body = document.getElementsByTagName('body');
    var _html = document.getElementsByTagName('html');
    var _mask = document.getElementById('mask');
    _body[0].style = "overflow-x:visible;overflow-y:visible;";
    _html[0].style = "overflow-x:visible;overflow-y:visible;";
    _mask.style.display = "none";
}