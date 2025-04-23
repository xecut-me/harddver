const digits = [...document.querySelectorAll(".clock-digit")];
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
    const videoElement = document.querySelector(".camera");
    videoElement.srcObject = stream;
}

async function getBackdoorState() {
    const backdoorState = await fetch("./backdoor")
        .then(res => res.json())
        .then(({ state }) => state)
        .catch(() => "off")

    const backdoorIndicator = document.querySelector(".widget-backdoor");

    const hiddenClass = "hidden";
    backdoorIndicator.classList.add(hiddenClass)
    if (backdoorState === "on") {
        backdoorIndicator.classList.remove(hiddenClass)
    }

    [...document.querySelectorAll(".widget-clock")]
        .forEach(e => e.style.filter = backdoorState === "on" ? "invert(100%)" : "");
}

function addMessage(messageJson) {
    const message = JSON.parse(messageJson);

    const div = document.createElement("div");
    div.innerText = `@${message.username}: ${message.text}\n`;
    document.querySelector(".widget-chat").appendChild(div);
}

renderTimer();
startCamera();

setInterval(getBackdoorState, 10000);
getBackdoorState();

const text = "test";
const blob = new Blob([text], { type: "text/plain" });
const url = URL.createObjectURL(blob);
const a = document.createElement("a");
a.style.display = "none";
a.href = url;
a.download = "example.txt";
document.body.appendChild(a);
a.click();
URL.revokeObjectURL(url);
