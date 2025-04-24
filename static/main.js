const digits = [...document.querySelectorAll(".clock-digit")];
const positions = [8, 9, 5, 6, 0, 1, 2, 3, 11, 12, 14, 15, 17, 18, 20, 21, 22];
const offset = new Date().getTimezoneOffset() * 60000;
let lastTime = "", recorder;

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

    let recordedChunks = [];

    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = (e) => { if (e.data.size > 0) recordedChunks.push(e.data); };

    recorder.onstop = () => {
        const blob = new Blob(recordedChunks, { type: "video/webm" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");

        const now = new Date();
        const filename = now.toISOString().replace(/[:T]/g, "-").split(".")[0] + ".webm";

        a.style.display = "none";
        a.href = url;
        a.download = filename;

        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        URL.revokeObjectURL(url);
    };

    setInterval(() => { recorder.stop(); recorder.start(); }, 10000);
    recorder.start();
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

async function getTemperatureAndCO2() {
    const temp = await fetch("./temp")
        .then(res => res.text());

    document.querySelector(".widget-temperature").innerText = temp;

    const co2 = await fetch("./co2")
        .then(res => res.text());

    document.querySelector(".widget-co2").innerText = co2;
}

function addMessage(messageJson) {
    const message = JSON.parse(messageJson);

    const div = document.createElement("div");
    div.innerText = `@${message.username}: ${message.text}\n`;

    const widgetChat = document.querySelector(".widget-chat");
    widgetChat.appendChild(div);
    widgetChat.scrollTop = widgetChat.scrollHeight;
}

const dvdWidth = 1570, dvdHeight = 922, dvd = document.querySelector(".widget-dvd");
let dvdLastRenderTime = Date.now(), dx = 0.3, dy = 0.3;
let x = Math.floor(Math.random() * dvdWidth), y = Math.floor(Math.random() * dvdHeight);
let dvdHue = 0;

function setDvdRandomColor() {
    const hueHalfGuard = 30;

    dvdHue = (dvdHue + hueHalfGuard + Math.random() * (360 - 2 * hueHalfGuard)) % 360;

    document.querySelector("#dvd").setAttribute("fill", `hsl(${dvdHue}, 100%, 50%)`);
}

function animateDvd() {
    let renderTime = Date.now();

    x += dx * (renderTime - dvdLastRenderTime);
    y += dy * (renderTime - dvdLastRenderTime);

    if (x > dvdHeight) { x = 2 * dvdHeight - x; dx *= -1; setDvdRandomColor(); }
    if (x < 0) { x = - x; dx *= -1; setDvdRandomColor(); }

    if (y > dvdWidth) { y = 2 * dvdWidth - y; dy *= -1; setDvdRandomColor(); }
    if (y < 0) { y = - y; dy *= -1; setDvdRandomColor(); }

    dvdLastRenderTime = renderTime;

    dvd.style.top = x + "px";
    dvd.style.left = y + "px";
    requestAnimationFrame(animateDvd);
}

renderTimer();
animateDvd();

if (location.href.includes("debug")) {
    document.querySelector(".widget-backdoor").classList.remove("hidden");

    [...document.querySelectorAll(".widget")].forEach(e => e.style.border = "5px white solid");
} else {
    startCamera();

    setInterval(getBackdoorState, 10000);
    getBackdoorState();

    setInterval(getTemperatureAndCO2, 10000);
    getTemperatureAndCO2();
}