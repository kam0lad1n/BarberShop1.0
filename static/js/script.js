const video = document.querySelector(".tutorial"),
animated = document.querySelectorAll(".animated")

const show_video = () =>{
    video.classList.add("active")
}
const hide_video = () => {
    video.classList.remove("active");
}

document.addEventListener("mousemove", (element) =>{
    animated.forEach((e) =>{
        let move_value = e.getAttribute("trf")
        let x = (element.clientX * move_value) / 50
        let y = (element.clientY * move_value) / 50

        e.style.transform = `translateX(${x * 1.25}px) translateY(${y * 1.25}px) rotate(${x * y / 100 - 25}deg)`
    })
})