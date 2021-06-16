from typing import List  # noqa: F401
import os
import subprocess

from libqtile import bar, layout, widget, hook, qtile, popup, configurable
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

mod = "mod4"
terminal = 'alacritty'


class KbdOverview(configurable.Configurable):
    defaults = [
        ('x', None, 'x position. Defaults to centering on screen.'),
        ('y', None, 'y position. Defaults to centering on screen.'),
        ('width', None, 'Width in pixels. Defaults to 75% screen width.'),
        ('height', None, 'Height in pixels. Defaults to 75% screen height.'),
        ('foreground', '#ffffff', 'Text colour.',),
        ('background', '#111111', 'Background colour.',),
        ('border', '#111111', 'Border colours. Or None for none.',),
        ('border_width', 4, 'Line width of borders.'),
        ('opacity', 0.8, 'Window opacity. Requires compositor.'),
        ('corner_radius', None, 'Corner radius for round corners, or None.'),
        ('font', 'Source Code Pro', 'Font.'),
        ('font_size', 14, 'Size of font.'),
        ('font_shadow', None, 'Color for text shadows, or None for no shadows.'),
    ]

    keys_ignored = (
        "XF86AudioMute",
        "XF86AudioLowerVolume",
        "XF86AudioRaiseVolume",
        "XF86AudioPlay",
        "XF86AudioNext",
        "XF86AudioPrev",
        "XF86AudioStop",
        "XF86MonBrightnessUp",
        "XF86MonBrightnessDown"
    )

    text_replaced = {
        "mod4": "Super",
        "control": "Ctrl",
        "mod1": "Alt",
        "shift": "Shift",
        "twosuperior": "²",
        "less": "<",
        "ampersand": "&",
        "Escape": "Esc",
        "Return": "Enter",
    }

    def __init__(self, **config):
        configurable.Configurable.__init__(self, **config)
        self.add_defaults(KbdOverview.defaults)
        self._window = None
        self._shown = False
        hook.subscribe.startup_complete(self.configure)

    def configure(self):
        # if self.border_width:
        #     self.border =  #qtile.color_pixel(self.border)  # this will need updating
        if self.width is None:
            self.width = int(qtile.screens[0].width * 6/8)
        if self.height is None:
            self.height = int(qtile.screens[0].height * 6/8)
        if self.x is None:
            self.x = int(qtile.current_screen.width * 1/8)
        if self.y is None:
            self.y = int(qtile.current_screen.height * 1/8)

        popup_config = {}
        for opt in popup.Popup.defaults:
            key = opt[0]
            if hasattr(self, key):
                popup_config[key] = getattr(self, key)

        self._window = popup.Popup(
            qtile, **popup_config, x=self.x, y=self.y, width=self.width, height=self.height
        )
        self._window.win.handle_ButtonPress = self._button_press
        self._window.clear()

        # title
        self._window.layout.font_size = 24
        self._window.text = 'Keyboard Shortcuts'        
        self._window.draw_text(y=28, x=(self._window.width / 2) - (self._window.layout.width / 2))
        self._window.drawer.draw_hbar(
            self.foreground + '.5', self.width * 1/8, self.width * 7/8, 76
        )

        # binding information should go here
        self._window.layout.font_size = self.font_size
        template = " \t\t\t {0:30}| \t {1:50}" # column widths: 30, 50
        i=0
        for key in keys:
            if key.key not in self.keys_ignored:
                modifiers = ""
                bindings = ""
                description = key.desc.title()

                for m in key.modifiers:
                    if m in self.text_replaced.keys():
                        modifiers += self.text_replaced[m] + " + "
                    else:
                        modifiers += m.capitalize() + " + "

                if len(key.key) > 1:
                    if key.key in self.text_replaced.keys():
                        bindings = self.text_replaced[key.key]
                    else:
                        bindings = key.key.title()
                else:
                    bindings = key.key

                self._window.text = template.format(modifiers+bindings, description)
                y = 80 + i * self._window.layout.height
                self._window.draw_text(y=y)
                i += 1

    def _button_press(self, event):
        if event.detail == 1:
            self.hide()

    def toggle(self, *args, **kwargs):
        if self._shown:
            self.hide()
        else:
            self.show()

    def hide(self):
        self._window.hide()
        self._shown = False

    def show(self, qtile=None):
        self._window.unhide()
        self._window.draw()
        self._shown = True

kbdoverview = KbdOverview()


keys = [
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    # Keyboard quick settings keys
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%"), desc="Increase Brightnes"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-"), desc="Decrease Brightnes"),
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle"), desc="Mute"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 sset Master 1- unmute"), desc="Decrease Volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 sset Master 1+ unmute"), desc="Increase Volume"),

    # Lockscreen
    Key([mod], "l", lazy.spawn("betterlockscreen -l dimblur"), desc="Lock screen, to update the image run 'betterlockscreen -u ~/path/to/picture'"),

    # Display Keybindings in a popup reference: https://github.com/qtile/qtile/issues/1329#issuecomment-742868703 https://github.com/qtile/qtile/blob/master/libqtile/popup.py
    Key([mod], "k", lazy.function(kbdoverview.toggle), desc="Display keybindings in a popup"),

    # Take screenshot
    Key([], "Print", lazy.spawn("scrot /home/pushp/Pictures/Screenshot-%Y-%m-%d-%H_%M_%S.jpg"), desc="Take a screenshot"),
]

group_names = [("WEB", {'layout': 'monadtall'}),
               ("TERM", {'layout': 'monadtall'}),
               ("CODE", {'layout': 'monadtall'}),
               ("SLACK", {'layout': 'max'}),
               ("EMAIL", {'layout': 'max'}),
               ("DOCS", {'layout': 'monadtall'}),
               ("MUS", {'layout': 'monadtall'}),
               ("VID", {'layout': 'monadtall'}),
               ("GFX", {'layout': 'floating'})]

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
