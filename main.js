const digits = [...document.querySelectorAll(".digit")];
const positions = [8, 9, 5, 6, 0, 1, 2, 3, 11, 12, 14, 15, 17, 18, 20, 21, 22];
const offset = new Date().getTimezoneOffset() * 60000;
let lastTime = "";

function render() {
    const time = new Date(Date.now() - offset).toISOString();

    for (let i = 0; i < positions.length; i++) {
        const d = positions[i];

        if (lastTime[d] != time[d]) {
            digits[i].style.backgroundPosition = `-${+time[d] * 68}px 0`;
        }
    }

    lastTime = time;
    requestAnimationFrame(render);
}

async function startCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    const videoElement = document.getElementById('camera');
    videoElement.srcObject = stream;
}

async function update() {
    const v = await fetch(`./version.txt?_=${Date.now()}`, { cache: "no-store" }).then(res => res.text());
    document.querySelector("#version").innerText = v;

    if (v != localStorage.harddverVersion) {
        localStorage.harddverVersion = v;
        location.reload();
    }
}

async function get_backdoor_state() {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append('Authorization','Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI1YzY0NDg0Y2NjNmE0N2VjOTY5Yzk2MjBlNmY4OWI5NSIsImlhdCI6MTc0NTE3MjA5NSwiZXhwIjoyMDYwNTMyMDk1fQ.bTSqlafXk-i7f0EOp2ENDqll7wNUucVoFaLjZqd53xo')

    const backdoorState = await fetch('https://haos.xecut.me/api/states/switch.esp_door_1_backdoor_switch',{headers:myHeaders})
        .then(res => res.json())
        .then(({state}) => state)
        .catch(() => 'off')

    const backdoorIndicator = document.querySelector('#backdoorIndicator')

    const hiddenClass = 'hidden'
    backdoorIndicator.classList.add(hiddenClass)
    if (backdoorState === 'on') {
        backdoorIndicator.classList.remove(hiddenClass)
    }
}

render();
startCamera();
setInterval(update, 10000);

get_backdoor_state();
setInterval(get_backdoor_state, 10000);
update();
