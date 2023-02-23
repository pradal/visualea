
# This file has been generated at Wed Feb 22 14:27:28 2023

from openalea.core import *


__name__ = 'dataflow_test'

__editable__ = True
__version__ = '0.0.1'
__license__ = 'Cecill-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'test simple data flow'
__url__ = 'https://github.com/openalea'
__icon__ = ''
__alias__ = []


__all__ = ['addition']



addition = CompositeNodeFactory(name='addition',
                             description='simple addition',
                             category='category test',
                             doc='',
                             inputs=[],
                             outputs=[],
                             elt_factory={  2: ('pkg_test', 'float'),
   3: ('pkg_test', 'float'),
   4: ('pkg_test', '+'),
   5: ('openalea.flow control', 'annotation'),
   6: ('openalea.flow control', 'annotation'),
   7: ('pkg_test', 'float')},
                             elt_connections={  140604922288400: (3, 0, 4, 0),
   140604922288432: (2, 0, 4, 1),
   140604922288464: (4, 0, 7, 0)},
                             elt_data={  2: {  'block': False,
         'caption': '2.1',
         'delay': 0,
         'hide': True,
         'id': 2,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': -245.9709450619092,
         'posy': -111.85872859148041,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   3: {  'block': False,
         'caption': '1.2',
         'delay': 0,
         'hide': True,
         'id': 3,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': -320.3252070658707,
         'posy': -111.0109722906813,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   4: {  'block': False,
         'caption': '+',
         'delay': 0,
         'hide': True,
         'id': 4,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': -314.20270829939903,
         'posy': -34.466726410245506,
         'priority': 0,
         'use_user_color': False,
         'user_application': False,
         'user_color': None},
   5: {  'id': 5,
         'posx': -364.22435123884213,
         'posy': -140.49860060790175,
         'txt': 'inputs'},
   6: {  'id': 6,
         'posx': -381.13154273993564,
         'posy': -60.87669916942594,
         'txt': 'addition'},
   7: {  'block': False,
         'caption': '3.3',
         'delay': 0,
         'hide': True,
         'id': 7,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': -311.29505256125043,
         'posy': 14.841906066585054,
         'priority': 0,
         'use_user_color': False,
         'user_application': True,
         'user_color': None},
   '__in__': {  'block': False,
                'caption': 'In',
                'delay': 0,
                'hide': True,
                'id': 0,
                'lazy': True,
                'port_hide_changed': set(),
                'posx': 0,
                'posy': 0,
                'priority': 0,
                'use_user_color': True,
                'user_application': None,
                'user_color': None},
   '__out__': {  'block': False,
                 'caption': 'Out',
                 'delay': 0,
                 'hide': True,
                 'id': 1,
                 'lazy': True,
                 'port_hide_changed': set(),
                 'posx': 0,
                 'posy': 0,
                 'priority': 0,
                 'use_user_color': True,
                 'user_application': None,
                 'user_color': None}},
                             elt_value={  2: [(0, '2.1')],
   3: [(0, '1.2')],
   4: [],
   5: [],
   6: [],
   7: [],
   '__in__': [],
   '__out__': []},
                             elt_ad_hoc={  2: {'position': [-245.9709450619092, -111.85872859148041], 'userColor': None, 'useUserColor': False},
   3: {'position': [-320.3252070658707, -111.0109722906813], 'userColor': None, 'useUserColor': False},
   4: {'position': [-314.20270829939903, -34.466726410245506], 'userColor': None, 'useUserColor': False},
   5: {'position': [-364.22435123884213, -140.49860060790175], 'text': 'inputs', 'textColor': None, 'rectP2': (176.7140917324355, 69.32013223357238), 'color': None, 'visualStyle': 1},
   6: {'position': [-381.13154273993564, -60.87669916942594], 'text': 'addition', 'textColor': None, 'rectP2': (-1, -1), 'color': None, 'visualStyle': 1},
   7: {'position': [-311.29505256125043, 14.841906066585054], 'userColor': None, 'useUserColor': False},
   '__in__': {'position': [0, 0], 'userColor': None, 'useUserColor': True},
   '__out__': {'position': [0, 0], 'userColor': None, 'useUserColor': True}},
                             lazy=True,
                             eval_algo='LambdaEvaluation',
                             )




