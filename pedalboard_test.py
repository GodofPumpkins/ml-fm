from pedalboard import Pedalboard, Reverb, load_plugin
from pedalboard.io import AudioFile
from mido import Message # not part of Pedalboard, but convenient!

#initial values: eg level 123 at max, 4 at min
#eg rate all at max
#op1 level at max, rest at 0



# Load a VST3 or Audio Unit plugin from a known path on disk:
instrument = load_plugin("Dexed.vst3")
# instrument.show_editor()
effect = load_plugin("ValhallaSupermassive.vst3")

# print(instrument.parameters)

# for f in instrument.parameters:
#     print(f)


print( instrument.resonance )

# print(instrument.parameters.keys())
# print(effect.parameters.keys())
# with open('dexed parameters.txt', 'w') as f:
#     f.write(str(instrument.parameters))
# dict_keys([
#   'sc_hpf_hz', 'input_lvl_db', 'sensitivity_db',
#   'ratio', 'attack_ms', 'release_ms', 'makeup_db',
#   'mix', 'output_lvl_db', 'sc_active',
#   'full_bandwidth', 'bypass', 'program',
# ])

effect.feedback = 100

# Render some audio by passing MIDI to an instrument:
sample_rate = 44100
audio = instrument(
  [Message("note_on", note=60), Message("note_off", note=60, time=5)],
  duration=5, # seconds
  sample_rate=sample_rate,
)

# Apply effects to this audio:
effected = effect(audio, sample_rate)

# ...or put the effect into a chain with other plugins:
board = Pedalboard([effect, Reverb()])
# ...and run that pedalboard with the same VST instance!
effected = board(audio, sample_rate)


with AudioFile('output.wav', 'w', 44100, 2) as o:
    o.write(effected)