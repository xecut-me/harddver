# xecut_harddver

Это страница двери в хакспейс xecut, присылайте пулл реквесты ;)

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
