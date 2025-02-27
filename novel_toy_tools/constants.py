#TODO export constants

import numpy as np

#General constants
PI = np.pi

#Viewer 3d constants
VIEWER3D_EULER_ORDER = 'YZX'
VIEWER3D_PERSPECTIVE_VECTOR = np.asarray([0, 1, 0])
VIEWER3D_RENDITION_DIMENTIONS = (800, 600)
#TODO add version here for version of the app
VIEWER3D_OUTPUT_COLUMNS = [
    '3d object',
    ' subject id',
    ' frame number',
    ' exp ID',
    ' age',
    ' camera type',
    ' code',
    ' x', ' y', ' z',
    ' onset',
    ' offset',
    ' raw filename'
]

VIEWER3D_CODES = {
    -1: "Object absent",
    1: "Object in view",
    -2: "Not codable"
}

#Novel Toy object constants
NOVEL_TOYS = [
    'LightBulbStickx2',
    'BowlingTrapWithCookie', 
    'PrickleBallPointy', 
    'FrogMan', 
    'BlockGiraffe', 
    'Phoo', 
    'XmasTreeBallyWhirl', 
    'HoleBlock2QuaterBlocks', 
    'XmasTreeBallyWhirlShorty',
    'XmasTreeBallyWhirl'
]

NOVEL_TOY_EXTENSION = '.obj' # .novel_toy in the future

#Assorted constants
NULL_TOY_FRAME_COUNTS = {novel_toy: 500 for novel_toy in NOVEL_TOYS}
NULL_TOY_FRAME_COUNTS['XmasTreeBallyWhirl'] = 0