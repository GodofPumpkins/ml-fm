from pedalboard import Pedalboard, Reverb, load_plugin
from pedalboard.io import AudioFile
from mido import Message # not part of Pedalboard, but convenient!
import mido
from functions.sysex_unpack import Param

#initial values: eg level 123 at max, 4 at min
#eg rate all at max
#op1 level at max, rest at 0

sample_rate = 44100

# Load a VST3 or Audio Unit plugin from a known path on disk:
# instrument = load_plugin("Dexed.vst3")
instrument = load_plugin("Dexed.so")
# print(instrument.cutoff)
# instrument.show_editor()
# effect = load_plugin("ValhallaSupermassive.vst3")
paramDict = {
	"cutoff": Param("Cutoff", 1, 0, 1, 0.001),
	"resonance": Param("Resonance", 0, 0, 1, 0.001),
	"output": Param("Output", 1, 0, 1, 0.001),
	"master_tune_adj": Param("MASTER TUNE ADJ", 0.5, -1.0, 0.999878, 0.001996015),
	"algorithm": Param("ALGORITHM", 1, 1.0, 32.0, 1.0),
	"feedback": Param("FEEDBACK", 0, 0.0, 7.0, 1.0),
	"osc_key_sync": Param("OSC KEY SYNC", True, False, True),
	"lfo_speed": Param("LFO SPEED", 0.353535, 0.0, 99.0, 1.0),
	"lfo_delay": Param("LFO DELAY", 0, 0.0, 99.0, 1.0),
	"lfo_pm_depth": Param("LFO PM DEPTH", 0, 0.0, 99.0, 1.0),
	"lfo_am_depth": Param("LFO AM DEPTH", 0, 0.0, 1.0, 0.001),
	"lfo_key_sync": Param("LFO KEY SYNC", 1, 0.0, 1.0, 0.001),
	"lfo_wave": Param("LFO WAVE", 0, 0.0, 1.0, 0.001),
	"transpose": Param("TRANSPOSE", 0.5, 0.0, 1.0, 0.001),
	"p_mode_sens": Param("P MODE SENS.", 0.428571, 0.0, 1.0, 0.001),
	"pitch_eg_rate_1": Param("PITCH EG RATE 1", 1, 0.0, 1.0, 0.001),
	"pitch_eg_rate_2": Param("PITCH EG RATE 2", 1, 0.0, 1.0, 0.001),
	"pitch_eg_rate_3": Param("PITCH EG RATE 3", 1, 0.0, 1.0, 0.001),
	"pitch_eg_rate_4": Param("PITCH EG RATE 4", 1, 0.0, 1.0, 0.001),
	"pitch_eg_level_1": Param("PITCH EG LEVEL 1", 0.50505, 0.0, 1.0, 0.001),
	"pitch_eg_level_2": Param("PITCH EG LEVEL 2", 0.50505, 0.0, 1.0, 0.001),
	"pitch_eg_level_3": Param("PITCH EG LEVEL 3", 0.50505, 0.0, 1.0, 0.001),
	"pitch_eg_level_4": Param("PITCH EG LEVEL 4", 0.50505, 0.0, 1.0, 0.001),
	"op1_eg_rate_1": Param("OP1 EG RATE 1", 1, 0.0, 1.0, 0.001),
	"op1_eg_rate_2": Param("OP1 EG RATE 2", 1, 0.0, 1.0, 0.001),
	"op1_eg_rate_3": Param("OP1 EG RATE 3", 1, 0.0, 1.0, 0.001),
	"op1_eg_rate_4": Param("OP1 EG RATE 4", 1, 0.0, 1.0, 0.001),
	"op1_eg_level_1": Param("OP1 EG LEVEL 1", 1, 0.0, 1.0, 0.001),
	"op1_eg_level_2": Param("OP1 EG LEVEL 2", 1, 0.0, 1.0, 0.001),
	"op1_eg_level_3": Param("OP1 EG LEVEL 3", 1, 0.0, 1.0, 0.001),
	"op1_eg_level_4": Param("OP1 EG LEVEL 4", 0, 0.0, 1.0, 0.001),
	"op1_output_level": Param("OP1 OUTPUT LEVEL", 1, 0.0, 1.0, 0.001),
	"op1_mode": Param("OP1 MODE", 0, 0.0, 1.0, 0.001),
	"op1_f_coarse": Param("OP1 F COARSE", 0.0322581, 0.0, 1.0, 0.001),
	"op1_f_fine": Param("OP1 F FINE", 0, 0.0, 1.0, 0.001),
	"op1_osc_detune": Param("OP1 OSC DETUNE", 0.5, 0.0, 1.0, 0.001),
	"op1_break_point": Param("OP1 BREAK POINT", 0, 0.0, 1.0, 0.001),
	"op1_l_scale_depth": Param("OP1 L SCALE DEPTH", 0, 0.0, 1.0, 0.001),
	"op1_r_scale_depth": Param("OP1 R SCALE DEPTH", 0, 0.0, 1.0, 0.001),
	"op1_l_key_scale": Param("OP1 L KEY SCALE", 0, 0.0, 1.0, 0.001),
	"op1_r_key_scale": Param("OP1 R KEY SCALE", 0, 0.0, 1.0, 0.001),
	"op1_rate_scaling": Param("OP1 RATE SCALING", 0, 0.0, 1.0, 0.001),
	"op1_a_mod_sens": Param("OP1 A MOD SENS.", 0, 0.0, 1.0, 0.001),
	"op1_key_velocity": Param("OP1 KEY VELOCITY", 0, 0.0, 1.0, 0.001),
	"op1_switch": Param("OP1 SWITCH", 1, 0.0, 1.0, 0.001),
	"op2_eg_rate_1": Param("OP2 EG RATE 1", 1, 0.0, 1.0, 0.001),
	"op2_eg_rate_2": Param("OP2 EG RATE 2", 1, 0.0, 1.0, 0.001),
	"op2_eg_rate_3": Param("OP2 EG RATE 3", 1, 0.0, 1.0, 0.001),
	"op2_eg_rate_4": Param("OP2 EG RATE 4", 1, 0.0, 1.0, 0.001),
	"op2_eg_level_1": Param("OP2 EG LEVEL 1", 1, 0.0, 1.0, 0.001),
	"op2_eg_level_2": Param("OP2 EG LEVEL 2", 1, 0.0, 1.0, 0.001),
	"op2_eg_level_3": Param("OP2 EG LEVEL 3", 1, 0.0, 1.0, 0.001),
	"op2_eg_level_4": Param("OP2 EG LEVEL 4", 0, 0.0, 1.0, 0.001),
	"op2_output_level": Param("OP2 OUTPUT LEVEL", 1, 0.0, 1.0, 0.001),
	"op2_mode": Param("OP2 MODE", 0, 0.0, 1.0, 0.001),
	"op2_f_coarse": Param("OP2 F COARSE", 0, 0.0, 1.0, 0.001),
	"op2_f_fine": Param("OP2 F FINE", 0, 0.0, 1.0, 0.001),
	"op2_osc_detune": Param("OP2 OSC DETUNE", 0.5, 0.0, 1.0, 0.001),
	"op2_break_point": Param("OP2 BREAK POINT", 0, 0.0, 1.0, 0.001),
	"op2_l_scale_depth": Param("OP2 L SCALE DEPTH", 0, 0.0, 1.0, 0.001),
	"op2_r_scale_depth": Param("OP2 R SCALE DEPTH", 0, 0.0, 1.0, 0.001),
	"op2_l_key_scale": Param("OP2 L KEY SCALE", 0, 0.0, 1.0, 0.001),
	"op2_r_key_scale": Param("OP2 R KEY SCALE", 0, 0.0, 1.0, 0.001),
	"op2_rate_scaling": Param("OP2 RATE SCALING", 0, 0.0, 1.0, 0.001),
	"op2_a_mod_sens": Param("OP2 A MOD SENS.", 0, 0.0, 1.0, 0.001),
	"op2_key_velocity": Param("OP2 KEY VELOCITY", 0, 0.0, 1.0, 0.001),
	"op2_switch": Param("OP2 SWITCH", 1, 0.0, 1.0, 0.001),
	"op3_eg_rate_1": Param("OP3 EG RATE 1", 0.151515, 0.0, 1.0, 0.001),
	"op3_eg_rate_2": Param("OP3 EG RATE 2", 0.646465, 0.0, 1.0, 0.001),
	"op3_eg_rate_3": Param("OP3 EG RATE 3", 0.494949, 0.0, 1.0, 0.001),
	"op3_eg_rate_4": Param("OP3 EG RATE 4", 1, 0.0, 1.0, 0.001),
	"op3_eg_level_1": Param("OP3 EG LEVEL 1", 0.444444, 0.0, 1.0, 0.001),
	"op3_eg_level_2": Param("OP3 EG LEVEL 2", 1, 0.0, 1.0, 0.001),
	"op3_eg_level_3": Param("OP3 EG LEVEL 3", 0, 0.0, 1.0, 0.001),
	"op3_eg_level_4": Param("OP3 EG LEVEL 4", 0, 0.0, 1.0, 0.001),
	"op3_output_level": Param("OP3 OUTPUT LEVEL", 1, 0.0, 1.0, 0.001),
	"op3_mode": Param("OP3 MODE", 0, 0.0, 1.0, 0.001),
	"op3_f_coarse": Param("OP3 F COARSE", 0.0645161, 0.0, 1.0, 0.001),
	"op3_f_fine": Param("OP3 F FINE", 0, 0.0, 1.0, 0.001),
	"op3_osc_detune": Param("OP3 OSC DETUNE", 0.5, 0.0, 1.0, 0.001),
	"op3_break_point": Param("OP3 BREAK POINT", 0, 0.0, 1.0, 0.001),
	"op3_l_scale_depth": Param("OP3 L SCALE DEPTH", 0, 0.0, 1.0, 0.001),
	"op3_r_scale_depth": Param("OP3 R SCALE DEPTH", 0, 0.0, 1.0, 0.001),
	"op3_l_key_scale": Param("OP3 L KEY SCALE", 0, 0.0, 1.0, 0.001),
	"op3_r_key_scale": Param("OP3 R KEY SCALE", 0, 0.0, 1.0, 0.001),
	"op3_rate_scaling": Param("OP3 RATE SCALING", 0, 0.0, 1.0, 0.001),
	"op3_a_mod_sens": Param("OP3 A MOD SENS.", 0, 0.0, 1.0, 0.001),
	"op3_key_velocity": Param("OP3 KEY VELOCITY", 0, 0.0, 1.0, 0.001),
	"op3_switch": Param("OP3 SWITCH", 1, 0.0, 1.0, 0.001),
	"op4_eg_rate_1": Param("OP4 EG RATE 1", 0.131313, 0.0, 1.0, 0.001),
	"op4_eg_rate_2": Param("OP4 EG RATE 2", 0.646465, 0.0, 1.0, 0.001),
	"op4_eg_rate_3": Param("OP4 EG RATE 3", 0.494949, 0.0, 1.0, 0.001),
	"op4_eg_rate_4": Param("OP4 EG RATE 4", 1, 0.0, 1.0, 0.001),
	"op4_eg_level_1": Param("OP4 EG LEVEL 1", 0.464646, 0.0, 1.0, 0.001),
	"op4_eg_level_2": Param("OP4 EG LEVEL 2", 1, 0.0, 1.0, 0.001),
	"op4_eg_level_3": Param("OP4 EG LEVEL 3", 0, 0.0, 1.0, 0.001),
	"op4_eg_level_4": Param("OP4 EG LEVEL 4", 0, 0.0, 1.0, 0.001),
	"op4_output_level": Param("OP4 OUTPUT LEVEL", 1, 0.0, 1.0, 0.001),
	"op4_mode": Param("OP4 MODE", 0, 0.0, 1.0, 0.001),
	"op4_f_coarse": Param("OP4 F COARSE", 0, 0.0, 1.0, 0.001),
	"op4_f_fine": Param("OP4 F FINE", 0, 0.0, 99.0, 1.0),
	"op4_osc_detune": Param("OP4 OSC DETUNE", 0.5, -7.0, 7.0, 1.0),
	"op4_break_point": Param("OP4 BREAK POINT", 'A-1', 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
	"op4_l_scale_depth": Param("OP4 L SCALE DEPTH", 0, 0.0, 99.0, 1.0),
	"op4_r_scale_depth": Param("OP4 R SCALE DEPTH", 0, 0.0, 99.0, 1.0),
	"op4_l_key_scale": Param("OP4 L KEY SCALE", "-LN", 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
	"op4_r_key_scale": Param("OP4 R KEY SCALE", "-LN", 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
	"op4_rate_scaling": Param("OP4 RATE SCALING", 0, 0.0, 7.0, 1.0),
	"op4_a_mod_sens": Param("OP4 A MOD SENS.", 0, 0.0, 3.0, 1.0),
	"op4_key_velocity": Param("OP4 KEY VELOCITY", 0, 0.0, 7.0, 1.0),
	"op4_switch": Param("OP4 SWITCH", "OP4 SWITCH ON", 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
	"op5_eg_rate_1": Param("OP5 EG RATE 1", 99, 0.0, 99.0, 1.0),
	"op5_eg_rate_2": Param("OP5 EG RATE 2", 99, 0.0, 99.0, 1.0),
	"op5_eg_rate_3": Param("OP5 EG RATE 3", 99, 0.0, 99.0, 1.0),
	"op5_eg_rate_4": Param("OP5 EG RATE 4", 99, 0.0, 99.0, 1.0),
	"op5_eg_level_1": Param("OP5 EG LEVEL 1", 99, 0.0, 99.0, 1.0),
	"op5_eg_level_2": Param("OP5 EG LEVEL 2", 99, 0.0, 99.0, 1.0),
	"op5_eg_level_3": Param("OP5 EG LEVEL 3", 99, 0.0, 99.0, 1.0),
	"op5_eg_level_4": Param("OP5 EG LEVEL 4", 0, 0.0, 99.0, 1.0),
	"op5_output_level": Param("OP5 OUTPUT LEVEL", 0, 0.0, 99.0, 1.0),
	"op5_mode": Param("OP5 MODE", "RATIO", 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
	"op5_f_coarse": Param("OP5 F COARSE", 1, 0.0, 31.0, 1.0),
	"op5_f_fine": Param("OP5 F FINE", 0, 0.0, 99.0, 1.0),
	"op5_osc_detune": Param("OP5 OSC DETUNE", 0.5, -7.0, 7.0, 1.0),
	"op5_break_point": Param("OP5 BREAK POINT", 'A-1', 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
	"op5_l_scale_depth": Param("OP5 L SCALE DEPTH", 0, 0.0, 99.0, 1.0),
	"op5_r_scale_depth": Param("OP5 R SCALE DEPTH", 0, 0.0, 99.0, 1.0),
	"op5_l_key_scale": Param("OP5 L KEY SCALE", "-LN", 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
	"op5_r_key_scale": Param("OP5 R KEY SCALE", "-LN", 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
	"op5_rate_scaling": Param("OP5 RATE SCALING", 0, 0.0, 7.0, 1.0),
	"op5_a_mod_sens": Param("OP5 A MOD SENS.", 0, 0.0, 3.0, 1.0),
	"op5_key_velocity": Param("OP5 KEY VELOCITY", 0, 0.0, 7.0, 1.0),
	"op5_switch": Param("OP5 SWITCH", "OP5 SWITCH ON", 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
	"op6_eg_rate_1": Param("OP6 EG RATE 1", 99, 0.0, 99.0, 1.0),
	"op6_eg_rate_2": Param("OP6 EG RATE 2", 99, 0.0, 99.0, 1.0),
	"op6_eg_rate_3": Param("OP6 EG RATE 3", 99, 0.0, 99.0, 1.0),
	"op6_eg_rate_4": Param("OP6 EG RATE 4", 99, 0.0, 99.0, 1.0),
	"op6_eg_level_1": Param("OP6 EG LEVEL 1", 99, 0.0, 99.0, 1.0),
	"op6_eg_level_2": Param("OP6 EG LEVEL 2", 99, 0.0, 99.0, 1.0),
	"op6_eg_level_3": Param("OP6 EG LEVEL 3", 99, 0.0, 99.0, 1.0),
	"op6_eg_level_4": Param("OP6 EG LEVEL 4", 0, 0.0, 99.0, 1.0),
	"op6_output_level": Param("OP6 OUTPUT LEVEL", 0, 0.0, 99.0, 1.0),
	"op6_mode": Param("OP6 MODE", "RATIO", 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
	"op6_f_coarse": Param("OP6 F COARSE", 1, 0.0, 31.0, 1.0),
	"op6_f_fine": Param("OP6 F FINE", 0, 0.0, 99.0, 1.0),
	"op6_osc_detune": Param("OP6 OSC DETUNE", 0.5, -7.0, 7.0, 1.0),
	"op6_break_point": Param("OP6 BREAK POINT", "A1", 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
	"op6_l_scale_depth": Param("OP6 L SCALE DEPTH", 0, 0.0, 99.0, 1.0),
	"op6_r_scale_depth": Param("OP6 R SCALE DEPTH", 0, 0.0, 99.0, 1.0),
	"op6_l_key_scale": Param("OP6 L KEY SCALE", "-LN", 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
	"op6_r_key_scale": Param("OP6 R KEY SCALE", "-LN", 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
	"op6_rate_scaling": Param("OP6 RATE SCALING", 0, 0.0, 7.0, 1.0),
	"op6_a_mod_sens": Param("OP6 A MOD SENS.", 0, 0.0, 3.0, 1.0),
	"op6_key_velocity": Param("OP6 KEY VELOCITY", 0, 0.0, 7.0, 1.0),
	"op6_switch": Param("OP6 SWITCH", "OP6 SWITCH ON", 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
	"bypass": Param("Bypass", False, 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for boolean values
	# "program": Param("Program", 'ARP 2600  ', 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
}

# instrument.show_editor()
# print(instrument.op1_eg_level_1)
# instrument.op1_eg_level_1.raw_value = 0
# instrument.cutoff = paramDict.get("cutoff").maximum
# instrument.op1_eg_level_1 = 0.5
# print(instrument.op1_eg_level_1)

sysex_mesage = mido.read_syx_file("./synlib/SynLib_001.syx")

instrument(
  sysex_mesage,
  duration=5, # seconds
  sample_rate=sample_rate,
)



# print(instrument.op1_eg_level_2)
# instrument.cutoff = 0.5
# instrument.op1_eg_rate_2.raw_value = 1
# instrument.op1_eg_rate_3.raw_value = 1
# instrument.op1_eg_rate_4.raw_value = 1
# instrument.show_editor()
program_message = [Message("program_change", program=10)]
instrument(
  program_message,
  duration=5, # seconds
  sample_rate=sample_rate,
)
instrument.show_editor()
# for i, (k, v) in enumerate(paramDict.items()):
	# instrument.k = v.value
	# if( (type(v.value) == float) or ( type(v.value) == int )):
		# print(type(v.value))
		# setattr(instrument, k, v.maximum)
		# setattr(instrument, k, v.value)
		

# instrument.show_editor()

# print(instrument.parameters)

# for f in instrument.parameters:
#     print(f)


# print( instrument.parameters )

# print(instrument.parameters.keys())
# print(effect.parameters.keys())
# print(str(instrument.parameters))
# with open('dexed parameters init.txt', 'w') as f:
# 	f.write(str(instrument.parameters))
# dict_keys([
#   'sc_hpf_hz', 'input_lvl_db', 'sensitivity_db',
#   'ratio', 'attack_ms', 'release_ms', 'makeup_db',
#   'mix', 'output_lvl_db', 'sc_active',
#   'full_bandwidth', 'bypass', 'program',
# ])

# effect.feedback = 100

# Render some audio by passing MIDI to an instrument:

message = [Message("note_on", note=60, velocity=100), Message("note_off", note=60, time=5)]

audio = instrument(
  message,
  duration=5, # seconds
  sample_rate=sample_rate,
)

# Apply effects to this audio:
# effected = effect(audio, sample_rate)

# ...or put the effect into a chain with other plugins:
# board = Pedalboard([effect, Reverb()])
# ...and run that pedalboard with the same VST instance!
# effected = board(audio, sample_rate)


with AudioFile('output.wav', 'w', 44100, 2) as o:
	o.write(audio)