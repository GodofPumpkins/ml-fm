import dawdreamer as daw
from scipy.io import wavfile
SAMPLE_RATE = 44100
BUFFER_SIZE = 128
DURATION = 5 # in seconds, might reduce later to 3 or 4

engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE) 

SYNTH_PLUGIN = "C:/FYP/vst2 dexed/Dexed.dll"

synth = engine.make_plugin_processor("my_dexed", SYNTH_PLUGIN)
# assert synth.get_name() == "my_dexed"

# # # write params to text file
# # with open('dawdreamer dexed params2.txt', 'w') as f:
# # 	f.write(str(synth.get_plugin_parameters_description()))

# # print default parameter values
# # for i in range(0, 155):
# #     print(str(i) + ": " + str(synth.get_parameter(i)))

# # operator on/off values

# ON = 1.0
# OFF = 0.0

# OP_1_ON = ON
# OP_2_ON = ON
# OP_3_ON = ON
# OP_4_ON = ON
# OP_5_ON = ON
# OP_6_ON = ON

# # select one of the 32 algorithms
# algorithm_number = 1
# alg = (1.0 / 32.0) * float(algorithm_number - 1) + 0.001

# default_parameters = [
#     [0, 1.0], # Filter Cutoff [Fully open]
#     [1, 0.0], # Filter Resonance
#     [2, 1.0], # Output Gain
#     [3, 0.5], # Master Tuning [Center is 0]
#     [4, alg], # Operator configuration
#     [5, 0.0], # Feedback
#     [6, 1.0], # Key Sync Oscillators
#     [7, 0.35353535413742065], # LFO Speed
#     [8, 0.0], # LFO Delay
#     [9, 0.0], # LFO Pitch Modulation Depth
#     [10, 0.0],# LFO Amplitude Modulation Depth
#     [11, 1.0],# LFO Key Sync
#     [12, 0.0],# LFO Waveform
#     [13, 0.5],# Middle C Tuning
#     [14, 0.4285714328289032],# P MODE SENS
#     [15, 1],# PITCH EG RATE 1
#     [16, 1],# PITCH EG RATE 2
#     [17, 1],# PITCH EG RATE 3
#     [18, 1],# PITCH EG RATE 4
#     [19, 0.5050504803657532],# PITCH EG LEVEL 1
#     [20, 0.5050504803657532],# PITCH EG LEVEL 2
#     [21, 0.5050504803657532],# PITCH EG LEVEL 3
#     [22, 0.5050504803657532],# PITCH EG LEVEL 4
# ]

# # Operator 1 Parameters
# default_parameters.extend([
#     [23, 0.9], # Operator 1 Attack Rate
#     [24, 0.9], # Operator 1 Decay Rate
#     [25, 0.9], # Operator 1 Sustain Rate
#     [26, 0.9], # Operator 1 Release Rate
#     [27, 1.0], # Operator 1 Attack Level
#     [28, 1.0], # Operator 1 Decay Level
#     [29, 1.0], # Operator 1 Sustain Level
#     [30, 0.0], # Operator 1 Release Level
#     [31, 1.0], # Operator 1 Gain
#     [32, 0.0], # Operator 1 Mode [1.0 is Fixed Frequency]
#     [33, 0.5], # Operator 1 Coarse Tuning
#     [34, 0.0], # Operator 1 Fine Tuning
#     [35, 0.5], # Operator 1 Detune
#     [36, 0.0], # Operator 1 Env Scaling Param
#     [37, 0.0], # Operator 1 Env Scaling Param
#     [38, 0.0], # Operator 1 Env Scaling Param
#     [39, 0.0], # Operator 1 Env Scaling Param
#     [40, 0.0], # Operator 1 Env Scaling Param
#     [41, 0.0], # Operator 1 Env Scaling Param
#     [42, 0.0], # Operator 1 Mod Sensitivity
#     [43, 0.0], # Operator 1 Key Velocity
#     [44, OP_1_ON], # Operator 1 On/Off switch
# ])

# # Operator 2 parameters
# default_parameters.extend([
#     [45, 0.9], # Operator 2 Attack Rate [No attack on operator 2]
#     [46, 0.0], # Operator 2 Decay Rate 
#     [47, 0.0], # Operator 2 Sustain Rate 
#     [48, 0.0], # Operator 2 Release Rate
#     [49, 1.0], # Operator 2 Attack Level
#     [50, 1.0], # Operator 2 Decay Level
#     [51, 1.0], # Operator 2 Sustain Level
#     [52, 1.0], # Operator 2 Release Level
#     [53, 1.0], # Operator 2 Gain [Operator 2 always outputs]
#     [54, 0.0], # Operator 2 Mode [1.0 is Fixed Frequency]
#     [55, 0.5], # Operater 2 Coarse Tuning
#     [56, 0.0], # Operater 2 Fine Tuning
#     [57, 0.5], # Operater 2 Detune
#     [58, 0.0], # Operator 2 Env Scaling Param
#     [59, 0.0], # Operator 2 Env Scaling Param
#     [60, 0.0], # Operator 2 Env Scaling Param
#     [61, 0.0], # Operator 2 Env Scaling Param
#     [62, 0.0], # Operator 2 Env Scaling Param
#     [63, 0.0], # Operator 2 Env Scaling Param
#     [64, 0.0], # Operator 2 Mod Sensitivity
#     [65, 0.0], # Operator 2 Key Velocity
#     [66, OP_2_ON], # Operator 2 On/Off switch
# ])

# # Operator 3 parameters
# default_parameters.extend([
#     [67, 0.9], # Operator 3 Attack Rate [No attack on operator 2]
#     [68, 0.0], # Operator 3 Decay Rate 
#     [69, 0.0], # Operator 3 Sustain Rate 
#     [70, 0.0], # Operator 3 Release Rate
#     [71, 1.0], # Operator 3 Attack Level
#     [72, 1.0], # Operator 3 Decay Level
#     [73, 1.0], # Operator 3 Sustain Level
#     [74, 1.0], # Operator 3 Release Level
#     [75, 1.0], # Operator 3 Gain [Operator 2 always outputs]
#     [76, 0.0], # Operator 3 Mode [1.0 is Fixed Frequency]
#     [77, 0.5], # Operater 3 Coarse Tuning
#     [78, 0.0], # Operater 3 Fine Tuning
#     [79, 0.5], # Operater 3 Detune
#     [80, 0.0], # Operator 3 Env Scaling Param
#     [81, 0.0], # Operator 3 Env Scaling Param
#     [82, 0.0], # Operator 3 Env Scaling Param
#     [83, 0.0], # Operator 3 Env Scaling Param
#     [84, 0.0], # Operator 3 Env Scaling Param
#     [85, 0.0], # Operator 3 Env Scaling Param
#     [86, 0.0], # Operator 3 Mod Sensitivity
#     [87, 0.0], # Operator 3 Key Velocity
#     [88, OP_3_ON], # Operator 3 On/Off switch
# ])

# # Operator 4 parameters
# default_parameters.extend([
#     [89, 0.9], # Operator 4 Attack Rate [No attack on operator 2]
#     [90, 0.0], # Operator 4 Decay Rate 
#     [91, 0.0], # Operator 4 Sustain Rate 
#     [92, 0.0], # Operator 4 Release Rate
#     [93, 1.0], # Operator 4 Attack Level
#     [94, 1.0], # Operator 4 Decay Level
#     [95, 1.0], # Operator 4 Sustain Level
#     [96, 1.0], # Operator 4 Release Level
#     [97, 1.0], # Operator 4 Gain [Operator 2 always outputs]
#     [98, 0.0], # Operator 4 Mode [1.0 is Fixed Frequency]
#     [99, 0.5], # Operater 4 Coarse Tuning
#     [100, 0.0], # Operater 4 Fine Tuning
#     [101, 0.5], # Operater 4 Detune
#     [102, 0.0], # Operator 4 Env Scaling Param
#     [103, 0.0], # Operator 4 Env Scaling Param
#     [104, 0.0], # Operator 4 Env Scaling Param
#     [105, 0.0], # Operator 4 Env Scaling Param
#     [106, 0.0], # Operator 4 Env Scaling Param
#     [107, 0.0], # Operator 4 Env Scaling Param
#     [108, 0.0], # Operator 4 Mod Sensitivity
#     [109, 0.0], # Operator 4 Key Velocity
#     [110, OP_4_ON], # Operator 4 On/Off switch
# ])

# # Operator 5 parameters
# default_parameters.extend([
#     [111, 0.9], # Operator 5 Attack Rate [No attack on operator 2]
#     [112, 0.0], # Operator 5 Decay Rate 
#     [113, 0.0], # Operator 5 Sustain Rate 
#     [114, 0.0], # Operator 5 Release Rate
#     [115, 1.0], # Operator 5 Attack Level
#     [116, 1.0], # Operator 5 Decay Level
#     [117, 1.0], # Operator 5 Sustain Level
#     [118, 1.0], # Operator 5 Release Level
#     [119, 1.0], # Operator 5 Gain [Operator 2 always outputs]
#     [120, 0.0], # Operator 5 Mode [1.0 is Fixed Frequency]
#     [121, 0.5], # Operater 5 Coarse Tuning
#     [122, 0.0], # Operater 5 Fine Tuning
#     [123, 0.5], # Operater 5 Detune
#     [124, 0.0], # Operator 5 Env Scaling Param
#     [125, 0.0], # Operator 5 Env Scaling Param
#     [126, 0.0], # Operator 5 Env Scaling Param
#     [127, 0.0], # Operator 5 Env Scaling Param
#     [128, 0.0], # Operator 5 Env Scaling Param
#     [129, 0.0], # Operator 5 Env Scaling Param
#     [130, 0.0], # Operator 5 Mod Sensitivity
#     [131, 0.0], # Operator 5 Key Velocity
#     [132, OP_5_ON], # Operator 5 On/Off switch
# ])

# # Operator 6 parameters
# default_parameters.extend([
#     [133, 0.9], # Operator 6 Attack Rate [No attack on operator 2]
#     [134, 0.0], # Operator 6 Decay Rate 
#     [135, 0.0], # Operator 6 Sustain Rate 
#     [136, 0.0], # Operator 6 Release Rate
#     [137, 1.0], # Operator 6 Attack Level
#     [138, 1.0], # Operator 6 Decay Level
#     [139, 1.0], # Operator 6 Sustain Level
#     [140, 1.0], # Operator 6 Release Level
#     [141, 1.0], # Operator 6 Gain [Operator 2 always outputs]
#     [142, 0.0], # Operator 6 Mode [1.0 is Fixed Frequency]
#     [143, 0.5], # Operater 6 Coarse Tuning
#     [144, 0.0], # Operater 6 Fine Tuning
#     [145, 0.5], # Operater 6 Detune
#     [146, 0.0], # Operator 6 Env Scaling Param
#     [147, 0.0], # Operator 6 Env Scaling Param
#     [148, 0.0], # Operator 6 Env Scaling Param
#     [149, 0.0], # Operator 6 Env Scaling Param
#     [150, 0.0], # Operator 6 Env Scaling Param
#     [151, 0.0], # Operator 6 Env Scaling Param
#     [152, 0.0], # Operator 6 Mod Sensitivity
#     [153, 0.0], # Operator 6 Key Velocity
#     [154, OP_6_ON], # Operator 6 On/Off switch
# ])

# # Override operators 3 through 6
# # default_parameters.extend([[i, 0.0] for i in range(67, 155)])

# # synth.open_editor()

# for param_set in default_parameters:
#     synth.set_parameter(param_set[0], param_set[1])

# # synth.open_editor()
# NOTE_DURATION = 4
# START = 0
# synth.add_midi_note(60, 127, START, NOTE_DURATION) # (MIDI note, velocity, start, duration)

# # # check number of output channels - should be 2 ie stereo output. As the synth itself has no stereo processing the channels will be identical and we will remove one later
# # print("synth num outputs: ", synth.get_num_output_channels())

# graph = [
#   (synth, []),  # synth takes no inputs, so we give an empty list.
# ]

# engine.load_graph(graph)

# engine.render(DURATION)  # Render DURATION seconds of audio.


# audio = engine.get_audio()  
# wavfile.write('fuck yu.wav', SAMPLE_RATE, audio.transpose())




ON = 1.0
OFF = 0.0

OP_1_ON = ON
OP_2_ON = ON
OP_3_ON = OFF
OP_4_ON = OFF
OP_5_ON = OFF
OP_6_ON = OFF

engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE) 

synth = engine.make_plugin_processor("my_dexed", SYNTH_PLUGIN)

# making initial state

algorithm_number = 1
alg = (1.0 / 32.0) * float(algorithm_number - 1) + 0.001

default_parameters = [
    [0, 1.0], # Filter Cutoff [Fully open]
    [1, 0.0], # Filter Resonance
    [2, 1.0], # Output Gain
    [3, 0.5], # Master Tuning [Center is 0]
    [4, alg], # Operator configuration
    [5, 0.0], # Feedback
    [6, 1.0], # Key Sync Oscillators
    [7, 0.35353535413742065], # LFO Speed
    [8, 0.0], # LFO Delay
    [9, 0.0], # LFO Pitch Modulation Depth
    [10, 0.0],# LFO Amplitude Modulation Depth
    [11, 1.0],# LFO Key Sync
    [12, 0.0],# LFO Waveform
    [13, 0.5],# Middle C Tuning
    [14, 0.4285714328289032],# P MODE SENS
    [15, 1],# PITCH EG RATE 1
    [16, 1],# PITCH EG RATE 2
    [17, 1],# PITCH EG RATE 3
    [18, 1],# PITCH EG RATE 4
    [19, 0.5050504803657532],# PITCH EG LEVEL 1
    [20, 0.5050504803657532],# PITCH EG LEVEL 2
    [21, 0.5050504803657532],# PITCH EG LEVEL 3
    [22, 0.5050504803657532],# PITCH EG LEVEL 4
]

# Operator 1 Parameters
default_parameters.extend([
    [23, 0.9], # Operator 1 Attack Rate
    [24, 0.9], # Operator 1 Decay Rate
    [25, 0.9], # Operator 1 Sustain Rate
    [26, 0.9], # Operator 1 Release Rate
    [27, 1.0], # Operator 1 Attack Level
    [28, 1.0], # Operator 1 Decay Level
    [29, 1.0], # Operator 1 Sustain Level
    [30, 0.0], # Operator 1 Release Level
    [31, 1.0], # Operator 1 Gain
    [32, 0.0], # Operator 1 Mode [1.0 is Fixed Frequency]
    [33, 0.5], # Operator 1 Coarse Tuning
    [34, 0.0], # Operator 1 Fine Tuning
    [35, 0.5], # Operator 1 Detune
    [36, 0.0], # Operator 1 Env Scaling Param
    [37, 0.0], # Operator 1 Env Scaling Param
    [38, 0.0], # Operator 1 Env Scaling Param
    [39, 0.0], # Operator 1 Env Scaling Param
    [40, 0.0], # Operator 1 Env Scaling Param
    [41, 0.0], # Operator 1 Env Scaling Param
    [42, 0.0], # Operator 1 Mod Sensitivity
    [43, 0.0], # Operator 1 Key Velocity
    [44, OP_1_ON], # Operator 1 On/Off switch
])

# Operator 2 parameters
default_parameters.extend([
    [45, 0.9], # Operator 2 Attack Rate [No attack on operator 2]
    [46, 0.0], # Operator 2 Decay Rate 
    [47, 0.0], # Operator 2 Sustain Rate 
    [48, 0.0], # Operator 2 Release Rate
    [49, 1.0], # Operator 2 Attack Level
    [50, 1.0], # Operator 2 Decay Level
    [51, 1.0], # Operator 2 Sustain Level
    [52, 1.0], # Operator 2 Release Level
    [53, 1.0], # Operator 2 Gain [Operator 2 always outputs]
    [54, 0.0], # Operator 2 Mode [1.0 is Fixed Frequency]
    [55, 0.5], # Operater 2 Coarse Tuning
    [56, 0.0], # Operater 2 Fine Tuning
    [57, 0.5], # Operater 2 Detune
    [58, 0.0], # Operator 2 Env Scaling Param
    [59, 0.0], # Operator 2 Env Scaling Param
    [60, 0.0], # Operator 2 Env Scaling Param
    [61, 0.0], # Operator 2 Env Scaling Param
    [62, 0.0], # Operator 2 Env Scaling Param
    [63, 0.0], # Operator 2 Env Scaling Param
    [64, 0.0], # Operator 2 Mod Sensitivity
    [65, 0.0], # Operator 2 Key Velocity
    [66, OP_2_ON], # Operator 2 On/Off switch
])

# Operator 3 parameters
default_parameters.extend([
    [67, 0.9], # Operator 3 Attack Rate [No attack on operator 2]
    [68, 0.0], # Operator 3 Decay Rate 
    [69, 0.0], # Operator 3 Sustain Rate 
    [70, 0.0], # Operator 3 Release Rate
    [71, 1.0], # Operator 3 Attack Level
    [72, 1.0], # Operator 3 Decay Level
    [73, 1.0], # Operator 3 Sustain Level
    [74, 1.0], # Operator 3 Release Level
    [75, 1.0], # Operator 3 Gain [Operator 2 always outputs]
    [76, 0.0], # Operator 3 Mode [1.0 is Fixed Frequency]
    [77, 0.5], # Operater 3 Coarse Tuning
    [78, 0.0], # Operater 3 Fine Tuning
    [79, 0.5], # Operater 3 Detune
    [80, 0.0], # Operator 3 Env Scaling Param
    [81, 0.0], # Operator 3 Env Scaling Param
    [82, 0.0], # Operator 3 Env Scaling Param
    [83, 0.0], # Operator 3 Env Scaling Param
    [84, 0.0], # Operator 3 Env Scaling Param
    [85, 0.0], # Operator 3 Env Scaling Param
    [86, 0.0], # Operator 3 Mod Sensitivity
    [87, 0.0], # Operator 3 Key Velocity
    [88, OP_3_ON], # Operator 3 On/Off switch
])

# Operator 4 parameters
default_parameters.extend([
    [89, 0.9], # Operator 4 Attack Rate [No attack on operator 2]
    [90, 0.0], # Operator 4 Decay Rate 
    [91, 0.0], # Operator 4 Sustain Rate 
    [92, 0.0], # Operator 4 Release Rate
    [93, 1.0], # Operator 4 Attack Level
    [94, 1.0], # Operator 4 Decay Level
    [95, 1.0], # Operator 4 Sustain Level
    [96, 1.0], # Operator 4 Release Level
    [97, 1.0], # Operator 4 Gain [Operator 2 always outputs]
    [98, 0.0], # Operator 4 Mode [1.0 is Fixed Frequency]
    [99, 0.5], # Operater 4 Coarse Tuning
    [100, 0.0], # Operater 4 Fine Tuning
    [101, 0.5], # Operater 4 Detune
    [102, 0.0], # Operator 4 Env Scaling Param
    [103, 0.0], # Operator 4 Env Scaling Param
    [104, 0.0], # Operator 4 Env Scaling Param
    [105, 0.0], # Operator 4 Env Scaling Param
    [106, 0.0], # Operator 4 Env Scaling Param
    [107, 0.0], # Operator 4 Env Scaling Param
    [108, 0.0], # Operator 4 Mod Sensitivity
    [109, 0.0], # Operator 4 Key Velocity
    [110, OP_4_ON], # Operator 4 On/Off switch
])

# Operator 5 parameters
default_parameters.extend([
    [111, 0.9], # Operator 5 Attack Rate [No attack on operator 2]
    [112, 0.0], # Operator 5 Decay Rate 
    [113, 0.0], # Operator 5 Sustain Rate 
    [114, 0.0], # Operator 5 Release Rate
    [115, 1.0], # Operator 5 Attack Level
    [116, 1.0], # Operator 5 Decay Level
    [117, 1.0], # Operator 5 Sustain Level
    [118, 1.0], # Operator 5 Release Level
    [119, 1.0], # Operator 5 Gain [Operator 2 always outputs]
    [120, 0.0], # Operator 5 Mode [1.0 is Fixed Frequency]
    [121, 0.5], # Operater 5 Coarse Tuning
    [122, 0.0], # Operater 5 Fine Tuning
    [123, 0.5], # Operater 5 Detune
    [124, 0.0], # Operator 5 Env Scaling Param
    [125, 0.0], # Operator 5 Env Scaling Param
    [126, 0.0], # Operator 5 Env Scaling Param
    [127, 0.0], # Operator 5 Env Scaling Param
    [128, 0.0], # Operator 5 Env Scaling Param
    [129, 0.0], # Operator 5 Env Scaling Param
    [130, 0.0], # Operator 5 Mod Sensitivity
    [131, 0.0], # Operator 5 Key Velocity
    [132, OP_5_ON], # Operator 5 On/Off switch
])

# Operator 6 parameters
default_parameters.extend([
    [133, 0.9], # Operator 6 Attack Rate [No attack on operator 2]
    [134, 0.0], # Operator 6 Decay Rate 
    [135, 0.0], # Operator 6 Sustain Rate 
    [136, 0.0], # Operator 6 Release Rate
    [137, 1.0], # Operator 6 Attack Level
    [138, 1.0], # Operator 6 Decay Level
    [139, 1.0], # Operator 6 Sustain Level
    [140, 1.0], # Operator 6 Release Level
    [141, 1.0], # Operator 6 Gain [Operator 2 always outputs]
    [142, 0.0], # Operator 6 Mode [1.0 is Fixed Frequency]
    [143, 0.5], # Operater 6 Coarse Tuning
    [144, 0.0], # Operater 6 Fine Tuning
    [145, 0.5], # Operater 6 Detune
    [146, 0.0], # Operator 6 Env Scaling Param
    [147, 0.0], # Operator 6 Env Scaling Param
    [148, 0.0], # Operator 6 Env Scaling Param
    [149, 0.0], # Operator 6 Env Scaling Param
    [150, 0.0], # Operator 6 Env Scaling Param
    [151, 0.0], # Operator 6 Env Scaling Param
    [152, 0.0], # Operator 6 Mod Sensitivity
    [153, 0.0], # Operator 6 Key Velocity
    [154, OP_6_ON], # Operator 6 On/Off switch
])

# apply parameters to synth
for param_set in default_parameters:
    synth.set_parameter(param_set[0], param_set[1])

# save/load this initial setup to a file
synth.save_state('C:/FYP/ml-fm/init_state')
# synth.load_state('C:/FYP/ml-fm/init_state')

# synth.open_editor()