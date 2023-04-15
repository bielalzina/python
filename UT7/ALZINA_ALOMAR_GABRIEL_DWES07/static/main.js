// INICILATZACIÓ

var serverAPI = "http://87.235.201.250:8080/whatspau_php";
var idUsuariActual = 0;

var token;
var missatges;

// RECUPERAM TOKEN
token = $.cookie("JWT");
//console.log(token);

// FUNCIÓ PER CARREGAR MISSATGES CONVERSA AMB UN USUARI
function carregaConversaPerContacte(idUserGrup) {
    //console.log(idUserGrup);
    // SEPARAM STRING id_contacte
    const vector = idUserGrup.split("-");
    var tipusContacte = vector[0];
    var idContacte = vector[1];
    //console.log(tipusContacte);
    //console.log(idContacte);

    if (tipusContacte == "amic") {
        // conversa amb un amic
        // RECUPERAM NOM AMIC
        let username = document.getElementById(idUserGrup).innerText;
        //console.log(username);
        //console.log("Entrant a JS, carregam conversa");

        // DEFINIM URL
        url = serverAPI + "/missatges/" + idContacte;
        //console.log(url);
        var aj1 = $.ajax({
            url: url,
            type: "GET",
            dataType: "json",
            headers: { Authorization: token },
        }).done(function (json) {
            conversa = json;
            //console.log(conversa);

            //RECUPERAM MISSATGES DE LA CONVERSA
            var str = pintaConversa(username, idContacte, conversa);
            document.getElementById("missatgesSection").innerHTML = str;

            //CANVIAM STATUS DELS MISSATGES REBUTS EN LA CONVERSA A LLEGITS
            canviaStatusToRead(conversa, idContacte);

            //ACTUALITZAM NUM. MISSATGES NOUS
            // CAPTURAM ELEMENT A MODIFICAR
            var idElement = document.getElementById(
                "numNous-amic-" + idContacte
            );
            // MODIFICAM ELEMENT
            idElement.classList.remove("table-success");
            idElement.innerHTML = "--";
        });
    } else {
        // conversa amb un grup
        // RECUPERAM NOM GRUP
        let groupName = document.getElementById(idUserGrup).innerText;
        //console.log(groupName);

        // DEFINIM URL
        url = serverAPI + "/missatgesgrup/" + idContacte;

        var aj1 = $.ajax({
            url: url,
            type: "GET",
            dataType: "json",
            headers: { Authorization: token },
        }).done(function (json) {
            conversaGrup = json;
            //console.log(conversaGrup);

            //PINTAM LA CONVERSA DEL GRUPRECUPERAM MISSATGES DE LA CONVERSA
            pintaConversaGrup(groupName, idContacte, conversaGrup);
        });
    }
}

//FUNCIÓ QUE PINTA LA CONVERSA AMB L'USUARI SELECCIONAT
function pintaConversa(username, idContacte, conversa) {
    var str;

    str = "<div class='col-sm-8'>";
    str += "<div class='alert alert-success' role='alert'>";
    str += "Conversa amb <strong>" + username + "</strong>";
    str += "</div>";
    str +=
        "<div class='h-50 overflow-auto' style='background-color: rgba(239, 234, 226, 1)'>";
    str += "<div class='col-sm-12'>";
    str += "<br>";

    for (var i = 0; i < conversa.length; i++) {
        if (conversa[i].id_receiver == idContacte) {
            str +=
                "<div class='col-sm-9 offset-sm-3 shadow-sm p-2 mb-4 rounded' style='background-color: rgba(217, 253, 211, 1)'>";
            str += "<p class='text-right mr-3 mb-2'>";
            str += conversa[i].missatge;
            str += "</p>";
            str += "<p class='text-right mb-1'>";
            str += "<small>";
            str += formataData(conversa[i].fecha);
            str += "</small>";
            str += "&nbsp;&nbsp;";
            if (conversa[i].status == "read") {
                str += "<img src='../static/read.png'></img>";
            } else if (conversa[i].status == "received") {
                str += "<img src='../static/received.png'></img>";
            } else {
                str += "<img src='../static/send.png'></img>";
            }

            str += "</p>";
            str += "</div>";
        } else {
            str += "<div class='col-sm-9 shadow-sm p-2 mb-4 bg-white rounded'>";
            str += "<p class='text-left mb-2'>";
            str += conversa[i].missatge;
            str += "</p>";
            str += "<p class='text-right mb-1'>";
            str += "<small>";
            str += formataData(conversa[i].fecha);
            str += "</small>";
            str += "</p>";
            str += "</div>";
        }
    }

    str += "</div>";
    str += "</div>";
    str += "<br>";

    str += "<div class='form-row'>";
    str += "<div class='col-11'>";
    str +=
        "<input type='text' placeholder='Escriu un missatge i envia-ho' class='form-control' name='missatgeNou' id='missatgeNou' >";
    str += "</div>";
    str += "<div class='col-1'>";
    str +=
        "<input type='image' src='static/enviar.png' onclick='enviaMissatge(" +
        idContacte +
        ")'>";
    str += "</div>";
    str += "</div>";
    str += "</div>";

    return str;
}

//CANVIA FORMAT DATA aaaa-mm-dd hh:mm:ss -> dd/mm/aaaa - hh:mm:ss
function formataData(data) {
    // Separam data i hora
    let parts = data.split(" ");
    let dataParts = parts[0].split("-");

    // Cream el nou format de data
    let novaData = dataParts[2] + "/" + dataParts[1] + "/" + dataParts[0];

    // Unim la data i l'hora en el format
    let novaDataHora = novaData + " - " + parts[1];

    return novaDataHora;
}

// CANVIA STATUS MISSATGES A READ
function canviaStatusToRead(conversa, idContacte) {
    //FILTRAM ELS MISSATGES REBUTS EN LA CONVERSA ENVIATS PER idContacte
    // I AMB STATUS = "send" o "received"
    //console.log(conversa);
    var missatgesFiltrats = conversa.filter(
        (missatge) =>
            missatge.id_sender == idContacte &&
            (missatge.status == "send" || missatge.status == "received")
    );

    //NOMÉS EXECUTAM EL PUT SI EXISTEIXEN MISSATGES QUE COMPLEIXEN CONDICIONS

    if (missatgesFiltrats.length > 0) {
        // FEIM PUT A L'API

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

function enviaMissatge(idContacte) {
    //console.log(idContacte);

    // Capturam missatge
    var nouMissatge = document.getElementById("missatgeNou").value;
    //console.log(nouMissatge);

    // ENVIAM POST A L'API

    var settings = {
        url: "http://87.235.201.250:8080/whatspau_php/missatges/" + idContacte,
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
        // TORNAM CARREGAR LA CONVERSA AMB L'USUARI
        idContacte = "amic-" + idContacte;
        carregaConversaPerContacte(idContacte);
    });
}

function pintaConversaGrup(groupName, idContacte, conversaGrup) {
    // RECUPERAM IDs I USERNAMES DLES USUARIS PER INDICAR QUI HA ENVIAT EL
    // MISSATGE EN ELS MISSATGES REBUTS EN CONVERSA GRUP

    var settings = {
        url: "http://87.235.201.250:8080/whatspau_php/users",
        method: "GET",
        timeout: 0,
        headers: {
            Authorization: token,
        },
    };

    $.ajax(settings).done(function (response) {
        usuarisLlista = response;
        //console.log(usuarisLlista);

        var str;

        str = "<div class='col-sm-8'>";
        str += "<div class='alert alert-success' role='alert'>";
        str += "Conversa amb el grup: &nbsp;<strong>" + groupName + "</strong>";
        str += "</div>";
        str +=
            "<div class='h-50 overflow-auto' style='background-color: rgba(239, 234, 226, 1)'>";
        str += "<div class='col-sm-12'>";
        str += "<br>";

        for (var i = 0; i < conversaGrup.length; i++) {
            // Identificam qui ha enviat el missatge

            nomSender = retornaUsernameById(
                conversaGrup[i].id_sender,
                usuarisLlista
            );

            if (nomSender == null) {
                // en aquest cas l'emissor és l'usuari autenticat (JO)
                // MISSATGES ENVIATS
                str +=
                    "<div class='col-sm-9 offset-sm-3 shadow-sm p-2 mb-4 rounded' style='background-color: rgba(217, 253, 211, 1)'>";
                str += "<p class='text-right mr-3 mb-2'>";
                str += conversaGrup[i].missatge;
                str += "</p>";
                str += "<p class='text-right mb-1'>";
                str += "<small>";
                str += formataData(conversaGrup[i].fecha);
                str += "</small>";

                str += "</p>";
                str += "</div>";
            } else {
                // MISSATGES REBUTS
                str +=
                    "<div class='col-sm-9 shadow-sm p-2 mb-4 bg-white rounded'>";
                str += "<p class='text-left mb-2 text-primary'>";

                str += nomSender;
                str += "</p>";
                str += "<p class='text-left mb-2'>";
                str += conversaGrup[i].missatge;
                str += "</p>";
                str += "<p class='text-right mb-1'>";
                str += "<small>";
                str += formataData(conversaGrup[i].fecha);
                str += "</small>";
                str += "</p>";
                str += "</div>";
            }
        }

        str += "</div>";
        str += "</div>";
        str += "<br>";

        str += "<div class='form-row'>";
        str += "<div class='col-11'>";
        str +=
            "<input type='text' placeholder='Escriu un missatge i envia-ho al grup' class='form-control' name='missatgeNouGrup' id='missatgeNouGrup' >";
        str += "</div>";
        str += "<div class='col-1'>";
        str +=
            "<input type='image' src='static/enviar.png' onclick='enviaMissatgeGrup(" +
            idContacte +
            ")'>";
        str += "</div>";
        str += "</div>";
        str += "</div>";

        document.getElementById("missatgesSection").innerHTML = str;
    });
}

function retornaUsernameById(id, usuarisLlista) {
    var nomAmic = null;
    for (let i = 0; i < usuarisLlista.length; i++) {
        if (id == usuarisLlista[i].id_user) {
            nomAmic = usuarisLlista[i].username;
        }
    }
    return nomAmic;
}

function enviaMissatgeGrup(idContacte) {
    //console.log(idContacte);

    // Capturam missatge
    var nouMissatgeGrup = document.getElementById("missatgeNouGrup").value;
    //console.log(nouMissatge);

    // ENVIAM POST A L'API

    var settings = {
        url:
            "http://87.235.201.250:8080/whatspau_php/missatgesgrup/" +
            idContacte,
        method: "POST",
        timeout: 0,
        headers: {
            Authorization: token,
            "Content-Type": "application/json",
        },
        data: JSON.stringify({
            texte: nouMissatgeGrup,
        }),
    };

    $.ajax(settings).done(function (response) {
        //console.log(response);
        // TORNAM CARREGAR LA CONVERSA AMB L'USUARI
        idContacte = "grup-" + idContacte;
        carregaConversaPerContacte(idContacte);
    });
}

function carregaFormCreaGrup() {
    // RECUPERAM IDs I USERNAMES DELS USUARIS PER PASSAR-LOS A FORM
    // CREACIÓ GRUP

    var settings = {
        url: "http://87.235.201.250:8080/whatspau_php/users",
        method: "GET",
        timeout: 0,
        headers: {
            Authorization: token,
        },
    };

    $.ajax(settings).done(function (response) {
        usuarisLlista = response;
        //console.log(usuarisLlista);

        var str;

        str = "<div class='container'>";
        str += "<div class='col-sm-8'>";
        str += "<div class='alert alert-success' role='alert'>";
        str += "<p>CREACIÓ GRUP WHATSPAU</p>";
        str += "<p>Has d'indicar el nom del grup</p>";
        str += "<p>";
        str += "Selecciona els membres del grup (un com a mínim)";
        str += "<br />";
        str += "Fes servir ctrl+click per seleccionar-ne més d'un membre";
        str += "<br />";
        str += "El teu contacte s'inclou per defecte";
        str += "</p>";
        str += "</div>";

        str += "<div class='form-group'>";
        str += "<label for='nomGrup'>NOM GRUP:</label>";
        str +=
            "<input type='text' class='form-control' id='nomGrup' name='nomGrup' required placeholder='Escriu aquí el nom del grup'/>";
        str += "</div>";
        str += "<div class='form-group'>";
        str += "<label for='membresGrup'>";
        str +=
            "Selecciona els membres del grup. Fes servir ctrl+click per seleccionar-ne més d'un:";
        str += "</label>";
        str +=
            "<select multiple id='membresGrup' name='membresGrup' required class='form-control' size='36'>";

        for (let i = 0; i < usuarisLlista.length; i++) {
            str +=
                "<option value=" +
                usuarisLlista[i].id_user +
                ">" +
                usuarisLlista[i].username +
                "</option>";
        }

        str += "</select>";
        str += "</div>";
        str +=
            "<button class='btn btn-primary' onclick='creaGrup()'>CREA</button>";

        str += "</div>";
        str += "</div>";

        document.getElementById("missatgesSection").innerHTML = str;
    });
}

function creaGrup() {
    // CAPTURAM VALORS DEL FORM
    var nomGrup = document.getElementById("nomGrup").value;
    //console.log(nomGrup);
    var comprovacioNomGrup = nomGrup.match(/^[^\s][a-zA-Z0-9\s]{2,}$/g);
    //console.log(comprovacioNomGrup);
    if (comprovacioNomGrup != null) {
        // CAPTURAM VALORS DEL SELECT
        var seleccionats = [];
        for (var option of document.getElementById("membresGrup").options) {
            if (option.selected) {
                seleccionats.push(option.value);
            }
        }
        if (seleccionats.length > 0) {
            //Convertim valors array seleccionats a int

            //console.log(seleccionats);
            var membresSeleccionats = [];
            seleccionats.forEach((id) =>
                membresSeleccionats.push(parseInt(id))
            );
            //console.log(membresSeleccionats);

            var settings = {
                url: "http://87.235.201.250:8080/whatspau_php/grups",
                method: "POST",
                timeout: 0,
                headers: {
                    Authorization: token,
                    "Content-Type": "application/json",
                },
                data: JSON.stringify({
                    users: membresSeleccionats,
                    grupname: nomGrup,
                }),
            };

            $.ajax(settings).done(function (response) {
                //console.log(response);

                $.jGrowl(
                    "S'HA CREAT EL GRUP " +
                        nomGrup +
                        ", AMB ELS MEMBRES INDICATS",
                    {
                        sticky: true,
                    }
                );
                $.jGrowl("ACTUALITZANT PAGINA!!", {
                    sticky: true,
                });
                location.reload();
            });
        } else {
            $.jGrowl("HAS DE SELECCIONAR UN MEMBRE COM A MÍNIM!!!", {
                sticky: true,
            });
        }
    } else {
        $.jGrowl("EL NOM DEL GRUP QUE HAS INTRODUÏT NO ÉS VÀLID!", {
            sticky: true,
        });
    }
}

//OBTENIM DATA i HORA QUAN ES CARREGA main.js
//A PARTIR D'AQUEST VALOR ES FARÀ LA PRIMERA COMPROVACIÓ
//PER CAPTURAR ELS MISSATGES NOUS, REBUTS DESPRÉS D'AQUEST VALOR

var dateTimeAnterior = new Date();

window.addEventListener("load", function () {
    setTimeout(function () {
        comprovaMissatgesNous(dateTimeAnterior);
    }, 60000);
});

function comprovaMissatgesNous(dateTimeAnterior) {
    var settings = {
        url: "http://87.235.201.250:8080/whatspau_php/missatges",
        method: "GET",
        timeout: 0,
        headers: {
            Authorization: token,
        },
    };

    $.ajax(settings).done(function (response) {
        const dateTimeActual = new Date();

        if (response.length > 0) {
            var missatgesNous = [];
            for (let i = 0; i < response.length; i++) {
                var dateTimeMissatge = strToDateObject(response[i].fecha);
                if (dateTimeMissatge > dateTimeAnterior) {
                    missatgesNous.push(response[i]);
                }
            }

            if (missatgesNous.length > 0) {
                // RECUPERAM USERS
                var settings = {
                    url: "http://87.235.201.250:8080/whatspau_php/users",
                    method: "GET",
                    timeout: 0,
                    headers: {
                        Authorization: token,
                    },
                };

                $.ajax(settings).done(function (users) {
                    str = "<p>MISSATGES NOUS</p>";
                    for (var i = 0; i < missatgesNous.length; i++) {
                        // Identificam qui ha enviat el missatge
                        nomSender = retornaUsernameById(
                            missatgesNous[i].id_sender,
                            users
                        );
                        const [dateStr, timeStr] =
                            missatgesNous[i].fecha.split(" ");
                        str += "<p> Tens un missatge nou de ";
                        str += "<strong>";
                        str += nomSender;
                        str += "</strong>. Enviat a les " + timeStr;
                        str += "</p>";
                        //ACTUALITZAM CONTADOR
                        var idTag =
                            "numNous-amic-" + missatgesNous[i].id_sender;
                        var tag = document.getElementById(idTag);
                        var valorTag = tag.innerHTML;
                        valorTag = parseInt(valorTag);
                        valorTag = valorTag + 1;
                        tag.innerHTML = valorTag;
                    }
                    $.jGrowl(str, {
                        header: "TENS MISSATGES NOUS!!!",
                        life: 4000,
                    });
                });
            }
        }

        setTimeout(function () {
            comprovaMissatgesNous(dateTimeActual);
        }, 60000);
    });
}

/*
function formataDataHora(ara) {
    const dia = String(ara.getDate()).padStart(2, "0");
    const mes = String(ara.getMonth() + 1).padStart(2, "0");
    const any = ara.getFullYear();
    const hora = String(ara.getHours()).padStart(2, "0");
    const minuts = String(ara.getMinutes()).padStart(2, "0");
    const segons = String(ara.getSeconds()).padStart(2, "0");

    const dataFormatada =
        dia +
        "/" +
        mes +
        "/" +
        any +
        " - " +
        hora +
        ":" +
        minuts +
        ":" +
        segons;
    return dataFormatada;
}
*/

function strToDateObject(dateString) {
    const [dateStr, timeStr] = dateString.split(" ");

    const [year, month, day] = dateStr.split("-");
    const [hours, minutes, seconds] = timeStr.split(":");

    const date = new Date(+year, +month - 1, +day, +hours, +minutes, +seconds);
    return date;
}

/*
function mostraAvisMissatgesNous(str) {
    var w = window.open("", "", "width=100,height=100");
    w.document.write(str);
    w.focus();
    setTimeout(function () {
        w.close();
    }, 2000);
}
*/
