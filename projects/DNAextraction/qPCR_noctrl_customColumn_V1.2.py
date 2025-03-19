#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 10:13:25 2021
@author: bwang@mgi-tech.com
Edited on Wed Sep 29 2022
@edited by: cameron.rogers@greenanalyticsllc.com
"""
##init, posi map and shake binding 
#three write methods:empty-None; pcr-"pcr"; kit-"kit" ;cannot grasp/loose-"useless"  shake-([,"shake"])

pos_type_map = {'POS1': 'useless', 'POS2': 'useless', 'POS3': 'useless', 'POS4': 'useless',
                'POS5': 'useless', 'POS6': 'useless', 'POS7': 'useless', 'POS8': 'useless',
                'POS9': None, 'POS10': None, 'POS11': None, 'POS12': None, 
                'POS13': 'PCRBioRadHSP9601', 'POS14': 'PCRBioRadHSP9601', 'POS15': 'PCRBioRadHSP9601', 'POS16': 'PCRBioRadHSP9601',
                'POS17': None, 'POS18': 'PCRBioRadHSP9601', 'POS19':None, 'POS20': [None, 'shake'],
                'POS21': 'DeepwellPlateDT7350504', 'POS22': None, 'POS23': None, 'POS24': 'useless'}
from spredo import *
spx96 = globals().get("Spx96")
init(spx96) #most important
binding_map(pos_type_map)
shake.binding(spx96)

#uploading consumables
def first_feature():
    """
    When loading the script for the first time, read
    Define the wizard indication UI matrix in this function. Each position pos[x] consists of the following fields:
        1. [Optional] Name of plate reagent/consumable. String, such as Deep well plate *This name needs to have a corresponding image file
        2. [Optional] Reagent/Consumable function description. string,
        3, [Optional] Description of reagent/consumable characteristics. String, e.g. 340µl/W.
        4, [Optional] Is there a cover plate. boolean, True or False
        5, [Optional] Whether it needs to be replaced. boolean, True or False
        6, [Optional] Slab name
	*Don't mess up the order. Otherwise identification error
    """
    return [('Pos1', 'TipGEBAF250A', 'New', '250 μL filter tips', False, True, ''),
            ('Pos2', '',  '', '',False, True, ''),
            ('Pos3', 'TipGEBAF250A', 'New', '250 μL filter tips', False, True, ''),
            ('Pos4', 'TipGEBAF250A', 'New', '250 μL filter tips', False, True, ''),
            ('POS5', 'TipGEBAF250A', 'New', '250 μL filter tips',False, True, 'HigherPosition'),
            ('Pos6', '',  '', '',False, True, ''),
            ('Pos7', '',  '', '',False, True, ''),
            ('Pos8', 'TipGEBAF250A', 'New', '250 μL filter tips', False, True, ''),
            ('Pos9', '','', '', False, True, 'PCR'),
            ('Pos10','','', '', False, True, 'PCR'),
            ('Pos11', '',  '', '',False, True, ''),
            ('Pos12', '',  '', '',False, True, ''),
            ('Pos13', 'PCRBioRadHSP9601', 'New Plate', '', False, True, ''),
            ('Pos14', 'PCRBioRadHSP9601', 'New Plate', '', False, True, ''),
            ('Pos15', 'PCRBioRadHSP9601', 'New Plate', '', False, True, ''),
            ('Pos16', 'PCRBioRadHSP9601', 'New Plate', '', False, True, ''),
            ('Pos17', '',  '', '',False, True, ''),
            ('Pos18', 'PCRBioRadHSP9601', 'Sample Plate', '', False, True, 'MagRack'),
            ('Pos19', '', '', '', False, True, 'MagRack'),
            ('Pos20', '', '',  '', False, True, 'Shaker'),
            ('Pos21', 'DeepwellPlateDT7350504', 'Master premix', 'MM in Col 1, 3, 5, 7: 200 ul/well', False, True, 'Temp_Module'),
            ('Pos22', '', '', '', False, True, ''),
            ('Pos23', '', '', '', False, True, ''),
            ('Pos24', '', '', '', False, True, 'Waste Bin')
    ]

first_feature()

home()

report(phase = 'qPCR setup', step = 'Turn on TC')
def blockOn(): 
   temp_a(6)	#6C
tb = parallel_block(blockOn)

# user select number of assays plate
results=require2({'Number of assay plates':[1,2,3,4]},{'':''})
plateNum=int(results[0][0])
mmCol=1 # master mix starts at Col1

if plateNum == 1:
    assayPlates=["POS13"]
    SecondPOS=[
        ('Pos1', 'TipGEBAF250A', 'New', '250 μL filter tips', False, True, ''),
        ('Pos2', '',  '', '',False, True, ''),
        ('Pos3', '',  '', '',False, True, ''),
        ('Pos4', '',  '', '',False, True, ''),
        ('POS5', 'TipGEBAF250A', 'New', '250 μL filter tips',False, True, 'HigherPosition'),
        ('Pos6', '',  '', '',False, True, ''),
        ('Pos7', '',  '', '',False, True, ''),
        ('Pos8', '',  '', '',False, True, ''),
        ('Pos9', '','', '', False, True, 'PCR'),
        ('Pos10','','', '', False, True, 'PCR'),
        ('Pos11', '',  '', '',False, True, ''),
        ('Pos12', '',  '', '',False, True, ''),
        ('Pos13', 'PCRBioRadHSP9601', 'New Plate', '', False, True, ''),
        ('Pos14', '',  '', '',False, True, ''),
        ('Pos15', '',  '', '',False, True, ''),
        ('Pos16', '',  '', '',False, True, ''),
        ('Pos17', '',  '', '',False, True, ''),
        ('Pos18', 'PCRBioRadHSP9601', 'Sample Plate', '', False, True, 'MagRack'),
        ('Pos19', '', '', '', False, True, 'MagRack'),
        ('Pos20', '', '',  '', False, True, 'Shaker'),
        ('Pos21', 'DeepwellPlateDT7350504', 'Master premix', 'MM in Col 1: 200 ul/well', False, True, 'Temp_Module'),
        ('Pos22', '', '', '', False, True, ''),
        ('Pos23', '', '', '', False, True, ''),
        ('Pos24', '', '', '', False, True, 'Waste Bin')
    ]
    update_feature(SecondPOS)
    dialog('Please put PCR plate on POS13 and remove tips from G12 and H12 on POS1.')
elif plateNum == 2:
    assayPlates=["POS13","POS14"]
    SecondPOS=[
        ('Pos1', 'TipGEBAF250A', 'New', '250 μL filter tips', False, True, ''),
        ('Pos2', '',  '', '',False, True, ''),
        ('Pos3', 'TipGEBAF250A', 'New', '250 μL filter tips', False, True, ''),
        ('Pos4', '',  '', '',False, True, ''),
        ('POS5', 'TipGEBAF250A', 'New', '250 μL filter tips',False, True, 'HigherPosition'),
        ('Pos6', '',  '', '',False, True, ''),
        ('Pos7', '',  '', '',False, True, ''),
        ('Pos8', '',  '', '',False, True, ''),
        ('Pos9', '','', '', False, True, 'PCR'),
        ('Pos10','','', '', False, True, 'PCR'),
        ('Pos11', '',  '', '',False, True, ''),
        ('Pos12', '',  '', '',False, True, ''),
        ('Pos13', 'PCRBioRadHSP9601', 'New Plate', '', False, True, ''),
        ('Pos14', 'PCRBioRadHSP9601', 'New Plate', '', False, True, ''),
        ('Pos15', '',  '', '',False, True, ''),
        ('Pos16', '',  '', '',False, True, ''),
        ('Pos17', '',  '', '',False, True, ''),
        ('Pos18', 'PCRBioRadHSP9601', 'Sample Plate', '', False, True, 'MagRack'),
        ('Pos19', '', '', '', False, True, 'MagRack'),
        ('Pos20', '', '',  '', False, True, 'Shaker'),
        ('Pos21', 'DeepwellPlateDT7350504', 'Master premix', 'MM in Col 1, 3: 200 ul/well', False, True, 'Temp_Module'),
        ('Pos22', '', '', '', False, True, ''),
        ('Pos23', '', '', '', False, True, ''),
        ('Pos24', '', '', '', False, True, 'Waste Bin')
    ]
    update_feature(SecondPOS)
    dialog('Please put PCR plate on POS13, POS14 and remove tips from G12 and H12 on POS1, POS3.')
elif plateNum == 3:
    assayPlates=["POS13","POS14","POS15"]
    SecondPOS=[
        ('Pos1', 'TipGEBAF250A', 'New', '250 μL filter tips', False, True, ''),
        ('Pos2', '',  '', '',False, True, ''),
        ('Pos3', 'TipGEBAF250A', 'New', '250 μL filter tips', False, True, ''),
        ('Pos4', 'TipGEBAF250A', 'New', '250 μL filter tips', False, True, ''),
        ('POS5', 'TipGEBAF250A', 'New', '250 μL filter tips',False, True, 'HigherPosition'),
        ('Pos6', '',  '', '',False, True, ''),
        ('Pos7', '',  '', '',False, True, ''),
        ('Pos8', '',  '', '',False, True, ''),
        ('Pos9', '','', '', False, True, 'PCR'),
        ('Pos10','','', '', False, True, 'PCR'),
        ('Pos11', '',  '', '',False, True, ''),
        ('Pos12', '',  '', '',False, True, ''),
        ('Pos13', 'PCRBioRadHSP9601', 'New Plate', '', False, True, ''),
        ('Pos14', 'PCRBioRadHSP9601', 'New Plate', '', False, True, ''),
        ('Pos15', 'PCRBioRadHSP9601', 'New Plate', '', False, True, ''),
        ('Pos16', '',  '', '',False, True, ''),
        ('Pos17', '',  '', '',False, True, ''),
        ('Pos18', 'PCRBioRadHSP9601', 'Sample Plate', '', False, True, 'MagRack'),
        ('Pos19', '', '', '', False, True, 'MagRack'),
        ('Pos20', '', '',  '', False, True, 'Shaker'),
        ('Pos21', 'DeepwellPlateDT7350504', 'Master premix', 'MM in Col 1, 3, 5: 200 ul/well', False, True, 'Temp_Module'),
        ('Pos22', '', '', '', False, True, ''),
        ('Pos23', '', '', '', False, True, ''),
        ('Pos24', '', '', '', False, True, 'Waste Bin')
    ]
    update_feature(SecondPOS)
    dialog('Please put PCR plate on POS13, POS14, POS15 and remove tips from G12 and H12 on POS1, POS3, POS4.')
elif plateNum == 4:
    assayPlates=["POS13","POS14","POS15","POS16"]
    dialog('Please put PCR plate on POS13, POS14, POS15, POS16 and remove tips from G12 and H12 on POS1, POS3, POS4, POS8.')
else:
    dialog('Number of assays must be 1 to 4.')

# transfer master mix 
report(phase = 'Distribute PCR Mix', step = 'Aliquot')

RecVolu = 13.75
TipsCou=1
for x in range(plateNum):
    load_tips({'Module':'POS5','Col': TipsCou, 'Row':1,'Tips':8})
    aspirate({'Module':'POS21','Col': mmCol+2*x, 'Row':1,'BottomOffsetOfZ':0.4,'AspirateVolume': ((RecVolu+2)*6), 'PreAirVolume': (5),'PostAirVolume': (0), 'AspirateRateOfP':20,'DelySeconds':1,'Tips':8})
    dispense({'Module' : 'POS21', 'Col': mmCol+2*x, 'Row': 1,'BottomOffsetOfZ':3, 'DispenseVolume': (2),'DispenseRateOfP':20,'DelySeconds':0.5,'Tips':8})
    for y in range(6):
        dispense({'Module' : assayPlates[x], 'Col': y+1, 'Row': 1,'BottomOffsetOfZ':2, 'DispenseVolume': (RecVolu),'DispenseRateOfP':20,'DelySeconds':2,'Tips':8})
    
    empty({'Module':'POS21','Col': mmCol+2*x, 'Row':1, 'BottomOffsetOfZ': 3, 'DispenseRateOfP': 15, 'DelySeconds': 0.5, 'Tips': 8})
    
    aspirate({'Module':'POS21','Col': mmCol+2*x, 'Row':1,'BottomOffsetOfZ':0.4,'AspirateVolume': ((RecVolu+2)*5), 'PreAirVolume': (0),'PostAirVolume': (0), 'AspirateRateOfP':20,'DelySeconds':1,'Tips':8})
    dispense({'Module' : 'POS21', 'Col': mmCol+2*x, 'Row': 1,'BottomOffsetOfZ':3, 'DispenseVolume': (2),'DispenseRateOfP':20,'DelySeconds':0.5,'Tips':8})
    for z in range(5):
        dispense({'Module' : assayPlates[x], 'Col': z+7, 'Row': 1,'BottomOffsetOfZ':2, 'DispenseVolume': (RecVolu),'DispenseRateOfP':20,'DelySeconds':2,'Tips':8})

    empty({'Module':'POS21','Col': mmCol+2*x, 'Row':1, 'BottomOffsetOfZ': 3, 'DispenseRateOfP': 15, 'DelySeconds': 0.5, 'Tips': 8})

    unload_tips({'Module' : 'POS24', 'Col': 6, 'Row':1, 'Tips':8})
    TipsCou += 1
    
# user select number of Rows in final column
resultsA=require2({'Final Column Number Rows? Please select 0 if no custom column is required :)':[0,1,2,3,4,5,6,7,8]},{'':''})
rowNum=int(resultsA[0][0])

if rowNum == 1:
    load_tips({'Module':'POS5','Col': TipsCou, 'Row':8,'Tips':8})
    aspirate({'Module':'POS21','Col': mmCol+2*x, 'Row':1,'BottomOffsetOfZ':0.4,'AspirateVolume': ((RecVolu+2)*1), 'PreAirVolume': (0),'PostAirVolume': (0), 'AspirateRateOfP':20,'DelySeconds':1,'Tips':8})
    dispense({'Module' : 'POS21', 'Col': mmCol+2*x, 'Row': 1,'BottomOffsetOfZ':3, 'DispenseVolume': (2),'DispenseRateOfP':20,'DelySeconds':0.5,'Tips':8})
    for z in range(1):
	dispense({'Module' : assayPlates[x], 'Col': z+12, 'Row': 1,'BottomOffsetOfZ':2, 'DispenseVolume': (RecVolu),'DispenseRateOfP':20,'DelySeconds':2,'Tips':8})

    empty({'Module':'POS21','Col': mmCol+2*x, 'Row':1, 'BottomOffsetOfZ': 3, 'DispenseRateOfP': 15, 'DelySeconds': 0.5, 'Tips': 8})

    unload_tips({'Module' : 'POS24', 'Col': 6, 'Row':1, 'Tips':8})
    TipsCou += 1
elif rowNum == 2:
    load_tips({'Module':'POS5','Col': TipsCou, 'Row':7,'Tips':8})
    aspirate({'Module':'POS21','Col': mmCol+2*x, 'Row':1,'BottomOffsetOfZ':0.4,'AspirateVolume': ((RecVolu+2)*1), 'PreAirVolume': (0),'PostAirVolume': (0), 'AspirateRateOfP':20,'DelySeconds':1,'Tips':8})
    dispense({'Module' : 'POS21', 'Col': mmCol+2*x, 'Row': 1,'BottomOffsetOfZ':3, 'DispenseVolume': (2),'DispenseRateOfP':20,'DelySeconds':0.5,'Tips':8})
    for z in range(1):
	dispense({'Module' : assayPlates[x], 'Col': z+12, 'Row': 1,'BottomOffsetOfZ':2, 'DispenseVolume': (RecVolu),'DispenseRateOfP':20,'DelySeconds':2,'Tips':8})

    empty({'Module':'POS21','Col': mmCol+2*x, 'Row':1, 'BottomOffsetOfZ': 3, 'DispenseRateOfP': 15, 'DelySeconds': 0.5, 'Tips': 8})

    unload_tips({'Module' : 'POS24', 'Col': 6, 'Row':1, 'Tips':8})
    TipsCou += 1
elif rowNum == 3:
    load_tips({'Module':'POS5','Col': TipsCou, 'Row':6,'Tips':8})
    aspirate({'Module':'POS21','Col': mmCol+2*x, 'Row':1,'BottomOffsetOfZ':0.4,'AspirateVolume': ((RecVolu+2)*1), 'PreAirVolume': (0),'PostAirVolume': (0), 'AspirateRateOfP':20,'DelySeconds':1,'Tips':8})
    dispense({'Module' : 'POS21', 'Col': mmCol+2*x, 'Row': 1,'BottomOffsetOfZ':3, 'DispenseVolume': (2),'DispenseRateOfP':20,'DelySeconds':0.5,'Tips':8})
    for z in range(1):
	dispense({'Module' : assayPlates[x], 'Col': z+12, 'Row': 1,'BottomOffsetOfZ':2, 'DispenseVolume': (RecVolu),'DispenseRateOfP':20,'DelySeconds':2,'Tips':8})

    empty({'Module':'POS21','Col': mmCol+2*x, 'Row':1, 'BottomOffsetOfZ': 3, 'DispenseRateOfP': 15, 'DelySeconds': 0.5, 'Tips': 8})

    unload_tips({'Module' : 'POS24', 'Col': 6, 'Row':1, 'Tips':8})
    TipsCou += 1
elif rowNum == 4:
    load_tips({'Module':'POS5','Col': TipsCou, 'Row':5,'Tips':8})
    aspirate({'Module':'POS21','Col': mmCol+2*x, 'Row':1,'BottomOffsetOfZ':0.4,'AspirateVolume': ((RecVolu+2)*1), 'PreAirVolume': (0),'PostAirVolume': (0), 'AspirateRateOfP':20,'DelySeconds':1,'Tips':8})
    dispense({'Module' : 'POS21', 'Col': mmCol+2*x, 'Row': 1,'BottomOffsetOfZ':3, 'DispenseVolume': (2),'DispenseRateOfP':20,'DelySeconds':0.5,'Tips':8})
    for z in range(1):
	dispense({'Module' : assayPlates[x], 'Col': z+12, 'Row': 1,'BottomOffsetOfZ':2, 'DispenseVolume': (RecVolu),'DispenseRateOfP':20,'DelySeconds':2,'Tips':8})

    empty({'Module':'POS21','Col': mmCol+2*x, 'Row':1, 'BottomOffsetOfZ': 3, 'DispenseRateOfP': 15, 'DelySeconds': 0.5, 'Tips': 8})

    unload_tips({'Module' : 'POS24', 'Col': 6, 'Row':1, 'Tips':8})
    TipsCou += 1
elif rowNum == 5:
    load_tips({'Module':'POS5','Col': TipsCou, 'Row':4,'Tips':8})
    aspirate({'Module':'POS21','Col': mmCol+2*x, 'Row':1,'BottomOffsetOfZ':0.4,'AspirateVolume': ((RecVolu+2)*1), 'PreAirVolume': (0),'PostAirVolume': (0), 'AspirateRateOfP':20,'DelySeconds':1,'Tips':8})
    dispense({'Module' : 'POS21', 'Col': mmCol+2*x, 'Row': 1,'BottomOffsetOfZ':3, 'DispenseVolume': (2),'DispenseRateOfP':20,'DelySeconds':0.5,'Tips':8})
    for z in range(1):
	dispense({'Module' : assayPlates[x], 'Col': z+12, 'Row': 1,'BottomOffsetOfZ':2, 'DispenseVolume': (RecVolu),'DispenseRateOfP':20,'DelySeconds':2,'Tips':8})

    empty({'Module':'POS21','Col': mmCol+2*x, 'Row':1, 'BottomOffsetOfZ': 3, 'DispenseRateOfP': 15, 'DelySeconds': 0.5, 'Tips': 8})

    unload_tips({'Module' : 'POS24', 'Col': 6, 'Row':1, 'Tips':8})
    TipsCou += 1
elif rowNum == 6:
    load_tips({'Module':'POS5','Col': TipsCou, 'Row':3,'Tips':8})
    aspirate({'Module':'POS21','Col': mmCol+2*x, 'Row':1,'BottomOffsetOfZ':0.4,'AspirateVolume': ((RecVolu+2)*1), 'PreAirVolume': (0),'PostAirVolume': (0), 'AspirateRateOfP':20,'DelySeconds':1,'Tips':8})
    dispense({'Module' : 'POS21', 'Col': mmCol+2*x, 'Row': 1,'BottomOffsetOfZ':3, 'DispenseVolume': (2),'DispenseRateOfP':20,'DelySeconds':0.5,'Tips':8})
    for z in range(1):
	dispense({'Module' : assayPlates[x], 'Col': z+12, 'Row': 1,'BottomOffsetOfZ':2, 'DispenseVolume': (RecVolu),'DispenseRateOfP':20,'DelySeconds':2,'Tips':8})

    empty({'Module':'POS21','Col': mmCol+2*x, 'Row':1, 'BottomOffsetOfZ': 3, 'DispenseRateOfP': 15, 'DelySeconds': 0.5, 'Tips': 8})

    unload_tips({'Module' : 'POS24', 'Col': 6, 'Row':1, 'Tips':8})
    TipsCou += 1
elif rowNum == 7:
    load_tips({'Module':'POS5','Col': TipsCou, 'Row':2,'Tips':8})
    aspirate({'Module':'POS21','Col': mmCol+2*x, 'Row':1,'BottomOffsetOfZ':0.4,'AspirateVolume': ((RecVolu+2)*1), 'PreAirVolume': (0),'PostAirVolume': (0), 'AspirateRateOfP':20,'DelySeconds':1,'Tips':8})
    dispense({'Module' : 'POS21', 'Col': mmCol+2*x, 'Row': 1,'BottomOffsetOfZ':3, 'DispenseVolume': (2),'DispenseRateOfP':20,'DelySeconds':0.5,'Tips':8})
    for z in range(1):
	dispense({'Module' : assayPlates[x], 'Col': z+12, 'Row': 1,'BottomOffsetOfZ':2, 'DispenseVolume': (RecVolu),'DispenseRateOfP':20,'DelySeconds':2,'Tips':8})

    empty({'Module':'POS21','Col': mmCol+2*x, 'Row':1, 'BottomOffsetOfZ': 3, 'DispenseRateOfP': 15, 'DelySeconds': 0.5, 'Tips': 8})

    unload_tips({'Module' : 'POS24', 'Col': 6, 'Row':1, 'Tips':8})
    TipsCou += 1
elif rowNum == 8:
    load_tips({'Module':'POS5','Col': TipsCou, 'Row':1,'Tips':8})
    aspirate({'Module':'POS21','Col': mmCol+2*x, 'Row':1,'BottomOffsetOfZ':0.4,'AspirateVolume': ((RecVolu+2)*1), 'PreAirVolume': (0),'PostAirVolume': (0), 'AspirateRateOfP':20,'DelySeconds':1,'Tips':8})
    dispense({'Module' : 'POS21', 'Col': mmCol+2*x, 'Row': 1,'BottomOffsetOfZ':3, 'DispenseVolume': (2),'DispenseRateOfP':20,'DelySeconds':0.5,'Tips':8})
    for z in range(1):
	dispense({'Module' : assayPlates[x], 'Col': z+12, 'Row': 1,'BottomOffsetOfZ':2, 'DispenseVolume': (RecVolu),'DispenseRateOfP':20,'DelySeconds':2,'Tips':8})

    empty({'Module':'POS21','Col': mmCol+2*x, 'Row':1, 'BottomOffsetOfZ': 3, 'DispenseRateOfP': 15, 'DelySeconds': 0.5, 'Tips': 8})

    unload_tips({'Module' : 'POS24', 'Col': 6, 'Row':1, 'Tips':8})
    TipsCou += 1

elif rowNum == 0:
	#add sample templates
	report(phase = 'qPCR Setup', step = 'Add Samples')

	SampVol = 5
	RecVolu = 5+RecVolu
	DeepMix = 5

	TipsPos=["POS1","POS3","POS4","POS8"]

	for x in range(plateNum):
    		load_tips({'Module':TipsPos[x],'Well':'1A','Tips':96}) 
    		aspirate({'Module':'POS18','Col': 1, 'Row':1,'BottomOffsetOfZ':0,'AspirateVolume': (SampVol+3), 'PreAirVolume': (5),'PostAirVolume': (0), 'AspirateRateOfP':50,'DelySeconds':1,'Tips':96})
    		dispense({'Module' : assayPlates[x], 'Col': 1, 'Row':1,'BottomOffsetOfZ':2,'DispenseRateOfP':10, 'DispenseVolume': (SampVol+3),'DelySeconds':1,'Tips':96})
    		mix({'Module':assayPlates[x], 'Col': 1, 'Row':1, 'SubMixLoopCounts':DeepMix, 'BottomOffsetOfZ':0.1, 'MixOffsetOfZInLoop':1.5, 'MixOffsetOfZAfterLoop':3,
    		'MixLoopVolume': (9), 'PreAirVolume':(0), 'DispenseVolumeAfterSubmixLoop':(0),
    		'MixLoopAspirateRate':20, 'MixLoopDispenseRate':20, 'DispenseRateAfterSubmixLoop':10,
    		'SubMixLoopCompletedDely':1, "SecondRouteRate": 38, 'Tips':96, 'TipTouchOffsetOfX':1, 'TipTouchHeight':10})
    		unload_tips({'Module' : TipsPos[x], 'Well':'1A','SafePointOfZ':15})

report(phase = 'qPCR setup', step = 'Turn off TC')

def blockOff():
   temp_sleep_a()
tbOFF = parallel_block(blockOff)

dialog('Workflow completed. Please add controls manually.')

home()

