from direct.actor.Actor import Actor

playerBody = Actor({
    # model dict
    'suit': 'phase_3.5\models\char\suitB-mod.bam'},

    # anim dict
    {'suit': {'neutral': 'phase_4/models/char/suitB-neutral.bam',
              'walk': 'phase_4/models/char/suitB-walk.bam'}}
)

playerHead = {'sun': 'phase_4/models/props/sun.bam'}