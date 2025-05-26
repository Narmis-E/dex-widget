# dex-widget
A [gtk4-layer-shell](https://github.com/wmww/gtk4-layer-shell) widget to display Dexcom CGM data
![dexwidget_demo](https://github.com/user-attachments/assets/b74b66f3-b003-4653-89ff-7fc815fcc8da) \
Currently takes the past hour of readings and plots them using matplotlib.

## Dependencies
#### Compositor
> A Wayland compositor that support the Layer Shell protocol. Layer shell is supported on:
> - wlroots based compositors (such as Sway)
> - Smithay based compositors (such as COSMIC)
> - Mir based compositors (some may not enable the protocol by default. It can be enabled with --add-wayland-extension zwlr_layer_shell_v1)
> - KDE Plasma on wayland
>
> Layer shell is not supported on:
> - Gnome-on-Wayland
> - Any X11 desktop

^ Taken from gtk4-layer-shell README

#### Packages
**Pip packages:** \
`PyGObject matplotlib pydexcom`

**OS packages:** \
Arch: `gtk4 gtk4-layer-shell gobject-introspection` \
Install the associated packages for your distro.

## Run
```
chmod +x dexwidget.py
./dexwidget.py
```
Or execute in preferred bar:
e.g waybar: `"on-click": "~/.local/bin/dexwidget.py"`

## Notes
Based on my [waybar-dexcom](https://github.com/Narmis-E/waybar-dexcom) module, with looks from [dexviewer](https://github.com/Narmis-E/dexviewer), but turned into a gtk4 widget (thanks to ai). \
Dexcom SHARE username, password and window position are hardcoded into dexwidget.py. Open in a text editor to change.

## Todo
- [ ] Figure out how to close on unfocus/click outside window
- [ ] Add keybindings for changing bg range (e.g 3h, 6h, 12h, 24h)
- [ ] Decrease startup time (optimise matplotlib or replace altogether) (ergo remove need for GLib wheel spinner)
- [ ] Add Dark/Light mode functionality?
- [ ] Logging to json file for extended history
- [ ] Settings (username, password, window position, mg/dL/mmol units etc.)

<br>

- Contributions are very much welcome.
- At the moment my gtk knowledge is equivalent to a steaming pile of shit 👍
