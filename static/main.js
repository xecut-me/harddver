const digits = [...document.querySelectorAll(".digit")];
const positions = [8, 9, 5, 6, 0, 1, 2, 3, 11, 12, 14, 15, 17, 18, 20, 21, 22];
const offset = new Date().getTimezoneOffset() * 60000;
let lastTime = "";

function renderTimer() {
    const time = new Date(Date.now() - offset).toISOString();

    for (let i = 0; i < positions.length; i++) {
        const d = positions[i];

        if (lastTime[d] != time[d]) {
            digits[i].style.backgroundPosition = `-${+time[d] * 68}px 0`;
        }
    }

    lastTime = time;
    requestAnimationFrame(renderTimer);
}

async function startCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    const videoElement = document.getElementById("camera");
    videoElement.srcObject = stream;
}

async function getBackdoorState() {
    const backdoorState = await fetch("./backdoor")
        .then(res => res.json())
        .then(({ state }) => state)
        .catch(() => "off")

    const backdoorIndicator = document.querySelector("#backdoorIndicator");

    const hiddenClass = "hidden";
    backdoorIndicator.classList.add(hiddenClass)
    if (backdoorState === "on") {
        backdoorIndicator.classList.remove(hiddenClass)
    }
}

function onMessage(message) {
    return "Привет! " + message.slice(0, 10);
}

renderTimer();
startCamera();

setInterval(getBackdoorState, 10000);
getBackdoorState();
