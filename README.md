# xecut_harddver

Это страница двери в хакспейс xecut, присылайте пулл реквесты ;)

Чат с админкой https://t.me/+IBkZEqKkqRlhNGQy

<img src="./docs/detailed.jpg"></img><br/>

<img src="./docs/pano.jpg"></img><br/>

<img src="./docs/back.jpg"></img><br/>

hardware (дверь) = harddver

# contibute

запускаем

```bash
python3 -m http.server
```

заходим на http://localhost:8000/

# технические детали

на базе alpine, установлены пакеты  

```bash
apk add xorg-server xf86-video-intel xf86-input-evdev xinit chromium fluxbox
```

в openrc init.d есть startx и kiosk

# power usage

poweroff 0.3W  
idle 8.5-9W  
load 15-18W  

# докер

docker build -t kiosk .

docker run -d --env-file .env --name kiosk -e DISPLAY=:0 -v /tmp/.X11-unix:/tmp/.X11-unix -v /home/kiosk/harddver:/app:ro --restart=unless-stopped kiosk

# бот

reload - Обновить страницу
produrl - Вернуть URL на продовый
url - Установить кастомный URL
deploy - Передеплоить бота

# разное

ssh -L 6080:localhost:6080 kiosk
http://localhost:6080/vnc.html?autoconnect=1&resize=scale
/usr/bin/x11vnc -display :0 -localhost -nopw -forever
~/noVNC/utils/novnc_proxy --vnc localhost:5900 --listen localhost:6080

rc-service kiosk stop
rc-service kiosk start
rc-update del kiosk
rc-update add kiosk default

rsync -rz --info=progress2 --delete ~/Desktop/xecut_harddver/ kiosk:/root/kiosk-website/

DISPLAY=:0 /usr/bin/chromium --no-first-run --disable-infobars --noerrdialogs --use-fake-ui-for-media-stream --kiosk http://192.168.1.58:8000/

DISPLAY=:0 /usr/bin/chromium --no-first-run --disable-infobars --noerrdialogs --use-fake-ui-for-media-stream file:///root/kiosk-website/index.html
