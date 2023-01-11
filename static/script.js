function update_status() {
  fetch("/status").then((res) => res.json()).then((json) => {
    let wanted_list = json["wanted_list"];
    let current_list = json["current_list"];
    let liste = document.getElementById("liste");
    liste.innerHTML = ""

    wanted_list.forEach(it => {
      if(current_list.includes(it)) {
        liste.innerHTML += "<div class=\"columns is-full is-centered\"><div class=\"column button is-half is-success\">"
            + it + "</div></div>"
      } else {
        liste.innerHTML += "<div class=\"columns is-full is-centered\"><div class=\"column button is-half is-danger\">"
            + it + "</div></div>"
      }
    });
  })
}

function reset() {
  fetch("/reset").then((res) => res.json()).then((json) => {
    // Muss auch noch gemacht werden oder auch nicht, bin mir nicht mehr sicher
  })
}

setInterval(update_status, 100);