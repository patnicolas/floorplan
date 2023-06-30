// __author__ = "Patrick Nicolas"
// __copyright__ = "Copyright 2023. All rights reserved."

let chosenImage = document.getElementById("chosen-image");
let fileName = document.getElementById("file-name");
let error = document.getElementById("error");
let imageDisplay = document.getElementById("image-display");


const displayDate = (dateType) => {
    let loginDateP = document.getElementById(dateType);
    const today = (dateType == "loginDate") ? new Date() : new Date(Date.now() + 1000*60*60*24*2);
    const month = today.getMonth() +1;
    const day = today.getDate();
    const year = today.getFullYear();
    const time = today.toLocaleTimeString('en-US');

    const comment = (dateType == "loginDate") ? "Login date/time:" : "Completion date:";
    loginDateP.innerHTML = comment + '&nbsp;&nbsp;&nbsp;' + month + '/' + day + '/' + year + ' ' + time + ' PST'
};


function resetLandingPage2() {
    url = "http://localhost:8000/"
    fetch(url, {
        method: "GET"
    })
    location.reload();
}

const displayReset = (state) => {
    const reset_div = document.getElementById("resetId");
    if (reset_div) {
        reset_div.style.display = state;
    }
}

window.onload = () => {
    error.innerText = "";
    displayReset("block")
    displayDate("loginDate")
    displayDate("completionDate")
};
