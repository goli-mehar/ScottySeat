"use strict"
var refreshrate = 10000
var windowid = 0

var mapwidth = 640
var mapheight = 480
var occupied_color = '#914040'
var available_color = '#409143'
var persepctiveRatio = 250/490
var response = {}
var order = "available"

function initialize() {
    let map = document.getElementById("game")
    map.style.width = mapwidth + "px"
    map.style.height = mapheight + "px"
    let header = document.getElementById("header")
    header.style.width = mapwidth + "px"
    let footer = document.getElementById("footer")
    footer.style.width = mapwidth + "px"
    sendRoomRequest(event)
    windowid = window.setInterval(sendRoomRequest, refreshrate, event)
}

function sendRoomRequest(event) {
    displayError('')
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }
    xhr.open("POST", MoveURL, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("roomname="+roomname+"&csrfmiddlewaretoken="+getCSRFToken());
}

function changeOrder() {
    order = document.getElementById("order").value
    console.log(order)
    updateRoom(response)
}
function updateRoom(itemlist) {
    console.log(itemlist)
    let rooms = document.getElementById("roomlist");
    let initialized = false;
    let temp_list = [];
    while (rooms.hasChildNodes()) {
        rooms.removeChild(rooms.firstChild);
    }
    for (let room in itemlist) {
        temp_list.push(room)
    }
    console.log(temp_list)
    temp_list.sort(function(a,b){
        if (itemlist[a][order] > itemlist[b][order]){
            return -1;
        }
        if (itemlist[a][order] < itemlist[b][order]){
            return 1;
        }
        return 0;
    });
    console.log(itemlist)
    console.log(temp_list)
    for (var i = 0; i < temp_list.length; i++) {
        if (temp_list[i] == roomname){
            initialized = true;
        }
        let roominfo = document.createElement("UL");
        roominfo.innerHTML = temp_list[i] + '&nbsp&nbsp&nbsp' + '<span style="color:' + occupied_color + '">' + itemlist[temp_list[i]].occupied + '</span>' + "&nbsp&nbsp&nbsp" + '<span style="color:' + available_color + '">' + itemlist[temp_list[i]].available + '</span>';
        roominfo.id = temp_list[i];
        roominfo.className = "roomlist_item"
        roominfo.onclick = function() {changeCurRoom(this.id)};
        rooms.appendChild(roominfo);
    }
    console.log(temp_list)
    if (!initialized){
        roomname = temp_list[0]
        let title = document.getElementById("roomname")
        title.innerHTML = roomname
    }

}
function changeCurRoom(id) {
    roomname = id
    let title = document.getElementById("roomname")
    title.innerHTML = id
    // console.log(roomname)
    updateMap(response)

}
function updateMap(itemlist) {
    // for (var j = 0; j < itemlist.room.length; j++){
    console.log(roomname)
    console.log(itemlist[roomname])
    let items = itemlist[roomname]
    let seatscount = items.seatscount
    let seatsposition = items.seatsposition
    let personorchair = items.personorchair
    // let tablecount = items.room.tablecount
    // let tablesposition = items.room.tablesposition.split(',')
    let peoplecount = items.personscount
    let occupied = items.occupied
    let available = items.available
    // let peopleposition = items.room.peopleposition.split(',')
    let occupancy = items.occupancy
    let tables = items.tablesposition
    let tablecount = items.tablecount
    // mapwidth = items.w
    // mapheight = items.h
    // console.log(mapwidth)
    // remove chairs and tables from previous update
    let map = document.getElementById("game")
    while (map.hasChildNodes()) {
        map.removeChild(map.firstChild)
    }
    document.getElementById("occupied").innerHTML = 'Occupied : ' + '<span style="color:' + occupied_color + '">' + occupied + '</span>'
    document.getElementById("available").innerHTML = 'Available : ' + '<span style="color:' + available_color + '">' + available + '</span>'
    console.log(seatsposition)
    for (let i = tablecount - 1; i >= 0; i--){
        console.log(tablecount)
        let element = document.createElement("div")
        element.id = 'table_' + i
        element.style.background = 'repeating-linear-gradient(45deg,#ababab, #ababab 3px,lightgray 3px,lightgray 18px)'
        // element.style.backgroundColor =
        element.style.position = "absolute"
        element.style.border= '3px solid #ababab'
        element.style.borderRadius = '12.5px'
        // element.style.width = '100px'
        // element.style.height = '50px'
        // element.style.top = (tables[i][0]) + 'px'
        // element.style.left = (mapwidth - tables[i][1]) + 'px'
        // element.style.height = tables[i][2] + 'px'
        // element.style.width = tables[i][3] + 'px'
        element.style.top = (tables[i][1] - tables[i][3]) + 'px'
        element.style.left = (tables[i][0]) + 'px'
        element.style.height = tables[i][3] + 'px'
        element.style.width = tables[i][2] + 'px'
        map.appendChild(element)
    }
    console.log(seatscount + peoplecount - 1)
    for (let i = seatscount + peoplecount - 1; i >= 0; i--){
        console.log(i)
        let ob = personorchair[i]
        // w = seatsposition[i]
        // h = seatsposition[i]
        let element = document.createElement("div")
        if (ob == "0"){
            let av = occupancy[i]
            let x = seatsposition[i][0]
            let y = seatsposition[i][1]
            element.id = 'chair_' + i
            if (av){
                element.style.backgroundColor = '#409143'
            }
            else{
                element.style.backgroundColor = '#914040'
            }
            element.style.borderRadius = '50%'
            element.style.position = "absolute";
            element.style.width = '25px'
            element.style.height = '25px'
            element.style.top = (y - 12.5) + 'px'
            element.style.left = (x - 12.5) + 'px'
        }
        map.appendChild(element)
    }
        // console.log(Date.now())
}

function updatePage(xhr) {
    if (xhr.status == 200) {
        response = JSON.parse(xhr.responseText)
        updateRoom(response)
        updateMap(response)
        return
    }

    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }


    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }
    displayError(response)
}

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}