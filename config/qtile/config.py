from typing import List  # noqa: F401
import os
import subprocess

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from keys import keys


mod = "mod4"
terminal = 'alacritty'


group_names = [("WEB", {'layout': 'monadtall'}),
               ("TERM", {'layout': 'monadtall'}),
               ("CODE", {'layout': 'monadtall'}),
               ("SLACK", {'layout': 'max'}),
               ("EMAIL", {'layout': 'max'}),
               ("DOCS", {'layout': 'monadtall'}),
               ("MUS", {'layout': 'monadtall'}),
               ("VID", {'layout': 'monadtall'}),
               ("GAMES", {'layout': 'floating'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen(), desc="Switch to Workspace {}".format(i)))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name), desc="Move focused window to Workspace {}".format(i))) # Send current window to another group


layout_theme = {
    "border_width": 2,
    "margin": 8,
    "border_focus": "e1acff",
    "border_normal": "1D2330"
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme),
    # layout.Columns(border_focus_stack='#d75f5f'),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

colors = [["#282c34", "#282c34"], # panel background
          ["#3d3f4b", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#74438f", "#74438f"], # border line color for 'other tabs' and color for 'odd widgets'
          ["#4f76c7", "#4f76c7"], # color for the 'even widgets'
          ["#e1acff", "#e1acff"], # window name
          ["#ecbbfb", "#ecbbfb"]] # backbround for inactive screens

prompt = "{0}@{1}: ".format(os.environ["USER"], "Machine")

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
        widget.Sep(
            linewidth = 0,
            padding = 6,
            foreground = colors[2],
            background = colors[0]
        ),
        widget.GroupBox(
            font = "Ubuntu Bold",
            fontsize = 9,
            margin_y = 3,
            margin_x = 0,
            padding_y = 5,
            padding_x = 3,
            borderwidth = 3,
            active = colors[2],
            inactive = colors[7],
            rounded = False,
            highlight_color = colors[1],
            highlight_method = "line",
            this_current_screen_border = colors[6],
            this_screen_border = colors [4],
            other_current_screen_border = colors[6],
            other_screen_border = colors[4],
            foreground = colors[2],
            background = colors[0]
        ),
        widget.Prompt(
            prompt = prompt,
            font = "Ubuntu Mono",
            padding = 10,
            foreground = colors[3],
            background = colors[1]
        ),
        widget.Sep(
            linewidth = 0,
            padding = 40,
            foreground = colors[2],
            background = colors[0]
        ),
        widget.WindowName(
            foreground = colors[6],
            background = colors[0],
            padding = 0
        ),
        widget.Sep(
            linewidth = 0,
            padding = 6,
            foreground = colors[0],
            background = colors[0]
        ),
        widget.TextBox(
            text = '',
            background = colors[0],
            foreground = colors[5],
            padding = 0,
            fontsize = 37
        ),
        widget.Net(
            interface = "wlp59s0",
            format = '{down} ↓↑ {up}',
            foreground = colors[2],
            background = colors[5],
            padding = 5
        ),
        widget.TextBox(
            text = '',
            background = colors[5],
            foreground = colors[4],
            padding = 0,
            fontsize = 37
        ),
        widget.CheckUpdates(
            update_interval = 1800,
            distro = "Arch_checkupdates",
            display_format = " {updates} Updates ",
            no_update_string = " Updated ",
            foreground = colors[2],
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e sudo pacman -Syu')},
            background = colors[4]
        ),
        widget.TextBox(
            text='',
            background = colors[4],
            foreground = colors[5],
            padding = 0,
            fontsize = 37
        ),
        widget.Memory(
            foreground = colors[2],
            background = colors[5],
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e htop')},
            padding = 5
        ),
        widget.TextBox(
            text = '',
            background = colors[5],
            foreground = colors[4],
            padding = 0,
            fontsize = 37
        ),
        widget.TextBox(
            text = " ",
            foreground = colors[2],
            background = colors[4],
            padding = 0
        ),
        widget.Volume(
            foreground = colors[2],
            background = colors[4],
            padding = 5
        ),
        widget.TextBox(
            text = '',
            background = colors[4],
            foreground = colors[5],
            padding = 0,
            fontsize = 37
        ),
        widget.CurrentLayoutIcon(
            custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
            foreground = colors[2],
            background = colors[5],
            padding = 0,
            scale = 0.7
        ),
        widget.CurrentLayout(
            foreground = colors[2],
            background = colors[5],
            padding = 5
        ),
        widget.TextBox(
            text = '',
            background = colors[5],
            foreground = colors[4],
            padding = 0,
            fontsize = 37
        ),
        widget.TextBox(
            text = "  ",
            foreground = colors[2],
            background = colors[4],
            padding = 0
        ),
        widget.Battery(
            foreground = colors[2],
            background = colors[4],
            notify_below=15,
            charge_char="",
            discharge_char="",
            format='{percent:2.0%} {char}',
        ),
        widget.TextBox(
            text = '',
            background = colors[4],
            foreground = colors[5],
            padding = 0,
            fontsize = 37
        ),
        widget.Clock(
            foreground = colors[2],
            background = colors[5],
            format = "%a, %B %d - %H:%M "
        ),
        widget.TextBox(
            text = '',
            background = colors[5],
            foreground = colors[4],
            padding = 0,
            fontsize = 37
        ),
        widget.Systray(
            foreground = colors[2],
            background = colors[4],
            padding = 5
        ),
        widget.TextBox(
            text = " ",
            foreground = colors[2],
            background = colors[4],
        ),
    ]
    return widgets_list

def init_widgets_screen_secondary():
    widgets_screen_secondary = init_widgets_list()
    del widgets_screen_secondary[7:8]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen_secondary

def init_widgets_screen_primary():
    widgets_screen_primary = init_widgets_list()
    return widgets_screen_primary                 # Primary monitor will display all widgets in widgets_list

def init_screens():
    return [
        # Screen(top=bar.Bar(widgets=init_widgets_screen_secondary(), opacity=1.0, size=20)),
        Screen(top=bar.Bar(widgets=init_widgets_screen_primary(), opacity=1.0, size=20)),
        # Screen(top=bar.Bar(widgets=init_widgets_screen_secondary(), opacity=1.0, size=20))
    ]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen_secondary = init_widgets_screen_secondary()
    widgets_screen_primary = init_widgets_screen_primary()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# Autostart apps
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

wmname = "Qtile"
