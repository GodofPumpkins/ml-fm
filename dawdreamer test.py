import dawdreamer as daw
from scipy.io import wavfile
SAMPLE_RATE = 44100
BUFFER_SIZE = 128
DURATION = 5 # in seconds, might reduce later to 3 or 4

engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE) 

SYNTH_PLUGIN = "C:/FYP/vst2 dexed/Dexed.dll"

synth = engine.make_plugin_processor("my_dexed", SYNTH_PLUGIN)
assert synth.get_name() == "my_dexed"

# # write params to text file
# with open('dawdreamer dexed params2.txt', 'w') as f:
# 	f.write(str(synth.get_plugin_parameters_description()))

# print default parameter values
# for i in range(0, 155):
#     print(str(i) + ": " + str(synth.get_parameter(i)))

# select one of the 32 algorithms
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

# Turn Operator 1 into a simple sine wave with no envelope
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
    [44, 1.0], # Operator 1 On/Off switch
])

# Override some of Operator 2 parameters
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
    [58, 0.0], # Operator 2 Env Scaling Param
    [59, 0.0], # Operator 2 Env Scaling Param
    [60, 0.0], # Operator 2 Env Scaling Param
    [61, 0.0], # Operator 2 Env Scaling Param
    [62, 0.0], # Operator 2 Env Scaling Param
    [63, 0.0], # Operator 2 Env Scaling Param
    [64, 0.0], # Operator 2 Mod Sensitivity
    [65, 0.0], # Operator 2 Key Velocity
    [66, 1.0], # Operator 2 On/Off switch
])

# Override operators 3 through 6
default_parameters.extend([[i, 0.0] for i in range(67, 155)])

# synth.open_editor()

for param_set in default_parameters:
    synth.set_parameter(param_set[0], param_set[1])

# synth.open_editor()
NOTE_DURATION = 4
START = 0
synth.add_midi_note(60, 127, START, NOTE_DURATION) # (MIDI note, velocity, start, duration)

# # check number of output channels - should be 2 ie stereo output. As the synth itself has no stereo processing the channels will be identical and we will remove one later
# print("synth num outputs: ", synth.get_num_output_channels())

graph = [
  (synth, []),  # synth takes no inputs, so we give an empty list.
]

engine.load_graph(graph)

engine.render(DURATION)  # Render DURATION seconds of audio.


audio = engine.get_audio()  
wavfile.write('fuck yu.wav', SAMPLE_RATE, audio.transpose())