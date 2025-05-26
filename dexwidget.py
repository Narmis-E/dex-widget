#!/usr/bin/env python3

from ctypes import CDLL
CDLL("libgtk4-layer-shell.so")

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
from gi.repository import Gtk4LayerShell as LayerShell
from gi.repository import Gtk, Gdk, GLib
import threading

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk4agg import FigureCanvasGTK4Agg as FigureCanvas
from matplotlib.patches import Rectangle
from pydexcom import Dexcom

def fetch_readings():
    try:
        dexcom = Dexcom(username="USERNAME HERE", password="PASSWORD HERE", region="ous") #region="us" if inside US
        readings = dexcom.get_glucose_readings(minutes=60, max_count=12)
        return list(reversed([r.mmol_l for r in readings]))
    except Exception as e:
        print(f"Error fetching Dexcom readings: {e}")
        return None

def create_styled_figure(bg_values):
    fig = Figure(figsize=(3.2, 2.2), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    width = len(bg_values)

    ax.add_patch(Rectangle((-0.5, 0), width, 4.2, fc='lightcoral', alpha=0.4, zorder=0, clip_on=True))
    ax.add_patch(Rectangle((-0.5, 4.4), width, 5.35, fc='lightgrey', alpha=0.3, zorder=0, clip_on=True))
    ax.add_patch(Rectangle((-0.5, 10), width, 6, fc='lightgoldenrodyellow', alpha=0.4, zorder=0, clip_on=True))

    ax.set_yticks([2, 6, 10, 14, 16])
    ax.set_ylim(0, 16)
    ax.set_xlim(-0.5, width - 0.5)
    ax.autoscale(enable=False, axis='y')

    if bg_values:
        ax.plot(bg_values, marker='o', color='#c5c9c5', linewidth=0, zorder=2, markersize=4)
    ax.set_xticks([])

    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.set_ylabel("")

    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.set_facecolor("#1f1f1f")
    ax.set_facecolor("#1f1f1f")
    ax.tick_params(colors="#c5c9c5", labelsize=8, pad=2, length=0)

    fig.tight_layout()
    return fig

def on_activate(app):
    window = Gtk.Window(application=app)
    window.set_default_size(360, 240)

    css = """
    window { background-color: transparent; }
    .rounded-window {
        background-color: #1f1f1f;
        border-radius: 9px;
        margin: 10px;
    }
    """
    
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(css.encode())
    display = Gdk.Display.get_default()
    Gtk.StyleContext.add_provider_for_display(
        display,
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    window.add_css_class("rounded-window")

    LayerShell.init_for_window(window)
    LayerShell.set_layer(window, LayerShell.Layer.TOP)
    LayerShell.set_anchor(window, LayerShell.Edge.TOP, True)
    LayerShell.set_margin(window, LayerShell.Edge.TOP, 9) # padding from top of output (e.g my compositors gaps are 9px)

    outer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    outer_box.set_margin_top(10)
    outer_box.set_margin_bottom(10)
    outer_box.set_margin_start(10)
    outer_box.set_margin_end(10)

    spinner = Gtk.Spinner()
    spinner.set_size_request(48, 48)
    spinner.start()
    spinner.set_halign(Gtk.Align.CENTER)
    spinner.set_valign(Gtk.Align.CENTER)

    loading_label = Gtk.Label(label="Loading BG data...")
    loading_label.set_halign(Gtk.Align.CENTER)
    loading_label.set_valign(Gtk.Align.CENTER)

    outer_box.append(spinner)
    outer_box.append(loading_label)
    window.set_child(outer_box)
    window.present()

    threading.Thread(target=_fetch_and_update_graph, args=(outer_box, spinner, loading_label), daemon=True).start()

    gesture = Gtk.GestureClick()
    gesture.connect("pressed", lambda *_: window.close())
    window.add_controller(gesture)

def _fetch_and_update_graph(outer_box, spinner, loading_label):
    bg_values = fetch_readings()
    GLib.idle_add(_update_gui_with_graph, outer_box, spinner, loading_label, bg_values)
    return False

def _update_gui_with_graph(outer_box, spinner, loading_label, bg_values):
    outer_box.remove(spinner)
    outer_box.remove(loading_label)
    spinner.stop()

    if bg_values is not None:
        fig = create_styled_figure(bg_values)
        canvas = FigureCanvas(fig)
        outer_box.append(canvas)
    else:
        error_label = Gtk.Label(label="Failed to load data.\nPlease check your connection or credentials.")
        error_label.set_halign(Gtk.Align.CENTER)
        error_label.set_valign(Gtk.Align.CENTER)
        error_label.set_hexpand(True)
        error_label.set_vexpand(True)
        outer_box.append(error_label)

    return False

app = Gtk.Application(application_id="com.narmis-e.DexWidget")
app.connect("activate", on_activate)
app.run(None)
