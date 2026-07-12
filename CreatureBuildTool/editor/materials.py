# CreatureBuildTool/editor/materials.py

from dataclasses import dataclass

@dataclass
class Material:
	name: 				str
	density: 			float
	colour: 			tuple[int,int,int]
	transparent:		bool
		

BONE  			= 	Material(	"Bone", 				1700, 		(	200,	200,	180	), 	False	)
BLOOD 			= 	Material(	"Blood", 				1060, 		(	255,	0,		0	), 	False	)
AIR   			= 	Material(	"Air",					   0, 		(	135, 	206, 	235	), 	 True	)
LIVER   		= 	Material(	"Liver",				1000, 		(	210, 	30, 	80	), 	 False	)
CONNECTIVE   	= 	Material(	"Connective Tissue",	1050, 		(	255, 	200, 	210	), 	 False	)
MUSCLE   		= 	Material(	"Muscle Tissue",		1060, 		(	255, 	0, 		130	), 	 False	)
NERVOUS   		= 	Material(	"Nervous Tissue",		1020, 		(	100, 	30, 	255	), 	 False	)
KERATIN   		= 	Material(	"Keratin",				2100, 		(	200, 	200, 	100	), 	 False	)
SKIN   			= 	Material(	"Skin",					1050, 		(	255, 	255, 	255	), 	 False	)
MELON   		= 	Material(	"Melanin",				1050, 		(	100, 	0, 		100	), 	 False	)

