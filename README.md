# xecut_harddver

Это страница двери в хакспейс xecut, присылайте пулл реквесты ;)

Чат с админкой https://t.me/+IBkZEqKkqRlhNGQy

<img src="./docs/detailed.jpg"></img><br/>

<img src="./docs/pano.jpg"></img><br/>

<img src="./docs/back.jpg"></img><br/>

hardware (дверь) = harddver

# Первоначальная установка

на базе alpine, установлены пакеты  

```bash
apk add --no-cache xorg-server xf86-video-intel xf86-input-evdev xinit chromium openbox chromium \
    chromium-chromedriver udev ttf-freefont dbus bash curl ca-certificates xdg-utils

pip install selenium==4.31.0 python-telegram-bot==20.5 --break-system-packages
```

# Power usage

poweroff 0.3W  
idle 8.5-9W  
load 15-18W  

# Команды бота

reload - Обновить страницу
produrl - Вернуть URL на продовый
url - Установить кастомный URL
deploy - Передеплоить бота

# Разное, VNC

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

scp ~/Desktop/xecut/harddver/main.py kiosk@kiosk:/home/kiosk/harddver/main.py
