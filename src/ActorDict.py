from panda3d.core import loadPrcFile

from direct.actor.Actor import Actor
loadPrcFile('../config/Config.prc')
playerBody = Actor({
    # model dict
    'suit': 'phase_3.5/models/char/suitB-mod.bam'},

    # anim dict
    {'suit': {'neutral': 'phase_4/models/char/suitB-neutral.bam',
              'walk': 'phase_4/models/char/suitB-walk.bam'}}
)

playerHead = {'sun': 'phase_4/models/props/sun.bam'}

Goon = Actor({
    # model dict
    'body': 'phase_9/models/char/Cog_Goonie-zero.bam'},

    # anim dict
    {'body': {'walk': 'phase_9/models/char/Cog_Goonie-walk.bam'}}
)
