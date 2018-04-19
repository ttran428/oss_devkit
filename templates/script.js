function btn_click(item) {
    var x = document.getElementById(item);
    console.log(item);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
