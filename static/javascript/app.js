//////////////////////////
// MODAL
//////////////////////////

// Get the modal
let modal = document.getElementById("infoModal");

// Get the button that opens the modal
let btn = document.getElementById("infoModalBtn");

// Get the <span> element that closes the modal
let span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

//////////////////////////
// CELLS
//////////////////////////

function editTable() {
    var table = document.getElementById('parameters');
    for (var r = 0, n = table.rows.length; r < n; r++) {
        for (var c = 0, m = table.rows[r].cells.length; c < m; c++) {
          if (table.rows[r].cells[c].firstChild) {
            if ((table.rows[r].cells[c].firstChild.value == 0.0) && !(table.rows[r].cells[c].classList.contains("meta-field"))) {
              //table.rows[r].cells[c].firstChild.style.backgroundColor = "rgb(192,192,192, 0.1)";
              table.rows[r].cells[c].firstChild.style.border = "none";
            }
          }
        }
    }
}

editTable()