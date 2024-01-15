import os
import sys

sys.path.append('..')

BROCKER_ADDRESS = '192.168.0.16'

OBJECT_DETECT_TOPIC = "/object"
ROBOT_STATUS = "/status"

IM_WIDTH = 640
IM_HEIGHT = 480

MODEL_NAME = 'inference_graph'

CWD_PATH = os.getcwd()

PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

PATH_TO_LABELS = os.path.join(CWD_PATH,'data','labelmap.pbtxt')

NUM_CLASSES = 4

CE = 16
DC = 13
RST = 26
SCLK = 5
DIN = 6

CONTRAST = 60

NOKIA_BL = 0

