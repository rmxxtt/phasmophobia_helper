import json
import math
import tkinter as tk
from enum import Enum, auto, IntFlag
from tkinter import ttk, PhotoImage, font
from typing import TypedDict, Generator, Any

# TODO gettext
_ = lambda x: x


class Paranormal(IntFlag):
    """ List of paranormal events """

    NONE = 0

    _('AREA_OBJECTS_INTERACTION_LITTLE')
    AREA_OBJECTS_INTERACTION_LITTLE = auto()
    _('AREA_OBJECTS_INTERACTION_MANY')
    AREA_OBJECTS_INTERACTION_MANY = auto()

    _('ELECTRICITY_GENERATOR_OFF')
    ELECTRICITY_GENERATOR_OFF = auto()
    _('ELECTRICITY_LIGHTBULB_BREAK')
    ELECTRICITY_LIGHTBULB_BREAK = auto()
    _('ELECTRICITY_LIGHTBULB_OFF')
    ELECTRICITY_LIGHTBULB_OFF = auto()

    _('GHOST_MODEL_CHANGE')
    GHOST_MODEL_CHANGE = auto()
    _('GHOST_SPEED_FAST')
    GHOST_SPEED_FAST = auto()
    _('GHOST_SPEED_NORMAL')
    GHOST_SPEED_NORMAL = auto()
    _('GHOST_SPEED_SLOW')
    GHOST_SPEED_SLOW = auto()
    _('GHOST_SPEED_BOOST_COLD')
    GHOST_SPEED_BOOST_COLD = auto()
    _('GHOST_SPEED_BOOST_ELECTRICITY')
    GHOST_SPEED_BOOST_ELECTRICITY = auto()
    _('GHOST_SPEED_BOOST_PLAYER')
    GHOST_SPEED_BOOST_PLAYER = auto()
    _('GHOST_SPEED_BOOST_REASON')
    GHOST_SPEED_BOOST_REASON = auto()
    _('GHOST_SPEED_SLOWDOWN_PLAYER')
    GHOST_SPEED_SLOWDOWN_PLAYER = auto()

    _('ITEM_VIDEO_CAMERA_ORB')
    ITEM_VIDEO_CAMERA_ORB = auto()
    _('ITEM_DOTS_PROJECTOR')
    ITEM_DOTS_PROJECTOR = auto()
    _('ITEM_EMF_READER')
    ITEM_EMF_READER = auto()
    _('ITEM_GHOST_WRITING_BOOK')
    ITEM_GHOST_WRITING_BOOK = auto()

    _('ITEM_SPIRIT_BOX')
    ITEM_SPIRIT_BOX = auto()
    _('ITEM_THERMOMETER_FREEZING_TEMPERATURES')
    ITEM_THERMOMETER_FREEZING_TEMPERATURES = auto()
    _('ITEM_UV_LIGHT_OR_GLOWSTICK_FINGERPRINTS')
    ITEM_UV_LIGHT_OR_GLOWSTICK_FINGERPRINTS = auto()

    _('GHOST_FINGERPRINTS_FIVE')
    GHOST_FINGERPRINTS_FIVE = auto()
    _('GHOST_FINGERPRINTS_SIX')
    GHOST_FINGERPRINTS_SIX = auto()
    _('GHOST_FINGERPRINTS_CLAWS')
    GHOST_FINGERPRINTS_CLAWS = auto()

    ALL = ~NONE


class GhostsEnum(Enum):
    """ Ghost list """

    _('Banshee')
    Banshee = auto()
    _('Demon')
    Demon = auto()
    _('Deogen')
    Deogen = auto()
    _('Goryo')
    Goryo = auto()
    _('Hantu')
    Hantu = auto()
    _('Jinn')
    Jinn = auto()
    _('Mare')
    Mare = auto()
    _('Moroi')
    Moroi = auto()
    _('Myling')
    Myling = auto()
    _('Obake')
    Obake = auto()
    _('Oni')
    Oni = auto()
    _('Onryo')
    Onryo = auto()
    _('Phantom')
    Phantom = auto()
    _('Poltergeist')
    Poltergeist = auto()
    _('Raiju')
    Raiju = auto()
    _('Revenant')
    Revenant = auto()
    _('Shade')
    Shade = auto()
    _('Spirit')
    Spirit = auto()
    _('Thaye')
    Thaye = auto()
    _('The_Mimic')
    The_Mimic = auto()
    _('The_Twins')
    The_Twins = auto()
    _('Wraith')
    Wraith = auto()
    _('Yokai')
    Yokai = auto()
    _('Yurei')
    Yurei = auto()


class Mask:
    """ Bitmask """

    def __init__(self):
        self.__mask = Paranormal.NONE

    @property
    def get(self):
        return self.__mask

    def set(self, *flags: Paranormal):
        for flag in flags:
            self.__mask |= flag

    def delete(self, *flags: Paranormal):
        for flag in flags:
            self.__mask &= ~flag

    def toggle(self, *flags: Paranormal):
        for flag in flags:
            self.__mask ^= flag

    def reset(self):
        self.__mask = Paranormal.NONE

    def set_all(self):
        self.__mask = Paranormal.ALL

    def check(self, flag: Paranormal):
        """ For one flag """
        if flag.bit_count() != 1:
            raise ValueError('Expected count flags 1, got %s instead' % flag.bit_count())
        return self.__mask & flag

    def check_all(self, flags: Paranormal):
        """ For one or more flags. Checks if all flags from 'flags' are enabled in 'self.__mask' """
        return (self.__mask & flags) == flags

    def check_any(self, flags: Paranormal):
        """ For one or more flags. Checks if at least one flag is enabled """
        return self.__mask & flags


class Ghost:
    def __init__(self, ghost: GhostsEnum):
        self.__type = ghost
        self.__name = ghost.name
        self.__mask = Mask()

    @property
    def type(self):
        return self.__type

    @property
    def name(self):
        return self.__name

    @property
    def mask(self):
        return self.__mask


class GhostsInit:
    """ Init all ghosts """

    def __init__(self):
        self.__ghosts: list[Ghost] = []
        self.load_config()

    @property
    def get_all(self):
        return self.__ghosts

    def load_config(self):
        with open('./config/ghosts_config.json') as f:
            templates = json.load(f)

        for name, events in templates.items():
            ghost = Ghost(GhostsEnum[name])
            ghost.mask.set(*[Paranormal[i] for i in events])
            self.__ghosts.append(ghost)

    @staticmethod
    def create_config(file='./config/create_ghosts_config.json'):
        config = dict([(i.name, [p.name for p in list(Paranormal)[1:-1]]) for i in GhostsEnum])
        with open(file, 'w') as f:
            f.write(json.dumps(config, indent=4))


class GhostsButtons(TypedDict):
    button: ttk.Button
    ghost: Ghost
    generator: Generator[PhotoImage, Any, None]


class Icon:
    def __init__(self):
        self.choose = PhotoImage(file='./assets/icon/choose.png')
        self.discard = PhotoImage(file='./assets/icon/discard.png')
        self.empty = PhotoImage(file='./assets/icon/empty.png')


class Assets:
    def __init__(self):
        self.icon = Icon()


class App(tk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master)

        self.ui_main = None
        self.fonts: list[font.Font] = []
        self.ghosts = GhostsInit()

        self.ghosts_buttons: list[GhostsButtons] = []

        self.events_checkboxes: list[tk.BooleanVar] = []
        self.events_mask = Mask()
        """ Mask of all events flags """

        master.withdraw()

        master.title('Phasmophobia Helper')
        master.resizable(False, False)
        master.overrideredirect(False)
        master.update()

        self.assets = Assets()
        self.init_ui()

        master.deiconify()

    def init_ui(self):
        self.ui_main = ttk.Frame()
        self.ui_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.ui_ghost_events()
        self.ui_ghost_list()

    def ui_ghost_events(self):
        ui_main = ttk.LabelFrame(self.ui_main, text=_('Events'), labelanchor=tk.N, padding=10)
        ui_main.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        ui_reset_button = ttk.Button(ui_main, text=_('Reset events'), padding=(10, 2))
        ui_reset_button.configure(command=lambda: self.ui_reset_all_checkboxes())
        ui_reset_button.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))

        # For - Skip 'Paranormal' parameters, 'NONE' and 'ALL'
        for event in list(Paranormal)[1:-1]:
            var = tk.BooleanVar()
            var.set(False)
            button = ttk.Checkbutton(ui_main, text=_(event.name), variable=var, onvalue=True, offvalue=False,
                                     command=lambda v=var, e=event: self.ui_event_click(v, e))
            button.pack(anchor=tk.W)
            self.events_checkboxes.append(var)

    def ui_ghost_list(self):
        ui_main = ttk.LabelFrame(self.ui_main, text=_('Ghosts'), labelanchor=tk.N, padding=10)
        ui_main.pack(side=tk.RIGHT, fill=tk.Y)

        ui_column_1 = tk.Frame(ui_main)
        ui_column_2 = tk.Frame(ui_main)
        ui_reset_button = ttk.Button(ui_main, text=_('Reset settings'), padding=(10, 2))
        ui_reset_button.configure(command=lambda: self.ui_reset_all_icons())

        ui_reset_button.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        ui_column_2.pack(side=tk.RIGHT, fill=tk.Y)
        ui_column_1.pack(side=tk.LEFT, padx=(0, 10))

        tk_default_font = font.Font(font='TkDefaultFont').actual()
        family, size = tk_default_font['family'], tk_default_font['size']
        found_mask = font.Font(weight="bold", size=size)
        not_found_mask = font.Font(weight="normal", size=size)
        self.fonts.extend([found_mask, not_found_mask])

        ttk.Style().configure('FoundMask.TButton', font=found_mask, anchor=tk.W)
        ttk.Style().configure('NotFoundMask.TButton', font=not_found_mask, foreground="#777", anchor=tk.W)

        # Find the last element for the first column of ghosts
        ui_half = math.ceil(len(self.ghosts.get_all) / 2)

        # Generation of two columns
        for i, ghost in enumerate(self.ghosts.get_all):
            ui_select_column = ui_column_1 if i < ui_half else ui_column_2
            generator = self.circular_icon_generator()
            button = ttk.Button(ui_select_column, text=f' {_(ghost.name)}', style='NotFoundMask.TButton',
                                image=next(generator), compound=tk.LEFT,
                                width=self.max_len_ghost_name(), padding=(10, 8, 20, 8))
            # Circular change button icon on click
            button.configure(command=lambda b=button, g=generator: App.ui_next_icon(b, g))
            button.pack(fill=tk.X, ipadx=0, ipady=0, pady=(8, 0))
            # For further operations, such as changing styles
            self.ghosts_buttons.append(dict(button=button, generator=generator, ghost=ghost))

    def ui_event_click(self, var: tk.BooleanVar, event: Paranormal):
        if var.get():
            self.events_mask.set(event)
        else:
            self.events_mask.delete(event)
        self.search_ghosts_by_mask_of_all_checkboxes()

    def search_ghosts_by_mask_of_all_checkboxes(self):
        for element in self.ghosts_buttons:
            ghost = element['ghost']
            button = element['button']
            #
            if self.events_mask.get in [Paranormal.NONE, Paranormal.ALL]:
                button.configure(style='NotFoundMask.TButton')
                continue
            if ghost.mask.check_all(self.events_mask.get):
                button.configure(style='FoundMask.TButton')
            else:
                button.configure(style='NotFoundMask.TButton')

    def circular_icon_generator(self):
        """ Circular change button icon on click """
        while True:
            icons = [self.assets.icon.empty,
                     self.assets.icon.discard,
                     self.assets.icon.choose]
            for icon in icons:
                send = (yield icon)
                if send in ['reset']:
                    break

    @staticmethod
    def ui_next_icon(button: ttk.Button, generator: Generator):
        button.configure(image=next(generator))

    def ui_reset_all_icons(self):
        for element in self.ghosts_buttons:
            generator = element['generator']
            button = element['button']
            button.configure(image=generator.send('reset'))

    def ui_reset_all_checkboxes(self):
        for var in self.events_checkboxes:
            var.set(False)
        self.events_mask.reset()
        self.search_ghosts_by_mask_of_all_checkboxes()

    def max_len_ghost_name(self):
        return len(max([_(ghost.name) for ghost in self.ghosts.get_all], key=len))


if __name__ == '__main__':
    def main():
        master = tk.Tk()
        app = App(master)
        app.mainloop()


    main()
