"use strict"
var refreshrate = 10000
var windowid = 0

var mapwidth = 800
var mapheight = 500
var occupied_color = '#914040'
var available_color = '#409143'
var persepctiveRatio = 250/490


function initialize() {
    let map = document.getElementById("game")
    map.style.width = mapwidth + "px"
    map.style.height = mapheight + "px"
    let header = document.getElementById("header")
    header.style.width = mapwidth + "px"
    let footer = document.getElementById("footer")
    footer.style.width = mapwidth + "px"
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

// function straighten(x, y){
//     let e = ((1-persepctiveRatio) * mapheight)/2
//     e = ((mapwidth - y)/mapwidth) * e
//     if (x <= e) return [0, y]
//     if (x >= (mapheight - e)) return [mapheight, y]
//     let newx = ((x - e)/(mapheight - 2*e))*mapheight
//     let f = (mapwidth/(mapwidth - 2*e)) * y
//     if (f >= mapwidth) f = mapwidth
//     return [newx, f]
// }

function updateMap(items) {
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
    // mapwidth = items.w
    // mapheight = items.h
    // console.log(mapwidth)
    // remove chairs and tables from previous update
    let map = document.getElementById("game")
    // let nodes = map.childNodes;
    // for (let p = 0; p < nodes.length; p++){
    //     nodes[p].firstChild.removeAttribute("style")
    // }
    while (map.hasChildNodes()) {
        map.removeChild(map.firstChild)
    }
    document.getElementById("occupied").innerHTML = 'Occupied : ' + '<span style="color:' + occupied_color + '">' + occupied + '</span>'
    document.getElementById("available").innerHTML = 'Available : ' + '<span style="color:' + available_color + '">' + available + '</span>'
    console.log(seatsposition)
    for (let i = seatscount + peoplecount - 1; i >= 0; i--){
        let x = seatsposition[i][0]
        let y = seatsposition[i][1]
        let ob = personorchair[i]
        let av = occupancy[i]
        // w = seatsposition[i]
        // h = seatsposition[i]
        let element = document.createElement("div")
        if (ob == "56"){
            element.id = 'chair_' + i
            if (av){
                element.style.backgroundColor = '#409143'
            }
            else{
                element.style.backgroundColor = '#914040'
            }
        }
        // person case, in final version person won't be displayed
        // else{
        //     element.id = 'person_' + i
        //     element.style.backgroundColor = '#905010'
        // }
        element.style.borderRadius = '50%'
        element.style.position = "absolute";
        element.style.width = '25px'
        element.style.height = '25px'
        // let mapx = x * mapheight
        // let mapy = y * mapwidth
        // mapx = straighten(mapx, mapy)[0]
        // mapy = straighten(mapx, mapy)[1]
        // console.log(mapx)
        // console.log(mapy)
        element.style.top = x + 'px'
        element.style.right = y + 'px'
        map.appendChild(element)
    }
    // console.log(Date.now())
}

function updatePage(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
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

    let response = JSON.parse(xhr.responseText)
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