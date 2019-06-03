import assets as gamepad_assets
import tkinter
from tkinter import ttk, colorchooser

import pygame

# TODO: run a tkinter gui asking for which controller, xbox or ps4
# TODO: set colour_key from GUI also

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED     =  ( 255,  100,  100)
COLOUR_KEY = (255, 0, 128) #fuchsia


class ControllerOverlayApp:

    def __init__(self, assets, gamepad_type: str, gamepad_number: int=0, trigger_deadzone: float=0.002):
        self.asset_map = assets
        self.asset_map.load()

        self.running = False
        self.window_is_framed = True
        self.trigger_deadzone = trigger_deadzone

        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(gamepad_number)
        self.controller.init()
        self.BUTTON_TRANSLATION = gamepad_assets.ButtonTranslator(gamepad_type.lower())

        pygame.init()
        size = self.asset_map._base.get_size()
        self.window_size = (size[0] + 10, size[1] + 10)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption('Controller Visualisation Overlay')

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3: # right click to make frame available, so we can move the window around easily
                        if not self.window_is_framed:
                            self.window_is_framed = True
                            self.screen = pygame.display.set_mode(self.window_size)
                        else:
                            self.window_is_framed = False
                            self.screen = pygame.display.set_mode(self.window_size, pygame.NOFRAME)

            self.screen.fill(COLOUR_KEY)
            self.screen.blit(self.asset_map._base, (5, 5))

            for button_num in range(self.controller.get_numbuttons()):
                button_is_pressed = self.controller.get_button(button_num)
                button_ID = self.BUTTON_TRANSLATION(button_num)
                if button_ID in self.asset_map.analogs and not button_is_pressed:
                    if button_ID == self.asset_map.left_analog:
                        left_analog = self.asset_map[button_ID][button_is_pressed]
                    else:
                        right_analog = self.asset_map[button_ID][button_is_pressed]
                elif button_ID in self.asset_map.analogs and button_is_pressed:
                    if button_ID == self.asset_map.left_analog:
                        left_analog = self.asset_map[button_ID][button_is_pressed]
                    else:
                        right_analog = self.asset_map[button_ID][button_is_pressed]
                elif button_ID not in self.asset_map.analogs:
                    try:
                        btndat = self.asset_map[button_ID][button_is_pressed]
                        self.screen.blit(btndat['img'], btndat['loc'])
                    except (KeyError, TypeError):
                        continue

            dpad_state =  self.controller.get_hat(0)
            for im, loc in self.asset_map[dpad_state]:
                self.screen.blit(im, loc)

            # Analog Stick movement
            left_ana_horiz, left_ana_verti = round(self.controller.get_axis(self.BUTTON_TRANSLATION(self.asset_map.left_stick_x)), 2), round(self.controller.get_axis(self.BUTTON_TRANSLATION(self.asset_map.left_stick_y)), 2)
            right_ana_horiz, right_ana_verti = round(self.controller.get_axis(self.BUTTON_TRANSLATION(self.asset_map.right_stick_x)), 2), round(self.controller.get_axis(self.BUTTON_TRANSLATION(self.asset_map.right_stick_y)), 2)

            self.screen.blit(left_analog['img'], (left_analog['loc'][0] + (30 * left_ana_horiz), left_analog['loc'][1] + (30 * left_ana_verti)))
            self.screen.blit(right_analog['img'], (right_analog['loc'][0] + (30 * right_ana_horiz), right_analog['loc'][1] + (30 * right_ana_verti)))
            
            lt = self.asset_map.left_trigger
            rt = self.asset_map.right_trigger
            if max(0, (self.controller.get_axis(5) + 1) / 2) > self.trigger_deadzone:
                self.screen.blit(lt['img'], lt['loc'])
            if max(0, (self.controller.get_axis(4) + 1) / 2) > self.trigger_deadzone:
                self.screen.blit(rt['img'], rt['loc'])
            pygame.display.update()

supported_gps = ('PlayStation 4', 'Xbox One')
assets =  None
gp_using = None
should_continue = False
platform_map = {
    1: (gamepad_assets.Xbox1Assets, 'xbox1'),
    0: (gamepad_assets.PS4Assets, 'ps4')
}


root = tkinter.Tk()
root.geometry('300x200')
root.title('Gamepad Overlay Launcher')
lbl = tkinter.Label(root, text='Gamepad: ', font=('lucon.ttf', 18))
choices = ttk.Combobox(root, values=supported_gps)
choices.current(0)
# print(dir(choices))

lbl.grid(column=0, row=0)
choices.grid(column=1, row=0)

def get_colour():
    global COLOUR_KEY
    col = colorchooser.askcolor()
    COLOUR_KEY = col[0]


def gp_launch():
    global assets, gp_using, should_continue
    idx = choices.current()
    data = platform_map[idx]
    assets = data[0]()
    gp_using = data[1]
    should_continue = True
    root.destroy()

set_colour = tkinter.Button(root, text='Set Background Colour', command=get_colour)
set_colour.grid(column=1, row=1)
launch = tkinter.Button(root, text='Launch', command=gp_launch)
launch.grid(column=1, row=2)



root.mainloop()
if should_continue:
    app = ControllerOverlayApp(assets, gp_using)
    app.run()
    pygame.quit()
