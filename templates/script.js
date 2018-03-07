function btn_click(item) {
    var x = document.getElementById(item);
    console.log(item);
    if (x.style.display === "block") {
        x.style.display = "none";
    } else {
        x.style.display = "block";
    }
}
