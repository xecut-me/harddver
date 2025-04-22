# Хард Дверь = hardware дверь

Это страница двери в хакспейс Xecut, присылайте пулл реквесты ;)  

Дверь это бывший 16.5" ноут, разобранный и приклеенный 3M липкой лентой к двери  

Чтобы задеплоить пинганите https://t.me/enovikov11 или вступвйте в чат с админкой https://t.me/+IBkZEqKkqRlhNGQy  

<img src="./docs/detailed.jpg"></img><br/>
<img src="./docs/pano.jpg"></img><br/>
<img src="./docs/back.jpg"></img><br/>

# Разработчику

Телеграм ботик, он же http сервер, он же chromium с selenium для управления это main.py.  

Статический сайт расположен в ./static  

## Админские команды @harddver_bot

reload - Обновить страницу
produrl - Вернуть URL на продовый
url - Установить кастомный URL
deploy - Передеплоить бота
screenshot - Сделать скриншот

# Владельцу

## Как налить все с нуля

1. Установить https://alpinelinux.org  

2. Выполнить команды  

```bash
apk add --no-cache xorg-server xf86-video-intel xf86-input-evdev xinit chromium openbox chromium \
    chromium-chromedriver udev ttf-freefont dbus bash curl ca-certificates xdg-utils

pip install -r requirements.txt --break-system-packages
```

3. Настроить иксы, профиль и openrc файлы, см папку linux

## Дебаг хрома

<img src="./docs/debug.png"></img>

```bash
ssh -L 9222:localhost:9222 kiosk
```

chrome://inspect/#devices

## Управление openrc сервисом

```bash
rc-service kiosk stop
rc-service kiosk start
rc-update del kiosk
rc-update add kiosk default
```

## VNC

http://localhost:6080/vnc.html?autoconnect=1&resize=scale&password=123123

```bash
ssh -L 6080:localhost:6080 kiosk

x0vncserver -display :0 -localhost -PasswordFile ~/.vnc/passwd

~/noVNC/utils/novnc_proxy --vnc localhost:5900 --listen localhost:6080

apk add tigervnc
```

## Power usage

poweroff 0.3W  
idle 8.5-9W  
under full load 15-18W  

## Как тестить ботика без гитхаба

```bash
scp ~/Desktop/xecut/harddver/main.py kiosk@kiosk:/home/kiosk/harddver/main.py

DISPLAY=:0 /usr/bin/chromium --kiosk --no-first-run --disable-infobars --noerrdialogs --use-fake-ui-for-media-stream  http://192.168.1.58:8000/

DISPLAY=:0 /usr/bin/chromium --kiosk --no-first-run --disable-infobars --noerrdialogs --use-fake-ui-for-media-stream file:///root/kiosk-website/index.html
```
