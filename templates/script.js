function btn_click(item, opened, down, right) {
    var text = document.getElementById(item);
    var pic = document.getElementById(opened)
    if (text.style.display === "block") {
        text.style.display = "none";
        pic.src = right;
    } else {
        text.style.display = "block";
        pic.src = down;
    }
}
