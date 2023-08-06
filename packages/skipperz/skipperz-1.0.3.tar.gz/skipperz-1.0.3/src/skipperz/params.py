import pygame


class ParamObject:
    pass


bad_guy_1_animation = ['assets/mechant1-c.png','assets/mechant2-c.png','assets/mechant3-c.png','assets/mechant4-c.png', 'assets/mechant5-c.png']
hero_1_animation = ['assets/spaceship-2135750_165.png']
explosion_1_animation = ['assets/BoumA1.png', 'assets/BoumA2.png', 'assets/BoumA3.png', 'assets/BoumA2.png', 'assets/BoumA1.png']

sound_loop = "assets/457046__gerainsan__horror-pulsating-drone-loop.wav"
death_of_hero = "assets/218721__bareform__boom-bang.aiff"

throtle_sound = ParamObject()
throtle_sound.default = None
throtle_sound.top = None
throtle_sound.left = None
throtle_sound.down = None
throtle_sound.right = None

directional_key = ParamObject()
directional_key.left = [pygame.K_LEFT, pygame.K_q]
directional_key.right = [pygame.K_RIGHT, pygame.K_d]
directional_key.up = [pygame.K_UP, pygame.K_z]
directional_key.down = [pygame.K_DOWN, pygame.K_s]