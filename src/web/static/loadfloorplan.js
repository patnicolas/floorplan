// __author__ = "Patrick Nicolas"
// __copyright__ = "Copyright 2023. All rights reserved."

let uploadButton = document.getElementById("upload-button");
let chosenImage = document.getElementById("chosen-image");
let fileName = document.getElementById("file-name");
let container = document.querySelector(".container");
let error = document.getElementById("error");
let imageDisplay = document.getElementById("image-display");
let input = document.querySelector('input[type="file"]')
let username = document.getElementById("username_id")
let email = document.getElementById("email_id")


const fileHandler = (file, name, type) => {
  if (type.split("/")[1] !== "pdf") {
    //File Type Error
    error.innerText = "Format of floor plan " + type + " is incorrect. It should be PDF";
    return false;
  }
  error.innerText = "";
  let reader = new FileReader();
  reader.readAsDataURL(file);

  reader.onloadend = () => {
    //image and file name
    user_name = username.value
    let imageContainer = document.createElement("figure");
    let embed = document.createElement("embed");
    embed.src = reader.result;
    imageContainer.appendChild(embed);
    imageContainer.innerHTML += `<figcaption>From: ${user_name}  File: ${name}</figcaption>`;
    imageDisplay.appendChild(imageContainer);
    displaySubmit("block")
  };
};


const displayDate = (dateType) => {
    let loginDateP = document.getElementById(dateType);
    if (loginDateP) {
        const today = (dateType == "loginDate") ? new Date() : new Date(Date.now() + 1000*60*60*24*2);
        const month = today.getMonth() +1;
        const day = today.getDate();
        const year = today.getFullYear();
        const time = today.toLocaleTimeString('en-US');

        const comment = (dateType == "loginDate") ? "Login date/time:" : "Completion date:";
        loginDateP.innerHTML = comment + '&nbsp;&nbsp;&nbsp;' + month + '/' + day + '/' + year + ' ' + time + ' PST'
    }
};


const displaySubmit = (state) => {
    const submit_div = document.getElementById("buttonId");
    const cancel_div = document.getElementById("cancelId");
    if (submit_div) {
        submit_div.style.display = state;
        cancel_div.style.display = state;
    }
}


function resetLandingPage() {
    window.location.href=""
}


//Upload Button
uploadButton.addEventListener("change", () => {
  imageDisplay.innerHTML = "";
  Array.from(uploadButton.files).forEach((file) => {
    fileHandler(file, file.name, file.type);
  });
});

container.addEventListener(
  "dragenter",
  (e) => {
    e.preventDefault();
    e.stopPropagation();
    container.classList.add("active");
  },
  false
);

container.addEventListener(
  "dragleave",
  (e) => {
    e.preventDefault();
    e.stopPropagation();
    container.classList.remove("active");
  },
  false
);

container.addEventListener(
  "dragover",
  (e) => {
    e.preventDefault();
    e.stopPropagation();
    container.classList.add("active");
  },
  false
);

container.addEventListener(
  "drop",
  (e) => {
    e.preventDefault();
    e.stopPropagation();
    container.classList.remove("active");
    let draggedData = e.dataTransfer;
    let files = draggedData.files;
    imageDisplay.innerHTML = "";
    Array.from(files).forEach((file) => {
      fileHandler(file, file.name, file.type);
    });
    displaySubmit("block")
  },
  false
);


window.onload = () => {
    error.innerText = "";
    displaySubmit("none")
    displayDate("loginDate")
    displayDate("completionDate")
};
