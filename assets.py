import pathlib
import pygame

def load_image(path):
    return pygame.image.load(str(path))


class ButtonTranslator:

    ps4 = {
        0: 'westButton',
        1: 'southButton',
        2: 'eastButton',
        3: 'northButton',
        4: 'leftBumper',
        5: 'rightBumper',
        6: 'leftTrigger',
        7: 'rightTrigger',
        8: 'leftCenterButton',
        9: 'rightCenterButton',
        10: 'leftJoystick',
        11: 'rightJoystick',
        12: 'platformButton',
        13: 'centerButton',
        'LeftStickX': 0, # the axis that leftstickx will be for a ps4 controller
        'LeftStickY': 1,
        'RightStickX': 2,
        'RightStickY': 3
    }

    xbox1 = {
        0: 'southButton',
        1: 'eastButton',
        2: 'westButton',
        3: 'northButton',
        4: 'leftBumper',
        5: 'rightBumper',
        6: 'leftCenterButton',
        7: 'rightCenterButton',
        8: 'leftJoystick',
        9: 'rightJoystick',
        'LeftStickX': 0,
        'LeftStickY': 1,
        'RightStickX': 3,
        'RightStickY': 4
    }

    def __init__(self, platform: str):
        """
        platform - the actual platform of the gamepad so we can translate the button numbers into their respective controls
        """
        self.platform = platform.lower()

    def __call__(self, item):
        if self.platform == 'ps4':
            try:
                return self.ps4[item]
            except KeyError:
                pass
        elif self.platform == 'xbox1':
            try:
                return self.xbox1[item]
            except KeyError:
                pass



class PS4Assets:

    analogs = ('leftJoystick', 'rightJoystick')
    left_analog = 'leftJoystick'
    right_analog = 'rightJoystick'

    left_stick_x = 'LeftStickX'
    left_stick_y = 'LeftStickY'
    right_stick_x = 'RightStickX'
    right_stick_y = 'RightStickY'

    def __init__(self):
        self._loaded = False
        self._assets = {}
        self._files = pathlib.Path(__file__).parent / 'main_assets' / 'ps4' / 'pngs'

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._assets[item]
        elif isinstance(item, tuple): # Hat/ DPAD value
            imgs = []
            for idx, i in enumerate(item):
                if i == 0:
                    continue
                else:
                    dat = self._assets['DPAD'][idx][i]
                    imgs.append((dat['img'], dat['loc']))
            return imgs

    @property
    def loaded(self):
        return self._loaded

    def load(self):
        self._base = load_image(self._files / 'controller_base.png')
        self.left_trigger = {'img': load_image(self._files / 'left_trigger_pressed.png'), 'loc': (113, 5)}
        self.right_trigger = {'img': load_image(self._files / 'right_trigger_pressed.png'), 'loc': (602, 5)}
        bumper = load_image(self._files / 'bumper_pressed.png')
        joystick_up = load_image(self._files / 'stick_released.png')
        self._assets = {
            'southButton': {1: {'img': load_image(self._files / 'X_pressed.png'), 'loc': (628, 279)}},
            'eastButton': {1: {'img': load_image(self._files / 'Circle_pressed.png'), 'loc': (686, 222)}},
            'westButton': {1: {'img': load_image(self._files / 'Square_pressed.png'), 'loc': (570, 222)}},
            'northButton': {1: {'img': load_image(self._files / 'Triangle_pressed.png'), 'loc': (628, 164)}},
            'leftBumper': {1:{'img': bumper, 'loc': (114, 99)}},
            'rightBumper': {1:{'img': pygame.transform.flip(bumper, True, False), 'loc': (603, 99)}},
            'leftCenterButton': {1:{'img': load_image(self._files / 'share_pressed.png'), 'loc': (232, 148)}},
            'rightCenterButton': {1:{'img': load_image(self._files / 'options_pressed.png'), 'loc': (556, 148)}},
            'centerButton' : {1:{'img': load_image(self._files / 'touchpad_pressed.png'), 'loc': (277, 127)}},
            'platformButton': {1:{'img': load_image(self._files / 'ps_pressed.png'), 'loc': (387, 344)}},
            'leftJoystick': {
                0: {'img': joystick_up, 'loc': (235, 313)},
                1: {'img': load_image(self._files / 'left_stick_pressed.png'), 'loc': (235, 313)}
            },
            'rightJoystick': {
                0: {'img': joystick_up, 'loc': (491, 314)},
                1: {'img': load_image(self._files / 'right_stick_pressed.png'), 'loc': (491, 314)}
            },
            'DPAD' : { 
                0: {
                    -1: {'img': load_image(self._files / 'dpad_left.png'), 'loc': (98, 230)}, 
                    1: {'img': load_image(self._files / 'dpad_right.png'), 'loc': (168, 230)}
                },
                1: {
                    -1: {'img': load_image(self._files / 'dpad_down.png'), 'loc': (140, 259)}, 
                    1: {'img': load_image(self._files / 'dpad_up.png'), 'loc': (140, 186)}
                }
            }
        }
        self._loaded = True


class Xbox1Assets:

    analogs = ('leftJoystick', 'rightJoystick')
    left_analog = 'leftJoystick'
    right_analog = 'rightJoystick'

    left_stick_x = 'LeftStickX'
    left_stick_y = 'LeftStickY'
    right_stick_x = 'RightStickX'
    right_stick_y = 'RightStickY'

    def __init__(self):
        self._loaded = False
        self._assets = {}
        self._files = pathlib.Path(__file__).parent / 'main_assets' / 'xbox1' / 'pngs'

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._assets[item]
        elif isinstance(item, tuple): # Hat/ DPAD value
            imgs = []
            for idx, i in enumerate(item):
                if i == 0:
                    continue
                else:
                    dat = self._assets['DPAD'][idx][i]
                    imgs.append((dat['img'], dat['loc']))
            return imgs

    @property
    def loaded(self):
        return self._loaded
    
    def load(self):
        self._base = load_image(self._files / 'controller_base.png')
        self.left_trigger = {'img': load_image(self._files / 'trigger_pressed.png'), 'loc': (156, 6)}
        self.right_trigger = {'img': pygame.transform.flip(self.left_trigger['img'], True, False), 'loc': (515, 6)}
        bumper = load_image(self._files / 'bumper_pressed.png')
        joystick_up = load_image(self._files / 'joystick_released.png')
        joystick_down = load_image(self._files / 'joystick_pressed.png')
        self._assets = {
            'southButton': {
                1: {'img': load_image(self._files / 'A_pressed.png'), 'loc': (548, 311)},
                0: {'img': load_image(self._files / 'A_released.png'), 'loc': (548, 311)}
            },
            'eastButton': {
                1: {'img': load_image(self._files / 'B_pressed.png'), 'loc': (598, 261)},
                0: {'img': load_image(self._files / 'B_released.png'), 'loc': (598, 261)}
            },
            'westButton': {
                1: {'img': load_image(self._files / 'X_pressed.png'), 'loc': (497, 261)},
                0: {'img': load_image(self._files / 'X_released.png'), 'loc': (497, 261)}
            },
            'northButton': {
                1: {'img': load_image(self._files / 'Y_pressed.png'), 'loc': (547, 210)},
                0: {'img': load_image(self._files / 'Y_released.png'), 'loc': (547, 210)}
            },
            'leftBumper': {1:{'img': bumper, 'loc': (113, 134)}},
            'rightBumper': {1:{'img': pygame.transform.flip(bumper, True, False), 'loc': (477, 134)}},
            'leftCenterButton': {1:{'img': load_image(self._files / 'start_pressed.png'), 'loc': (311, 268)}},
            'rightCenterButton': {1:{'img': load_image(self._files / 'select_pressed.png'), 'loc': (418, 268)}},
            'leftJoystick': {
                0: {'img': joystick_up, 'loc': (150, 241)},
                1: {'img': joystick_down, 'loc': (150, 241)}
            },
            'rightJoystick': {
                0: {'img': joystick_up, 'loc': (436, 356)},
                1: {'img': joystick_down, 'loc': (436, 356)}
            },
            'DPAD' : { 
                0: {
                    -1: {'img': load_image(self._files / 'dpad_left.png'), 'loc': (228, 388)}, 
                    1: {'img': load_image(self._files / 'dpad_right.png'), 'loc': (283, 388)}
                },
                1: {
                    -1: {'img': load_image(self._files / 'dpad_down.png'), 'loc': (266, 406)}, 
                    1: {'img': load_image(self._files / 'dpad_up.png'), 'loc': (265, 350)}
                }
            }
        }
        self._loaded = True


