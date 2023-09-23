from pedalboard import Pedalboard, Reverb, load_plugin
from pedalboard.io import AudioFile
from mido import Message # not part of Pedalboard, but convenient!
import mido
from functions.sysex_unpack import Param

sample_rate = 44100

# Load a VST3 or Audio Unit plugin from a known path on disk:
# print("here")
instrument = load_plugin("DX7 V.vst3")
print("there")

# instrument.show_editor()

# for f in instrument.parameters:
#     print(f + "\n")
    
instrument.show_editor()

with open('dx7 v parameters.txt', 'w') as f:
	f.write(str(instrument.parameters))


# print( instrument.parameters )


# Render some audio by passing MIDI to an instrument:

message = [Message("note_on", note=60, velocity=100), Message("note_off", note=60, time=5)]

num_channels = 2

audio = instrument(
  message,
  duration=5, # seconds
  sample_rate=sample_rate,
  num_channels=num_channels,
)


with AudioFile('dx7 v output.wav', 'w', 44100, num_channels) as o:
	o.write(audio)