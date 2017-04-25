//Get the URL for the page with the given userId, index, and type

function buildURL(userId, index, type) {
    var prefix = 'https://mbasic.facebook.com/';
    var trans;
    if (userId.search(/profile\.php\?id=([0123456789])+/) == -1) {
        trans = '?';
    }
    else {
        trans = '&';
    }
    if(type == "friends") {
        return prefix + userId + trans + 'v=friends&startindex=' + index;
    }
    else if(type == "music") {
        return prefix + userId + trans + 'v=likes&sectionid=13001&startindex=' +  index;
    }
    else if(type == "books") {
        return prefix + userId + trans + 'v=likes&sectionid=13002&startindex=' + index;
    }
    else if(type == "movies") {
        return prefix + userId + trans + 'v=likes&sectionid=13005&startindex=' + index;
    }
    else if(type == "TV") {
        return prefix + userId + trans + 'v=likes&sectionid=13006&startindex=' + index;
    }
    else { //For other likes
        return prefix + userId + trans + 'v=likes&sectionid=9999&startindex=' + index;
    }
}

//Walk through all pages of a given type
function getPages(userId, index, type, done, idToName, nameToId, idsList) {
       function find(text, type){
        if (type == "friends") {
            var $t = $(text);
            var htmlData = $t.find('h3:contains("Friends")').next().next().children().children().children().children();
            var names = htmlData.find('a').map(function (e) {return $(this).text()}).get();
            var htmlIds = htmlData.find('td').map(function (e) {return $(this).html()}).get();
            var ids = [];
            var hIndex;
            
            for(hIndex = 0; hIndex < htmlIds.length; hIndex++) {
                var str = htmlIds[hIndex];
                var charIndex = str.search("<a class=");
                if (charIndex != -1) {
                    var endSection = str.search("</a>");
                    var short = str.substring(charIndex + 13, endSection);
                    var start = short.search("href=");
                    if (start == -1) {
                        ids.push("Deleted"); //this person deleted their Facebook account
                    }
                    else {
                        var end = short.search("fref");
                        var thisId = short.substring(start + 7, end -1).replace(/&amp/g, "");
                        ids.push(thisId);
                    }
                }
            }
            
           // alert(ids);
            if (ids.length != names.length) {
                alert("Size mismatch!");
            }
            var pairs = [];
            var i;
            for (i = 0;  i < ids.length; i++) {
                pairs.push([names[i], ids[i]]);
                if (ids[i] != "Deleted") {
                    idsList.push(ids[i]);
                    idToName[ids[i]] = names[i];
                    nameToId[names[i]] = ids[i];
                }
                else {
                    nameToId[names[i]] = "";
                }
            }
            return pairs;
        }
        else if (type == "music") {
            var $t = $(text);
            var mySet = $t.find('h4:contains("Music")').last().siblings().find('img').siblings();
            var names = mySet.find('span').map(function (e) {
					return $(this).text().replace(/,/g,"")}).get();
            var longer = mySet.map(function (e) {
					return $(this).html()}).get();
            var ids =[];
            var i;
            for (i = 0; i < longer.length; i++) {
                var text = longer[i];
                var endIndex = text.search('fref');
                if(endIndex != -1){
                    ids.push(text.substring(10, endIndex - 2));
                }
            }
            if (names.length != ids.length) {
                alert("length mismatch");
            }
            else {
                var pairs = [];
                var j;
                for (j = 0; j < names.length; j++) {
                    pairs.push([names[j], ids[j]]);
                }
                return pairs;
            }
        }
        else if (type == "books") {
            var $t = $(text);
            var mySet = $t.find('h4:contains("Books ")').last().siblings().find('img').siblings();
            var names = mySet.find('span').map(function (e) {
					return $(this).text().replace(/,/g,"")}).get();
            var longer = mySet.map(function (e) {
					return $(this).html()}).get();
            var ids =[];
           // alert(names);
            var i;
            for (i = 0; i < longer.length; i++) {
                var text = longer[i];
                var endIndex = text.search('fref');
                if(endIndex != -1){
                    ids.push(text.substring(10, endIndex - 2));
                }
            }
            if (names.length != ids.length) {
                alert("length mismatch");
            }
            else {
                var pairs = [];
                var j;
                for (j = 0; j < names.length; j++) {
                    pairs.push([names[j], ids[j]]);
                }
                return pairs;
            }
        }
        else if (type == "movies") {
            var $t = $(text);
            var mySet = $t.find('h4:contains("Movies ")').last().siblings().find('img').siblings();
            var names = mySet.find('span').map(function (e) {
					return $(this).text().replace(/,/g,"")}).get();
            var longer = mySet.map(function (e) {
					return $(this).html()}).get();
            var ids =[];
            //alert(names);
            var i;
            for (i = 0; i < longer.length; i++) {
                var text = longer[i];
                var endIndex = text.search('fref');
                if(endIndex != -1){
                    ids.push(text.substring(10, endIndex - 2));
                }
            }
            if (names.length != ids.length) {
                alert("length mismatch");
            }
            else {
                var pairs = [];
                var j;
                for (j = 0; j < names.length; j++) {
                    pairs.push([names[j], ids[j]]);
                }
                return pairs;
            }
        }
        else if (type == "TV") {
            var $t = $(text);
            var mySet = $t.find('h4:contains("Television ")').last().siblings().find('img').siblings();
            var names = mySet.find('span').map(function (e) {
					return $(this).text().replace(/,/g,"")}).get();
            var longer = mySet.map(function (e) {
					return $(this).html()}).get();
            var ids =[];
            //alert(names);
            var i;
            for (i = 0; i < longer.length; i++) {
                var text = longer[i];
                var endIndex = text.search('fref');
                if(endIndex != -1){
                    ids.push(text.substring(10, endIndex - 2));
                }
            }
            if (names.length != ids.length) {
                alert("length mismatch");
            }
            else {
                var pairs = [];
                var j;
                for (j = 0; j < names.length; j++) {
                    pairs.push([names[j], ids[j]]);
                }
                return pairs;
            }
        }
        else {
            var $t = $(text);
            var mySet = $t.find('h4:contains("Other")').last().siblings().find('img').siblings();
            var names = mySet.find('span').map(function (e) {
					return $(this).text().replace(/,/g,"")}).get();
            var longer = mySet.map(function (e) {
					return $(this).html()}).get();
            var ids =[];
            var i;
            for (i = 0; i < longer.length; i++) {
                var text = longer[i];
                var endIndex = text.search('fref');
                if(endIndex != -1){
                    ids.push(text.substring(10, endIndex - 2));
                }
            }
            if (names.length != ids.length) {
                alert("length mismatch");
            }
            else {
                var pairs = [];
                var j;
                for (j = 0; j < names.length; j++) {
                    pairs.push([names[j], ids[j]]);
                }
                return pairs;
            }
        }
    }
    var url = buildURL(userId, index, type);
    //alert(url);
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.onreadystatechange = function(e) {
        if (xhr.readyState == 4) {
            var text = xhr.responseText;
            //alert(text);
            var pages = find(text, type);
            if (pages.length > 0) {
                getPages(userId, index + pages.length, type, function (morePages) {
                         done(pages.concat(morePages), type);
                         }, idToName, nameToId, idsList);
            }
            else {
                done([], type);
            }
        }
    }
    xhr.send();
}

//Get all of the page likes of a user.
function getAllLikes(userId, done, index, idToName, nameToId, idsList, likeStack)
{
    getPages(userId, 0, "music", done, idToName, nameToId, idsList);
    chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
        if (request.action == "music" && request.id == userId){
        getPages(userId, 1, "books", done, idToName, nameToId, idsList); //This drops the first book displayed
            }
    });
    chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
    if (request.action == "books" && request.id == userId){
    getPages(userId, 1, "movies", done, idToName, nameToId, idsList); //This drops the first movied displayed
        }
    });
    chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
    if (request.action == "movies" && request.id == userId){
    getPages(userId, 1, "TV", done, idToName, nameToId, idsList); //This drops the first show displayed
        }
    });
    chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
        if (request.action == "TV" && request.id == userId){
        getPages(userId, 0, "other", done, idToName, nameToId, idsList);
            }
    });
    chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
        if (request.action == "other" && request.id == userId){
            //alert(index);
            if (index%10 == 9 && index != 0) {
                alert((index + 1) + " profiles analyzed");
            }
            if (likeStack.length > 15000){
                alert("Trying Pop");
                //var header = [["Number of Points:", likeStack.length],["personName:", "personid:", "pageName:", "pageid:"]];
                var header = [["personName", "personid", "pageName", "pageid"]];
                var data = header.concat(likeStack);
                //alert(data); //for debugging
                var csvContent = "data:text/csv;charset=utf-8,";
                data.forEach(function(infoArray, index){
                    dataString = infoArray.join(",");
                    csvContent += index < data.length ? dataString+ "\n" : dataString;

                }); 
                //csvContent += data.join(",");
                //alert(csvContent);
                var myCSV = encodeURI(csvContent);
                var link = document.createElement("a");
                link.setAttribute("href", myCSV);
                var yourName = idToName[idsList[0]];
                link.setAttribute("download", yourName + " allLikes.csv");
                document.body.appendChild(link);
                link.click();
                while(likeStack.length != 0) {
                    likeStack.pop();
                }
            }
            chrome.runtime.sendMessage({action: String("doNext " + index),
                                       id: -1});
            //alert("ready");
            //alert(idsList.length);
            if (index == (idsList.length - 1)) {
                chrome.runtime.sendMessage({action: "All Likes Done",
                                           id: -1});
            }
        }
    });
}

//Get all friends of a user, including the user
function getFriends(raw, idToName, nameToId, idsList) {
	var xhr = new XMLHttpRequest();
	xhr.open('GET', 'https://www.facebook.com', true);
	xhr.onreadystatechange = function (e) {
		if (xhr.readyState == 4) {
			var text = xhr.responseText;
            
             //Get the owner's name, Facebook id, url
            var headIndex = text.search("fbxWelcomeBoxName");
            
            var tailIndex = text.search("fb_welcome_box");
            var short = text.substring(headIndex + 17, tailIndex + 1000);
            var idHead = short.search("href=");
            var longID = short.substring(idHead + 31, short.length);
            var idTail = longID.search("ref=bookmarks");
            var id = longID.substring(0, idTail - 1);
            var longName = short.substring(short.search("fb_welcome_box") + 16, short.length);
            var rawName = longName.substring(0, longName.search("</a>"));
            var name = rawName.replace(/&#039;/g, "\'");
            var idNamePairs = [];
            raw.push([name, id]);
            idToName[id] = name;
            nameToId[name] = id;
            idsList.push(id);
            
            getPages(id, 0, "friends", function(data) {
                data.forEach(function(item){raw.push(item);});
                chrome.runtime.sendMessage({
                action: "Friends Done",
                    id: -1
                });  
            },idToName, nameToId, idsList);
        }
	}
	xhr.send();
}

//Execute when requested by extension
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
    if(request.action == "parse"){
        alert("Analysis started!");
        var rawData = [];
        var idToName = {};
        var nameToId = {};
        var idsList = [];
        var likeStack = [];
        //alert(rawData);
        getFriends(rawData, idToName, nameToId, idsList);
        chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
            if(request.action == "Friends Done") {
                alert(request.action);
                    
                //var testPerson = [];
                //testPerson.push(nameToId["First Last"]);
                /*testPerson.push(nameToId["First Last"]);
                testPerson.push(nameToId["First Last"]);
                testPerson.push(nameToId["First Last"]);*/
                //idsList = testPerson;
                //alert(idsList);
                /*var i;
                var short = [];
                for (i = 0; i < 14; i++)
                    {
                        short.push(idsList[i]);
                    } 
                idsList = short;*/
                
                idsList.forEach(function(person, index) {
                    //alert(index);
                    if (index == 0) {
                        getAllLikes(person, function(data, type){
                            data.forEach(function(item){
                                likeStack.push([idToName[person], person, item]);
                            });
                            chrome.runtime.sendMessage({action: type,
                                                       id: person});
                        }, index, idToName, nameToId, idsList, likeStack);
                    }
                    else {
                        chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
                            if (request.action == String("doNext " + (index - 1))) {
                                //alert(idToName[person]);
                                getAllLikes(person, function(data, type){
                                data.forEach(function(item){
                                    likeStack.push([idToName[person], person, item]);
                                });
                                chrome.runtime.sendMessage({
                                    action: type,
                                    id: person});
                                }, index, idToName, nameToId, idsList, likeStack);  
                            }
                        });
                    }
                });
            }
    });
        //Save csv's
                chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
            if(request.action == "All Likes Done") {
                alert(request.action);
                // To make it easier for pandas, remove first part of header
                // var header = [["Number of Points:", likeStack.length], ["personName:", "personid:", "pageName:", "pageid:"]];
                var header = [["personName", "personid", "pageName", "pageid"]];
                var data = header.concat(likeStack);
                //alert(data); //for debugging
                var csvContent = "data:text/csv;charset=utf-8,";
                data.forEach(function(infoArray, index){
                    dataString = infoArray.join(",");
                    csvContent += index < data.length ? dataString+ "\n" : dataString;

                }); 
                //csvContent += data.join(",");
                //alert(csvContent);
                var myCSV = encodeURI(csvContent);
                var link = document.createElement("a");
                link.setAttribute("href", myCSV);
                var yourName = idToName[idsList[0]];
                link.setAttribute("download", yourName + " allLikes.csv");
                document.body.appendChild(link);
                link.click();
                var firstName = yourName.substring(0, yourName.search(" "));
                alert("Thanks " + firstName + "!"); //Please send csv's to adam.hare@worc.ox.ac.uk");
            }
        });
    }
});