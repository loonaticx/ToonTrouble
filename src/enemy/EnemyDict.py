ModelDict = {'a': ['/models/char/suitA-', 4],
             'b': ['/models/char/suitB-', 4],
             'c': ['/models/char/suitC-', 3.5]}
TutorialModelDict = {'a': ['/models/char/suitA-', 4],
                     'b': ['/models/char/suitB-', 4],
                     'c': ['/models/char/suitC-', 3.5]}

HeadModelDict = {'a': ['/models/char/suitA-', 4],
 'b': ['/models/char/suitB-', 4],
 'c': ['/models/char/suitC-', 3.5]}

EnemyParts = ['phase_3.5/models/char/suitA-mod',
            'phase_3.5/models/char/suitB-mod',
            'phase_3.5/models/char/suitC-mod',
            'phase_4/models/char/suitA-heads',
            'phase_4/models/char/suitB-heads',
            'phase_3.5/models/char/suitC-heads']
DefaultEnemyAnimations = [
    ['throw-paper', 'throw-paper', 5],
    ['shredder', 'shredder', 3.5],
    ['roll-o-dex', 'roll-o-dex', 5],
    ['speak', 'speak', 5]
]

EnemyAnimations = {
    'f': [['throw-paper', 'throw-paper', 3.5], ['phone', 'phone', 3.5], ['shredder', 'shredder', 3.5]],
    'p': [['pencil-sharpener', 'pencil-sharpener', 5],
          ['pen-squirt', 'pen-squirt', 5],
          ['hold-eraser', 'hold-eraser', 5],
          ['finger-wag', 'finger-wag', 5],
          ['hold-pencil', 'hold-pencil', 5]],
    'ym': [['throw-paper', 'throw-paper', 5],
           ['golf-club-swing', 'golf-club-swing', 5],
           ['magic3', 'magic3', 5],
           ['rubber-stamp', 'rubber-stamp', 5],
           ['smile', 'smile', 5]],
    'mm': [['speak', 'speak', 5],
           ['effort', 'effort', 5],
           ['magic1', 'magic1', 5],
           ['pen-squirt', 'fountain-pen', 5],
           ['finger-wag', 'finger-wag', 5]],
    'ds': [['magic1', 'magic1', 5],
           ['magic2', 'magic2', 5],
           ['throw-paper', 'throw-paper', 5],
           ['magic3', 'magic3', 5]],
    'hh': [['pen-squirt', 'fountain-pen', 7],
           ['glower', 'glower', 5],
           ['throw-paper', 'throw-paper', 5],
           ['magic1', 'magic1', 5],
           ['magic3', 'magic3', 5],
           ['roll-o-dex', 'roll-o-dex', 5]],
    'cr': [['pickpocket', 'pickpocket', 5], ['throw-paper', 'throw-paper', 3.5], ['glower', 'glower', 5]],
    'tbc': [['cigar-smoke', 'cigar-smoke', 8],
            ['glower', 'glower', 5],
            ['song-and-dance', 'song-and-dance', 8],
            ['golf-club-swing', 'golf-club-swing', 5]],
    'cc': [['speak', 'speak', 5],
           ['glower', 'glower', 5],
           ['phone', 'phone', 3.5],
           ['finger-wag', 'finger-wag', 5]],
    'tm': [['speak', 'speak', 5],
           ['throw-paper', 'throw-paper', 5],
           ['pickpocket', 'pickpocket', 5],
           ['roll-o-dex', 'roll-o-dex', 5],
           ['finger-wag', 'finger-wag', 5]],
    'nd': [['pickpocket', 'pickpocket', 5],
           ['roll-o-dex', 'roll-o-dex', 5],
           ['magic3', 'magic3', 5],
           ['smile', 'smile', 5]],
    'gh': [['speak', 'speak', 5], ['pen-squirt', 'fountain-pen', 5], ['rubber-stamp', 'rubber-stamp', 5]],
    'ms': [['effort', 'effort', 5],
           ['throw-paper', 'throw-paper', 5],
           ['stomp', 'stomp', 5],
           ['quick-jump', 'jump', 6]],
    'tf': [['phone', 'phone', 5],
           ['smile', 'smile', 5],
           ['throw-object', 'throw-object', 5],
           ['magic3', 'magic3', 5],
           ['glower', 'glower', 5]],
    'm': [['speak', 'speak', 5],
          ['magic2', 'magic2', 5],
          ['magic1', 'magic1', 5],
          ['golf-club-swing', 'golf-club-swing', 5],
          ['cigar-smoke', 'cigar-smoke', 8]],
    'mh': [['magic1', 'magic1', 5],
           ['smile', 'smile', 5],
           ['golf-club-swing', 'golf-club-swing', 5],
           ['song-and-dance', 'song-and-dance', 5]],
    'sc': [['throw-paper', 'throw-paper', 3.5], ['watercooler', 'watercooler', 5], ['pickpocket', 'pickpocket', 5]],
    'pp': [['throw-paper', 'throw-paper', 5], ['glower', 'glower', 5], ['finger-wag', 'fingerwag', 5]],
    'tw': [['throw-paper', 'throw-paper', 3.5],
           ['glower', 'glower', 5],
           ['magic2', 'magic2', 5],
           ['finger-wag', 'finger-wag', 5]],
    'bc': [['phone', 'phone', 5], ['hold-pencil', 'hold-pencil', 5]],
    'nc': [['phone', 'phone', 5], ['throw-object', 'throw-object', 5]],
    'mb': [['magic1', 'magic1', 5], ['throw-paper', 'throw-paper', 3.5]],
    'ls': [['throw-paper', 'throw-paper', 5], ['throw-object', 'throw-object', 5], ['hold-pencil', 'hold-pencil', 5]],
    'rb': [['glower', 'glower', 5], ['cigar-smoke', 'cigar-smoke', 8], ['magic1', 'magic1', 5],
           ['golf-club-swing', 'golf-club-swing', 5]],
    'bf': [['pickpocket', 'pickpocket', 5],
           ['rubber-stamp', 'rubber-stamp', 5],
           ['shredder', 'shredder', 3.5],
           ['watercooler', 'watercooler', 5]],
    'b': [['effort', 'effort', 5],
          ['throw-paper', 'throw-paper', 5],
          ['throw-object', 'throw-object', 5],
          ['magic1', 'magic1', 5]],
    'dt': [['rubber-stamp', 'rubber-stamp', 5],
           ['throw-paper', 'throw-paper', 5],
           ['speak', 'speak', 5],
           ['finger-wag', 'fingerwag', 5],
           ['throw-paper', 'throw-paper', 5]],
    'ac': [['throw-object', 'throw-object', 5],
           ['roll-o-dex', 'roll-o-dex', 5],
           ['stomp', 'stomp', 5],
           ['phone', 'phone', 5],
           ['throw-paper', 'throw-paper', 5]],
    'bs': [['magic1', 'magic1', 5], ['cigar-smoke', 'cigar-smoke', 8], ['throw-paper', 'throw-paper', 5],
           ['finger-wag', 'fingerwag', 5]],
    'sd': [['magic2', 'magic2', 5],
           ['quick-jump', 'jump', 6],
           ['stomp', 'stomp', 5],
           ['magic3', 'magic3', 5],
           ['hold-pencil', 'hold-pencil', 5],
           ['throw-paper', 'throw-paper', 5]],
    'le': [['speak', 'speak', 5],
           ['throw-object', 'throw-object', 5],
           ['glower', 'glower', 5],
           ['throw-paper', 'throw-paper', 5]],
    'bw': [['finger-wag', 'fingerwag', 5],
           ['cigar-smoke', 'cigar-smoke', 8],
           ['gavel', 'gavel', 8],
           ['magic1', 'magic1', 5],
           ['throw-object', 'throw-object', 5],
           ['throw-paper', 'throw-paper', 5]]
}