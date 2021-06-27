from libqtile import qtile, hook, popup, configurable
from libqtile.config import Key
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
    Key([mod, "shift"], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    # Keyboard quick settings keys
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%"), desc="Increase Brightnes"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-"), desc="Decrease Brightnes"),
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle"), desc="Mute"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 sset Master 1- unmute"), desc="Decrease Volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 sset Master 1+ unmute"), desc="Increase Volume"),

    # Lockscreen
    Key([mod], "l", lazy.spawn("betterlockscreen -l dimblur"), desc="Lock screen, to update the image run 'betterlockscreen -u ~/path/to/picture'"),

    # TODO: Toggle Touchpad
    # Key([mod], "t", lazy.spawn("synclient TouchpadOff=$((`synclient -l | grep TouchpadOff | awk '{print $3}'`==0))"), desc="Toggle Touchpad On/Off"),

    # Launch Rofi
    Key([mod], "r", lazy.spawn('rofi -modi "drun,window" -terminal alacritty -scroll-method 1  -show-icons -display-drun \"App" -show drun'), desc="Launch Rofi"),

    # Display Keybindings in a popup reference: https://github.com/qtile/qtile/issues/1329#issuecomment-742868703 https://github.com/qtile/qtile/blob/master/libqtile/popup.py
    Key([mod], "k", lazy.function(kbdoverview.toggle), desc="Display keybindings in a popup"),

    # Take screenshot
    Key([], "Print", lazy.spawn("scrot /home/pushp/Pictures/Screenshot-%Y-%m-%d-%H_%M_%S.jpg"), desc="Take a screenshot"),

    # Rofi Power menu
    Key([mod], "Escape", lazy.spawn('bash -c "~/.config/rofi/scripts/rofi-power"'), desc="Power Menu on Rofi"),
]
