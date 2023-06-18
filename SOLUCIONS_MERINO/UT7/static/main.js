// .......................................................
// INICIALITZACIO
// .......................................................

var serverAPI = "http://87.235.201.250:8080/whatspau_php";
var IdusuariActual = 0;
var usuaris;
var token;
var missatges;

// RECUPERAM TOKLEN

token = $.cookie("JWT");

// .......................................................
// FUNCIO QUE  CARREGA LES DADES DESDE LA API
// .......................................................

// FUNCIO QUE DEMANA XAT AMB UN USUARI-GRUP

function carregaConversaSegonsContacte(idUser) {
    console.log(idUser);
    // RECUPERAM NOM DE L'AMIC
    let username = document.getElementById(idUser).innerText;
    console.log(username);

    // RECUPERAM MISSATGES CONVERSA
    url = "http://87.235.201.250:8080/whatspau_php/missatges/" + idUser;
    var ajax1 = $.ajax({
        url: url,
        type: "GET",
        dataType: "json",
        headers: { Authorization: token },
    }).done(function (json) {
        conversa = json;
        console.log(conversa);

        // PINTAM LA CONVERSA
        var str = pintaConversa(username, idUser, conversa);
        document.getElementById("missatgesSection").innerHTML = str;
        //FEIM SCROLL A TOP PÀGINA
        window.scrollTo(0, 0);

        // CANVIAM STATUS MISSATGES REBUTS A READ
        canviaStatusToRead(conversa, idUser);

        // ACTUALITZAM NUM. MISSATGES NOUS
        // CAPTURAM ELEMENT A MODIFICAR
        var idElement = document.getElementById("numNous-" + idUser);
        // MODIFICAM ELEMENT
        idElement.classList.remove("table-success");
        idElement.innerHTML = "0";
    });
}

// FUNCIÓ QUE PINTA LA CONVERSA AMB USUARI SELECCIONAT
function pintaConversa(username, idUser, conversa) {
    var str;
    str = "<div class='col-sm-8'>";
    str += "<div class='alert alert-success' role='alert'>";
    str += "Xat amb <STRONG>" + username + "</STRONG>";
    str += "</div>";
    str +=
        "<div class='h-50 overflow-auto' style='background-color: rgba(239, 234, 226, 1)'>";
    str += "<div class='col-sm-12'>";
    str += "<br />";
    for (var i = 0; i < conversa.length; i++) {
        if (conversa[i].id_receiver == idUser) {
            //MISSATGES ENVIATS
            str +=
                "<div class='col-sm-9 offset-sm-3 shadow-sm p-2 mb-4 rounded' style='background-color: rgba(217, 253, 211, 1)'>";
            str += "<p class='text-right mr-3 mb-2'>";
            str += conversa[i].missatge;
            str += "</p>";
            str += "<p class='text-right mb-1'>";
            str += "<small>";
            str += conversa[i].fecha;
            str += "</small>";
            str += "&nbsp;&nbsp;";
            if (conversa[i].status == "read") {
                str += "<img src='../static/read.png'></img>";
            } else if (conversa[i].status == "received") {
                str += "<img src='../static/received.png'/></img>";
            } else {
                str += "<img src='../static/send.png'/></img>";
            }

            str += "</p>";
            str += "</div>";
        } else {
            // MISSATGES REBUTS
            str += "<div class='col-sm-9 shadow-sm p-2 mb-4 bg-white rounded'>";
            str += "<p class='text-left mb-2'>";
            str += conversa[i].missatge;
            str += "</p>";
            str += "<p class='text-right mb-1'>";
            (str += "<small>"), (str += conversa[i].fecha);
            str += "</small>";
            str += "</p>";
            str += "</div>";
        }
    }
    str += "</div>";
    str += "</div>";
    str += "<br />";
    str += "<div class='form-row'>";
    str += "<div class='col-11'>";
    str += "<input type='text' placeholder='Escriu un missatge i envia-ho' ";
    str += "class='form-control' name='missatgeNou'id='missatgeNou'/>";
    str += "</div>";
    str += "<div class='col-1'>";
    str += "<input type='image' src='static/enviar.png' ";
    str += "onclick='enviaMissatge(" + idUser + ")'/>";
    str += "</div>";
    str += "</div>";
    str += "</div>";
    return str;
}

// FUNCIO CANVIA STATUS MISSATGES A READ
function canviaStatusToRead(conversa, idUser) {
    // FILTRAM ELS MISSATGES REBUTS DE LA CONVERSA ENVIATS PER idUser
    // I AMB STATUS = "send" o "received"
    var missatgesFiltrats = conversa.filter(
        (missatge) =>
            missatge.id_sender == idUser &&
            (missatge.status == "send" || missatge.status == "received")
    );

    // NOMES CANVIAM STATUS SI HI HA MISSATGES QUE COMPLEIXEN CONDICIÓ
    if (missatgesFiltrats.length > 0) {
        var settings = {
            url: "http://87.235.201.250:8080/whatspau_php/missatgesllegits",
            method: "PUT",
            timeout: 0,
            headers: {
                Authorization: token,
                "Content-Type": "application/json",
            },
            data: JSON.stringify(missatgesFiltrats),
        };

        $.ajax(settings).done(function (response) {
            //console.log(response);
        });
    }
}

// FUNCIO QUE ENVIA UN MISSATGE A UN AMIC
function enviaMissatge(idUser) {
    //CAPTURAM MISSATGE
    var nouMissatge = document.getElementById("missatgeNou").value;

    // ENVIAM POS A L'API

    var settings = {
        url: "http://87.235.201.250:8080/whatspau_php/missatges/" + idUser,
        method: "POST",
        timeout: 0,
        headers: {
            Authorization: token,
            "Content-Type": "application/json",
        },
        data: JSON.stringify({
            texte: nouMissatge,
        }),
    };

    $.ajax(settings).done(function (response) {
        //console.log(response);
        // TORNAM A CARREGAR LA CONVERSA AMB L'USUARI
        carregaConversaSegonsContacte(idUser);
    });
}

/* function cargaBasic() {
    //carregam les usuaris (ja els tenim, pero per veure com se fa)
    console.log("Entrant a JS, carregam usuaris");
    token = $.cookie("JWT");
    console.log(token);
    url = serverAPI + "/users";
    var aj1 = $.ajax({
        url: url,
        type: "GET",
        dataType: "json",
        headers: { Authorization: token },
    }).done(function (json) {
        console.log(json);
        usuaris = json;
    });
}

function MissatgesUsuari(id_user) {
    //carrega els missatges d'un usuari
}

//exemple de codi per imprimir missatges, 
//el podeu utilitzar així com esta o modificar
function PrintMissatges(missatges, usuari) {
    const user = usuaris.find((element) => element["id_user"] == usuari);
    htmlHeader =
        '<div class="alert alert-success" role="alert">Conversa amb ' +
        user["username"] +
        "</div>";
    htmlFooter =
        '<div class="form-row"><div class="col-11"><input type="text" class="form-control" id="missatgeNou" >';
    htmlFooter +=
        '</div><div class="col-1"><img src="static/enviar.png" onclick="EnviaMissatge()"></div></div>';
    htmlBody =
        '<div class="h-50 overflow-auto" style="background-color: rgba(0,0,255,.1)"><div class="col-sm-10">';
    for (i = 0; i < missatges.length; i++) {
        mis = missatges[i];
        if (mis["id_sender"] == user["id_user"]) {
            //és un missatge rebut
            htmlMis =
                '<div class="shadow-sm p-2 mb-4 bg-info rounded"><p class="text-left">' +
                mis["missatge"];
            htmlMis += "<sub>" + mis["fecha"] + "</sub></p></div>";
        } else {
            //és un missatge enviat
            htmlMis =
                '<div class="shadow-sm p-2 mb-4 bg-white rounded"><p class="text-right">' +
                mis["missatge"];
            htmlMis +=
                "<sub>" +
                mis["fecha"] +
                '<img src="static/' +
                mis["status"] +
                '.png"></sub></p></div>';
        }
        htmlBody += htmlMis;
    }
    htmlBody += "</div></div>";
    $("#missatgesSection").html(htmlHeader + htmlBody + htmlFooter);
}
 */
