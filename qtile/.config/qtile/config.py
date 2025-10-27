from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
from pathlib import Path
import subprocess
os.environ["XCURSOR_THEME"] = "Classic-Flat-White"
os.environ["XCURSOR_SIZE"] = "24"
os.environ["QT_QPA_PLATFORMTHEME"] = "qt5ct" 

mod = "mod4"
terminal = guess_terminal()

myTerm = "alacritty"      # My terminal of choice

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "v", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "d", lazy.spawn("rofi -show drun -show-icons"), desc='Run Launcher'),
    Key([mod], "b", lazy.spawn("librewolf"), desc='browser'),
    Key(
        ["control"], 
        "F12",
        lazy.spawn('sh -c "maim -s | xclip -selection clipboard -t image/png -i"'),
        desc="Screenshot"
    ),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            # Key(
            #     [mod, "shift"],
            #     i.name,
            #     lazy.window.togroup(i.name, switch_group=True),
            #     desc=f"Switch to & move focused window to group {i.name}",
            # ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
                desc="move focused window to group {}".format(i.name)),
        ]
    )

colors = [
    ["#2d2a2e", "#2d2a2e"],  # bg        (primary.background)
    ["#fff1f3", "#fff1f3"],  # fg        (primary.foreground)
    ["#2c2525", "#2c2525"],  # color01   (normal.black)
    ["#fd6883", "#fd6883"],  # color02   (normal.red)
    ["#adda78", "#adda78"],  # color03   (normal.green)
    ["#f9cc6c", "#f9cc6c"],  # color04   (normal.yellow)
    ["#f38d70", "#f38d70"],  # color05   (normal.blue)
    ["#a8a9eb", "#a8a9eb"],  # color06   (normal.magenta)
    ["#85dacc", "#85dacc"],  # color15   (bright.cyan)
    ["#72696a", "#72696a"]   # color[9]  (bright.black)
]


# helper in case your colors are ["#hex", "#hex"]
def C(x): return x[0] if isinstance(x, (list, tuple)) else x

layout_theme = {
    "border_width" : 0,
    "margin" : 0,
    "border_focus" : colors[4],
    "border_normal" : colors[4],
}

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font Propo Bold",
    # font="Ubuntu Bold",
    fontsize=14,
    padding=0,
    background=colors[0],
)


extension_defaults = widget_defaults.copy()

sep = widget.Sep(linewidth=1, padding=8, foreground=colors[9])

screens = [
    Screen(
    	wallpaper="/home/user/.config/walls/forest.jpg",
    	wallpaper_mode="fill",
        top=bar.Bar(
            widgets = [
                widget.Spacer(length = 8),
                widget.Prompt(
                    font = "Ubuntu Mono",
                    fontsize=14,
                    foreground = colors[1]
                ),
                widget.GroupBox(
                    fontsize = 16,
                    margin_y = 5,
                    margin_x = 5,
                    padding_y = 0,
                    padding_x = 2,
                    borderwidth = 3,
                    active = colors[4],
                    inactive = colors[9],
                    rounded = False,
                    highlight_color = colors[0],
                    highlight_method = "line",
                    this_current_screen_border = colors[4],
                    this_screen_border = colors [5],
                    other_current_screen_border = colors[4],
                    other_screen_border = colors[5],
                ),
                widget.TextBox(
                    text = '|',
                    font = "JetBrainsMono Nerd Font Propo Bold",
                    foreground = colors[9],
                    padding = 2,
                    fontsize = 14
                ),
                widget.CurrentLayout(
                    foreground = colors[9],
                    padding = 5
                ),
                widget.TextBox(
                    text = '',
                    font = "JetBrainsMono Nerd Font Propo Bold",
                    foreground = colors[9],
                    padding = 2,
                    fontsize = 14
                ),
		widget.Spacer(length=bar.STRETCH),
                widget.Systray(padding = 6),
                widget.Clock(
                    foreground = colors[4],
                    padding = 8, 
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('notify-date')},
                    ## Uncomment for date and time 
                    format = "%a, %b %d - %H:%M",
                    ## Uncomment for time only
                    # format = "%I:%M %p",
                ),
                widget.Spacer(length = 8),
            ],
            # 24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"],  # Borders are magenta
            margin=[0, 0, 1, 0], 
            size=30
        ),
    ),
        Screen(
    	wallpaper="/home/user/.config/walls/forest.jpg",
    	wallpaper_mode="fill",
        top=bar.Bar(
            widgets = [
                widget.Spacer(length = 8),
                widget.Prompt(
                    font = "Ubuntu Mono",
                    fontsize=14,
                    foreground = colors[1]
                ),
                widget.GroupBox(
                    fontsize = 16,
                    margin_y = 5,
                    margin_x = 5,
                    padding_y = 0,
                    padding_x = 2,
                    borderwidth = 3,
                    active = colors[4],
                    inactive = colors[9],
                    rounded = False,
                    highlight_color = colors[0],
                    highlight_method = "line",
                    this_current_screen_border = colors[4],
                    this_screen_border = colors [5],
                    other_current_screen_border = colors[4],
                    other_screen_border = colors[5],
                ),
                widget.TextBox(
                    text = '|',
                    font = "JetBrainsMono Nerd Font Propo Bold",
                    foreground = colors[9],
                    padding = 2,
                    fontsize = 14
                ),
                widget.CurrentLayout(
                    foreground = colors[9],
                    padding = 5
                ),
                widget.TextBox(
                    text = '',
                    font = "JetBrainsMono Nerd Font Propo Bold",
                    foreground = colors[9],
                    padding = 2,
                    fontsize = 14
                ),
		widget.Spacer(length=bar.STRETCH),
                widget.Clock(
                    foreground = colors[4],
                    padding = 8, 
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('notify-date')},
                    ## Uncomment for date and time 
                    format = "%a, %b %d - %H:%M",
                    ## Uncomment for time only
                    # format = "%I:%M %p",
                ),
                widget.Spacer(length = 8),
            ],
            # 24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"],  # Borders are magenta
            margin=[0, 0, 1, 0], 
            size=30
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_width=0,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

wmname = "qtile"

@hook.subscribe.startup_once
def autostart():
    home = Path('~/.config/qtile/autostart.sh').expanduser()
    subprocess.run(home)
