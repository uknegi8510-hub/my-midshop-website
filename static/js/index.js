const container = document.getElementById("productScroll");
const fill = document.getElementById("scroll-fill");

function updateProgress() {
    const maxScroll = container.scrollWidth - container.clientWidth;

    if (maxScroll <= 0) {
        fill.style.width = "100%";
        return;
    }

    const percent = (container.scrollLeft / maxScroll) * 100;
    fill.style.width = percent + "%";
}

container.addEventListener("scroll", updateProgress);
window.addEventListener("load", updateProgress);
