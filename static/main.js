const digits = [...document.querySelectorAll(".digit")];
const positions = [8, 9, 5, 6, 0, 1, 2, 3, 11, 12, 14, 15, 17, 18, 20, 21, 22];
const offset = new Date().getTimezoneOffset() * 60000;
let lastTime = "";
let BACKDOOR_AUTH, BACKDOOR_URL;

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
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("Authorization", BACKDOOR_AUTH);

    const backdoorState = await fetch(BACKDOOR_URL, { headers: myHeaders })
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

async function initBackdoor() {
    const secrets = await fetch("./secrets").then(res => res.json());
    BACKDOOR_AUTH = secrets.BACKDOOR_AUTH;
    BACKDOOR_URL = secrets.BACKDOOR_URL;

    setInterval(getBackdoorState, 10000);
    getBackdoorState();
}

function onMessage(message) {
    return "Привет! " + message.slice(0, 10);
}

renderTimer();
startCamera();
initBackdoor();
