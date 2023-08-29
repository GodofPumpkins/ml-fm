# Takes a directory full of DX7 sysex patches and outputs a compacted unique list of voices
import os, sys, hashlib
import mido

from collections import OrderedDict

import pedalboard

class Dictlist(dict):
	def __setitem__(self, key, value):
		try:
			self[key]
		except KeyError:
			super(Dictlist, self).__setitem__(key, [])
		self[key].append(value)

def get_all_syx_files():
	sysexs = []
	for path, directories, files in os.walk('synlib'):
		files.sort()
		for file in files:
			d = os.path.join(path, file)
			if d.endswith("syx") or d.endswith("SYX"):
				sysexs.append(d)
	return sysexs

# Pull the name and voice out of a 128 byte buffer, and compute a hash of just the parameters
def parse_128b(buf):

	name = buf[118:128]
	digest = hashlib.md5(buf[:118]).hexdigest()
	algo = buf[110] + 1
	return (buf, name, digest, algo)

# Pull 32 voices out of a sysex patch bank, the most common form 
def parse_4104b(buf):
	voices = []
	for i in range(32):
		start_byte = 6 + (i*128)
		end_byte = start_byte + 128
		voices.append(parse_128b(buf[start_byte:end_byte]))
	return voices

# def sysex_message(patch_number, channel):
#     import dx7
#     # get the 155 bytes for the patch number from the C extension
#     patch_data = dx7.unpack(patch_number)
#     # generate the twos complement checksum for the patch data 
#     # from these dudes fighting w/ each other about who has the best programming skills sigh 
#     # https://yamahamusicians.com/forum/viewtopic.php?t=6864
#     check = ~sum(patch_data) + 1 & 0x7F

#     # Generate the sysex message
#     byte_count = 155 # always 155 bytes of patch information (the operator-on message is only for live mode)
#     msb = byte_count / 127
#     lsb = (byte_count % 127) - 1
#     return [0x43, channel, 0, msb, lsb] + patch_data + [check]

# #_port = mido.open_output()
# def update_voice(patch_number, channel):
#     sysex = sysex_message(patch_number, channel)
#     msg = mido.Message('sysex', data=sysex)
#     #_port.send(program)
#     _port.send(msg)

# def play_note(note, channel):
#     msg = mido.Message('note_on', note=note, channel=channel)
#     _port.send(msg)
# def stop_note(note,channel):
#     msg = mido.Message('note_off',note=note, channel = channel, velocity=0)
#     _port.send(msg)

def parse_all():
	all_files = get_all_syx_files()
	all_patches =[]
	total = 0
	cant = 0
	lengths = 0
	dedup = OrderedDict()
	for i,f in enumerate(all_files):
		# print(f)
		data = bytearray(open(f, 'rb').read())
		if(len(data) == 4104):
			p = parse_4104b(data)
		else:
			cant = cant + 1
			print("cant!!!!")

		lengths = lengths + len(p)
		for j, patch in enumerate(p):
			# print(patch)
			total = total + 1
			dedup[(i*32)+j] = (patch, f, j)
			# print(total)
	# print(lengths)
	return dedup

def unpack_packed_patch(p):
	# Input is a 128 byte thing from compact.bin
	# Output is a 156 byte thing that the synth knows about
	o = [0]*156
	for op in range(6):
		o[op*21:op*21 + 11] = p[op*17:op*17+11]
		leftrightcurves = p[op*17+11]
		o[op * 21 + 11] = leftrightcurves & 3
		o[op * 21 + 12] = (leftrightcurves >> 2) & 3
		detune_rs = p[op * 17 + 12]
		o[op * 21 + 13] = detune_rs & 7
		o[op * 21 + 20] = detune_rs >> 3
		kvs_ams = p[op * 17 + 13]
		o[op * 21 + 14] = kvs_ams & 3
		o[op * 21 + 15] = kvs_ams >> 2
		o[op * 21 + 16] = p[op * 17 + 14]
		fcoarse_mode = p[op * 17 + 15]
		o[op * 21 + 17] = fcoarse_mode & 1
		o[op * 21 + 18] = fcoarse_mode >> 1
		o[op * 21 + 19] = p[op * 17 + 16]
	
	o[126:126+9] = p[102:102+9]
	oks_fb = p[111]
	o[135] = oks_fb & 7
	o[136] = oks_fb >> 3
	o[137:137+4] = p[112:112+4]
	lpms_lfw_lks = p[116]
	o[141] = lpms_lfw_lks & 1
	o[142] = (lpms_lfw_lks >> 1) & 7
	o[143] = lpms_lfw_lks >> 4
	o[144:144+11] = p[117:117+11]
	o[155] = 0x3f

	# Clamp the unpacked patches to a known max. 
	maxes =  [
		99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, # osc6
		3, 3, 7, 3, 7, 99, 1, 31, 99, 14,
		99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, # osc5
		3, 3, 7, 3, 7, 99, 1, 31, 99, 14,
		99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, # osc4
		3, 3, 7, 3, 7, 99, 1, 31, 99, 14,
		99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, # osc3
		3, 3, 7, 3, 7, 99, 1, 31, 99, 14,
		99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, # osc2
		3, 3, 7, 3, 7, 99, 1, 31, 99, 14,
		99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, # osc1
		3, 3, 7, 3, 7, 99, 1, 31, 99, 14,
		99, 99, 99, 99, 99, 99, 99, 99, # pitch eg rate & level 
		31, 7, 1, 99, 99, 99, 99, 1, 5, 7, 48, # algorithm etc
		126, 126, 126, 126, 126, 126, 126, 126, 126, 126, # name
		127 # operator on/off
	]
	for i in range(156):
		if(o[i] > maxes[i]): o[i] = maxes[i]
		if(o[i] < 0): o[i] = 0
	return o

def convert_compact_to_unpacked():
	# Take a compact.bin and make it unpacked.bin
	f = bytearray(open("compact.bin").read())
	o = open("unpacked.bin", "w")
	num_patches = len(f)/128
	for patch in range(num_patches):
		patch_data = f[patch*128:patch*128+128]
		unpacked = unpack_packed_patch(patch_data)
		o.write(bytearray(unpacked))
	o.close()

# Writes all the voices to a binary file of 128 x patches, and also the names in ASCII to a txt file.
def main():
	paramDict = {
		"cutoff": Param("Cutoff", 1, 0, 1, 0.001),
		"resonance": Param("Resonance", 0, 0, 1, 0.001),
		"output": Param("Output", 1, 0, 1, 0.001),
		"master_tune_adj": Param("MASTER TUNE ADJ", 0.5, -1.0, 0.999878, ~0.001996015),
		"algorithm": Param("ALGORITHM", 1, 1.0, 32.0, 1.0),
		"feedback": Param("FEEDBACK", 0, 0.0, 7.0, 1.0),
		"osc_key_sync": Param("OSC KEY SYNC", 1, False, True),
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
		"op1_eg_rate_1": Param("OP1 EG RATE 1", 0.707071, 0.0, 1.0, 0.001),
		"op1_eg_rate_2": Param("OP1 EG RATE 2", 0.40404, 0.0, 1.0, 0.001),
		"op1_eg_rate_3": Param("OP1 EG RATE 3", 0.494949, 0.0, 1.0, 0.001),
		"op1_eg_rate_4": Param("OP1 EG RATE 4", 1, 0.0, 1.0, 0.001),
		"op1_eg_level_1": Param("OP1 EG LEVEL 1", 1, 0.0, 1.0, 0.001),
		"op1_eg_level_2": Param("OP1 EG LEVEL 2", 0.929293, 0.0, 1.0, 0.001),
		"op1_eg_level_3": Param("OP1 EG LEVEL 3", 0, 0.0, 1.0, 0.001),
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
		"op2_eg_rate_1": Param("OP2 EG RATE 1", 0.252525, 0.0, 1.0, 0.001),
		"op2_eg_rate_2": Param("OP2 EG RATE 2", 0.646465, 0.0, 1.0, 0.001),
		"op2_eg_rate_3": Param("OP2 EG RATE 3", 0.494949, 0.0, 1.0, 0.001),
		"op2_eg_rate_4": Param("OP2 EG RATE 4", 1, 0.0, 1.0, 0.001),
		"op2_eg_level_1": Param("OP2 EG LEVEL 1", 0.50505, 0.0, 1.0, 0.001),
		"op2_eg_level_2": Param("OP2 EG LEVEL 2", 1, 0.0, 1.0, 0.001),
		"op2_eg_level_3": Param("OP2 EG LEVEL 3", 0, 0.0, 1.0, 0.001),
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
		"op4_break_point": Param("OP4 BREAK POINT", 0, 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
		"op4_l_scale_depth": Param("OP4 L SCALE DEPTH", 0, 0.0, 99.0, 1.0),
		"op4_r_scale_depth": Param("OP4 R SCALE DEPTH", 0, 0.0, 99.0, 1.0),
		"op4_l_key_scale": Param("OP4 L KEY SCALE", 0, 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
		"op4_r_key_scale": Param("OP4 R KEY SCALE", 0, 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
		"op4_rate_scaling": Param("OP4 RATE SCALING", 0, 0.0, 7.0, 1.0),
		"op4_a_mod_sens": Param("OP4 A MOD SENS.", 0, 0.0, 3.0, 1.0),
		"op4_key_velocity": Param("OP4 KEY VELOCITY", 0, 0.0, 7.0, 1.0),
		"op4_switch": Param("OP4 SWITCH", 1, 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
		"op5_eg_rate_1": Param("OP5 EG RATE 1", 99, 0.0, 99.0, 1.0),
		"op5_eg_rate_2": Param("OP5 EG RATE 2", 99, 0.0, 99.0, 1.0),
		"op5_eg_rate_3": Param("OP5 EG RATE 3", 99, 0.0, 99.0, 1.0),
		"op5_eg_rate_4": Param("OP5 EG RATE 4", 99, 0.0, 99.0, 1.0),
		"op5_eg_level_1": Param("OP5 EG LEVEL 1", 99, 0.0, 99.0, 1.0),
		"op5_eg_level_2": Param("OP5 EG LEVEL 2", 99, 0.0, 99.0, 1.0),
		"op5_eg_level_3": Param("OP5 EG LEVEL 3", 99, 0.0, 99.0, 1.0),
		"op5_eg_level_4": Param("OP5 EG LEVEL 4", 0, 0.0, 99.0, 1.0),
		"op5_output_level": Param("OP5 OUTPUT LEVEL", 0, 0.0, 99.0, 1.0),
		"op5_mode": Param("OP5 MODE", 0, 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
		"op5_f_coarse": Param("OP5 F COARSE", 1, 0.0, 31.0, 1.0),
		"op5_f_fine": Param("OP5 F FINE", 0, 0.0, 99.0, 1.0),
		"op5_osc_detune": Param("OP5 OSC DETUNE", 0.5, -7.0, 7.0, 1.0),
		"op5_break_point": Param("OP5 BREAK POINT", 0, 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
		"op5_l_scale_depth": Param("OP5 L SCALE DEPTH", 0, 0.0, 99.0, 1.0),
		"op5_r_scale_depth": Param("OP5 R SCALE DEPTH", 0, 0.0, 99.0, 1.0),
		"op5_l_key_scale": Param("OP5 L KEY SCALE", 0, 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
		"op5_r_key_scale": Param("OP5 R KEY SCALE", 0, 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
		"op5_rate_scaling": Param("OP5 RATE SCALING", 0, 0.0, 7.0, 1.0),
		"op5_a_mod_sens": Param("OP5 A MOD SENS.", 0, 0.0, 3.0, 1.0),
		"op5_key_velocity": Param("OP5 KEY VELOCITY", 0, 0.0, 7.0, 1.0),
		"op5_switch": Param("OP5 SWITCH", 1, 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
		"op6_eg_rate_1": Param("OP6 EG RATE 1", 99, 0.0, 99.0, 1.0),
		"op6_eg_rate_2": Param("OP6 EG RATE 2", 99, 0.0, 99.0, 1.0),
		"op6_eg_rate_3": Param("OP6 EG RATE 3", 99, 0.0, 99.0, 1.0),
		"op6_eg_rate_4": Param("OP6 EG RATE 4", 99, 0.0, 99.0, 1.0),
		"op6_eg_level_1": Param("OP6 EG LEVEL 1", 99, 0.0, 99.0, 1.0),
		"op6_eg_level_2": Param("OP6 EG LEVEL 2", 99, 0.0, 99.0, 1.0),
		"op6_eg_level_3": Param("OP6 EG LEVEL 3", 99, 0.0, 99.0, 1.0),
		"op6_eg_level_4": Param("OP6 EG LEVEL 4", 0, 0.0, 99.0, 1.0),
		"op6_output_level": Param("OP6 OUTPUT LEVEL", 0, 0.0, 99.0, 1.0),
		"op6_mode": Param("OP6 MODE", 0, 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
		"op6_f_coarse": Param("OP6 F COARSE", 1, 0.0, 31.0, 1.0),
		"op6_f_fine": Param("OP6 F FINE", 0, 0.0, 99.0, 1.0),
		"op6_osc_detune": Param("OP6 OSC DETUNE", 0.5, -7.0, 7.0, 1.0),
		"op6_break_point": Param("OP6 BREAK POINT", 0, 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
		"op6_l_scale_depth": Param("OP6 L SCALE DEPTH", 0, 0.0, 99.0, 1.0),
		"op6_r_scale_depth": Param("OP6 R SCALE DEPTH", 0, 0.0, 99.0, 1.0),
		"op6_l_key_scale": Param("OP6 L KEY SCALE", 0, 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
		"op6_r_key_scale": Param("OP6 R KEY SCALE", 0, 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
		"op6_rate_scaling": Param("OP6 RATE SCALING", 0, 0.0, 7.0, 1.0),
		"op6_a_mod_sens": Param("OP6 A MOD SENS.", 0, 0.0, 3.0, 1.0),
		"op6_key_velocity": Param("OP6 KEY VELOCITY", 0, 0.0, 7.0, 1.0),
		"op6_switch": Param("OP6 SWITCH", 1, 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
		"bypass": Param("Bypass", 0, 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for boolean values
		"program": Param("Program", 0, 0.0, 1.0, 0.001),  # Assuming a default range, as the range is not provided for string values
	}
	compact = open("compact.bin", "wb")
	names = open("names.txt", "w")
	algos = open("algos.txt", "w")
	dedup = parse_all()
	k = 0
	for r, f, num in dedup.values():
		k += 1
		# print(k, r[1])
		compact.write(r[0])
		name = r[1] # the name will be the first name of this voice we saw
		algo = r[3]
		# for i,char in enumerate(name):
		#     # Make sure the name is actually ASCII printable
		#     if(ord(str(char)) < 32): name[i] = ' '
		#     if(ord(str(char)) > 126): name[i] = ' '
		# Keep the original filename and patch number
		# in addition to the "internal" name of the patch
		# which might have duplicate
		name = str(k) + "_" + str(algo) + "_" + bytes(name).decode('utf-8')
		names.write(name)
		names.write('\n')
		algos.write(str(algo))
		algos.write('\n')
	compact.close()
	names.close()
	print("Wrote %d patches to compact.bin & names.txt" % (len(dedup.items())))

if __name__ == "__main__":
	main()

class Param:
	def __init__(self, name = "", value = 0.0, maximum = 1.0, minimum = 0.0, increment = 1.0 ):
		self.name = name
		self.value = value
		self.increment = increment
		self.maximum = maximum
		self.minimum = minimum

		# TODO have key scale stuff map from integer to string later

class Dx7params:
	cutoff = Param("Cutoff", 1, 0, 1, 0.001)
	resonance = Param("Resonance", 0, 0, 1, 0.001)
	output = Param("Output", 1, 0, 1, 0.001)
	master_tune_adj = Param("MASTER TUNE ADJ", 0.5, -1.0, 0.999878, 0.001996015)
	algorithm = Param("ALGORITHM", 1, 1.0, 32.0, 1.0)
	feedback = Param("FEEDBACK", 0, 0.0, 7.0, 1.0)
	osc_key_sync = Param("OSC KEY SYNC", 1, False, True)
	lfo_speed = Param("LFO SPEED", 0.353535, 0.0, 99.0, 1.0)
	lfo_delay = Param("LFO DELAY", 0, 0.0, 99.0, 1.0)
	lfo_pm_depth = Param("LFO PM DEPTH", 0, 0.0, 99.0, 1.0)
	lfo_am_depth = Param("LFO AM DEPTH", 0, 0.0, 1.0, 0.001)
	lfo_key_sync = Param("LFO KEY SYNC", 1, 0.0, 1.0, 0.001)
	lfo_wave = Param("LFO WAVE", 0, 0.0, 1.0, 0.001)
	transpose = Param("TRANSPOSE", 0.5, 0.0, 1.0, 0.001)
	p_mode_sens = Param("P MODE SENS.", 0.428571, 0.0, 1.0, 0.001)
	pitch_eg_rate_1 = Param("PITCH EG RATE 1", 1, 0.0, 1.0, 0.001)
	pitch_eg_rate_2 = Param("PITCH EG RATE 2", 1, 0.0, 1.0, 0.001)
	pitch_eg_rate_3 = Param("PITCH EG RATE 3", 1, 0.0, 1.0, 0.001)
	pitch_eg_rate_4 = Param("PITCH EG RATE 4", 1, 0.0, 1.0, 0.001)
	pitch_eg_level_1 = Param("PITCH EG LEVEL 1", 0.50505, 0.0, 1.0, 0.001)
	pitch_eg_level_2 = Param("PITCH EG LEVEL 2", 0.50505, 0.0, 1.0, 0.001)
	pitch_eg_level_3 = Param("PITCH EG LEVEL 3", 0.50505, 0.0, 1.0, 0.001)
	pitch_eg_level_4 = Param("PITCH EG LEVEL 4", 0.50505, 0.0, 1.0, 0.001)
	op1_eg_rate_1 = Param("OP1 EG RATE 1", 0.707071, 0.0, 1.0, 0.001)
	op1_eg_rate_2 = Param("OP1 EG RATE 2", 0.40404, 0.0, 1.0, 0.001)
	op1_eg_rate_3 = Param("OP1 EG RATE 3", 0.494949, 0.0, 1.0, 0.001)
	op1_eg_rate_4 = Param("OP1 EG RATE 4", 1, 0.0, 1.0, 0.001)
	op1_eg_level_1 = Param("OP1 EG LEVEL 1", 1, 0.0, 1.0, 0.001)
	op1_eg_level_2 = Param("OP1 EG LEVEL 2", 0.929293, 0.0, 1.0, 0.001)
	op1_eg_level_3 = Param("OP1 EG LEVEL 3", 0, 0.0, 1.0, 0.001)
	op1_eg_level_4 = Param("OP1 EG LEVEL 4", 0, 0.0, 1.0, 0.001)
	op1_output_level = Param("OP1 OUTPUT LEVEL", 1, 0.0, 1.0, 0.001)
	op1_mode = Param("OP1 MODE", 0, 0.0, 1.0, 0.001)
	op1_f_coarse = Param("OP1 F COARSE", 0.0322581, 0.0, 1.0, 0.001)
	op1_f_fine = Param("OP1 F FINE", 0, 0.0, 1.0, 0.001)
	op1_osc_detune = Param("OP1 OSC DETUNE", 0.5, 0.0, 1.0, 0.001)
	op1_break_point = Param("OP1 BREAK POINT", 0, 0.0, 1.0, 0.001)
	op1_l_scale_depth = Param("OP1 L SCALE DEPTH", 0, 0.0, 1.0, 0.001)
	op1_r_scale_depth = Param("OP1 R SCALE DEPTH", 0, 0.0, 1.0, 0.001)
	op1_l_key_scale = Param("OP1 L KEY SCALE", 0, 0.0, 1.0, 0.001)
	op1_r_key_scale = Param("OP1 R KEY SCALE", 0, 0.0, 1.0, 0.001)
	op1_rate_scaling = Param("OP1 RATE SCALING", 0, 0.0, 1.0, 0.001)
	op1_a_mod_sens = Param("OP1 A MOD SENS.", 0, 0.0, 1.0, 0.001)
	op1_key_velocity = Param("OP1 KEY VELOCITY", 0, 0.0, 1.0, 0.001)
	op1_switch = Param("OP1 SWITCH", 1, 0.0, 1.0, 0.001)
	op2_eg_rate_1 = Param("OP2 EG RATE 1", 0.252525, 0.0, 1.0, 0.001)
	op2_eg_rate_2 = Param("OP2 EG RATE 2", 0.646465, 0.0, 1.0, 0.001)
	op2_eg_rate_3 = Param("OP2 EG RATE 3", 0.494949, 0.0, 1.0, 0.001)
	op2_eg_rate_4 = Param("OP2 EG RATE 4", 1, 0.0, 1.0, 0.001)
	op2_eg_level_1 = Param("OP2 EG LEVEL 1", 0.50505, 0.0, 1.0, 0.001)
	op2_eg_level_2 = Param("OP2 EG LEVEL 2", 1, 0.0, 1.0, 0.001)
	op2_eg_level_3 = Param("OP2 EG LEVEL 3", 0, 0.0, 1.0, 0.001)
	op2_eg_level_4 = Param("OP2 EG LEVEL 4", 0, 0.0, 1.0, 0.001)
	op2_output_level = Param("OP2 OUTPUT LEVEL", 1, 0.0, 1.0, 0.001)
	op2_mode = Param("OP2 MODE", 0, 0.0, 1.0, 0.001)
	op2_f_coarse = Param("OP2 F COARSE", 0, 0.0, 1.0, 0.001)
	op2_f_fine = Param("OP2 F FINE", 0, 0.0, 1.0, 0.001)
	op2_osc_detune = Param("OP2 OSC DETUNE", 0.5, 0.0, 1.0, 0.001)
	op2_break_point = Param("OP2 BREAK POINT", 0, 0.0, 1.0, 0.001)
	op2_l_scale_depth = Param("OP2 L SCALE DEPTH", 0, 0.0, 1.0, 0.001)
	op2_r_scale_depth = Param("OP2 R SCALE DEPTH", 0, 0.0, 1.0, 0.001)
	op2_l_key_scale = Param("OP2 L KEY SCALE", 0, 0.0, 1.0, 0.001)
	op2_r_key_scale = Param("OP2 R KEY SCALE", 0, 0.0, 1.0, 0.001)
	op2_rate_scaling = Param("OP2 RATE SCALING", 0, 0.0, 1.0, 0.001)
	op2_a_mod_sens = Param("OP2 A MOD SENS.", 0, 0.0, 1.0, 0.001)
	op2_key_velocity = Param("OP2 KEY VELOCITY", 0, 0.0, 1.0, 0.001)
	op2_switch = Param("OP2 SWITCH", 1, 0.0, 1.0, 0.001)
	op3_eg_rate_1 = Param("OP3 EG RATE 1", 0.151515, 0.0, 1.0, 0.001)
	op3_eg_rate_2 = Param("OP3 EG RATE 2", 0.646465, 0.0, 1.0, 0.001)
	op3_eg_rate_3 = Param("OP3 EG RATE 3", 0.494949, 0.0, 1.0, 0.001)
	op3_eg_rate_4 = Param("OP3 EG RATE 4", 1, 0.0, 1.0, 0.001)
	op3_eg_level_1 = Param("OP3 EG LEVEL 1", 0.444444, 0.0, 1.0, 0.001)
	op3_eg_level_2 = Param("OP3 EG LEVEL 2", 1, 0.0, 1.0, 0.001)
	op3_eg_level_3 = Param("OP3 EG LEVEL 3", 0, 0.0, 1.0, 0.001)
	op3_eg_level_4 = Param("OP3 EG LEVEL 4", 0, 0.0, 1.0, 0.001)
	op3_output_level = Param("OP3 OUTPUT LEVEL", 1, 0.0, 1.0, 0.001)
	op3_mode = Param("OP3 MODE", 0, 0.0, 1.0, 0.001)
	op3_f_coarse = Param("OP3 F COARSE", 0.0645161, 0.0, 1.0, 0.001)
	op3_f_fine = Param("OP3 F FINE", 0, 0.0, 1.0, 0.001)
	op3_osc_detune = Param("OP3 OSC DETUNE", 0.5, 0.0, 1.0, 0.001)
	op3_break_point = Param("OP3 BREAK POINT", 0, 0.0, 1.0, 0.001)
	op3_l_scale_depth = Param("OP3 L SCALE DEPTH", 0, 0.0, 1.0, 0.001)
	op3_r_scale_depth = Param("OP3 R SCALE DEPTH", 0, 0.0, 1.0, 0.001)
	op3_l_key_scale = Param("OP3 L KEY SCALE", 0, 0.0, 1.0, 0.001)
	op3_r_key_scale = Param("OP3 R KEY SCALE", 0, 0.0, 1.0, 0.001)
	op3_rate_scaling = Param("OP3 RATE SCALING", 0, 0.0, 1.0, 0.001)
	op3_a_mod_sens = Param("OP3 A MOD SENS.", 0, 0.0, 1.0, 0.001)
	op3_key_velocity = Param("OP3 KEY VELOCITY", 0, 0.0, 1.0, 0.001)
	op3_switch = Param("OP3 SWITCH", 1, 0.0, 1.0, 0.001)
	op4_eg_rate_1 = Param("OP4 EG RATE 1", 0.131313, 0.0, 1.0, 0.001)
	op4_eg_rate_2 = Param("OP4 EG RATE 2", 0.646465, 0.0, 1.0, 0.001)
	op4_eg_rate_3 = Param("OP4 EG RATE 3", 0.494949, 0.0, 1.0, 0.001)
	op4_eg_rate_4 = Param("OP4 EG RATE 4", 1, 0.0, 1.0, 0.001)
	op4_eg_level_1 = Param("OP4 EG LEVEL 1", 0.464646, 0.0, 1.0, 0.001)
	op4_eg_level_2 = Param("OP4 EG LEVEL 2", 1, 0.0, 1.0, 0.001)
	op4_eg_level_3 = Param("OP4 EG LEVEL 3", 0, 0.0, 1.0, 0.001)
	op4_eg_level_4 = Param("OP4 EG LEVEL 4", 0, 0.0, 1.0, 0.001)
	op4_output_level = Param("OP4 OUTPUT LEVEL", 1, 0.0, 1.0, 0.001)
	op4_mode = Param("OP4 MODE", 0, 0.0, 1.0, 0.001)
	op4_f_coarse = Param("OP4 F COARSE", 0, 0.0, 1.0, 0.001)
	op4_f_fine = Param("OP4 F FINE", 0, 0.0, 99.0, 1.0)
	op4_osc_detune = Param("OP4 OSC DETUNE", 0.5, -7.0, 7.0, 1.0)
	op4_break_point = Param("OP4 BREAK POINT", 0, 0.0, 1.0, 0.001)  # Assuming a default range, as the range is not provided for string values
	op4_l_scale_depth = Param("OP4 L SCALE DEPTH", 0, 0.0, 99.0, 1.0)
	op4_r_scale_depth = Param("OP4 R SCALE DEPTH", 0, 0.0, 99.0, 1.0)
	op4_l_key_scale = Param("OP4 L KEY SCALE", 0, 0.0, 1.0, 0.001)  # Assuming a default range, as the range is not provided for string values
	op4_r_key_scale = Param("OP4 R KEY SCALE", 0, 0.0, 1.0, 0.001)  # Assuming a default range, as the range is not provided for string values
	op4_rate_scaling = Param("OP4 RATE SCALING", 0, 0.0, 7.0, 1.0)
	op4_a_mod_sens = Param("OP4 A MOD SENS.", 0, 0.0, 3.0, 1.0)
	op4_key_velocity = Param("OP4 KEY VELOCITY", 0, 0.0, 7.0, 1.0)
	op4_switch = Param("OP4 SWITCH", 1, 0.0, 1.0, 0.001)  # Assuming a default range, as the range is not provided for string values
	op5_eg_rate_1 = Param("OP5 EG RATE 1", 99, 0.0, 99.0, 1.0)
	op5_eg_rate_2 = Param("OP5 EG RATE 2", 99, 0.0, 99.0, 1.0)
	op5_eg_rate_3 = Param("OP5 EG RATE 3", 99, 0.0, 99.0, 1.0)
	op5_eg_rate_4 = Param("OP5 EG RATE 4", 99, 0.0, 99.0, 1.0)
	op5_eg_level_1 = Param("OP5 EG LEVEL 1", 99, 0.0, 99.0, 1.0)
	op5_eg_level_2 = Param("OP5 EG LEVEL 2", 99, 0.0, 99.0, 1.0)
	op5_eg_level_3 = Param("OP5 EG LEVEL 3", 99, 0.0, 99.0, 1.0)
	op5_eg_level_4 = Param("OP5 EG LEVEL 4", 0, 0.0, 99.0, 1.0)
	op5_output_level = Param("OP5 OUTPUT LEVEL", 0, 0.0, 99.0, 1.0)
	op5_mode = Param("OP5 MODE", 0, 0.0, 1.0, 0.001)  # Assuming a default range, as the range is not provided for string values
	op5_f_coarse = Param("OP5 F COARSE", 1, 0.0, 31.0, 1.0)
	op5_f_fine = Param("OP5 F FINE", 0, 0.0, 99.0, 1.0)
	op5_osc_detune = Param("OP5 OSC DETUNE", 0.5, -7.0, 7.0, 1.0)
	op5_break_point = Param("OP5 BREAK POINT", 0, 0.0, 1.0, 0.001)  # Assuming a default range, as the range is not provided for string values
	op5_l_scale_depth = Param("OP5 L SCALE DEPTH", 0, 0.0, 99.0, 1.0)
	op5_r_scale_depth = Param("OP5 R SCALE DEPTH", 0, 0.0, 99.0, 1.0)
	op5_l_key_scale = Param("OP5 L KEY SCALE", 0, 0.0, 1.0, 0.001)  # Assuming a default range, as the range is not provided for string values
	op5_r_key_scale = Param("OP5 R KEY SCALE", 0, 0.0, 1.0, 0.001)  # Assuming a default range, as the range is not provided for string values
	op5_rate_scaling = Param("OP5 RATE SCALING", 0, 0.0, 7.0, 1.0)
	op5_a_mod_sens = Param("OP5 A MOD SENS.", 0, 0.0, 3.0, 1.0)
	op5_key_velocity = Param("OP5 KEY VELOCITY", 0, 0.0, 7.0, 1.0)
	op5_switch = Param("OP5 SWITCH", 1, 0.0, 1.0, 0.001)  # Assuming a default range, as the range is not provided for string values
	op6_eg_rate_1 = Param("OP6 EG RATE 1", 99, 0.0, 99.0, 1.0)
	op6_eg_rate_2 = Param("OP6 EG RATE 2", 99, 0.0, 99.0, 1.0)
	op6_eg_rate_3 = Param("OP6 EG RATE 3", 99, 0.0, 99.0, 1.0)
	op6_eg_rate_4 = Param("OP6 EG RATE 4", 99, 0.0, 99.0, 1.0)
	op6_eg_level_1 = Param("OP6 EG LEVEL 1", 99, 0.0, 99.0, 1.0)
	op6_eg_level_2 = Param("OP6 EG LEVEL 2", 99, 0.0, 99.0, 1.0)
	op6_eg_level_3 = Param("OP6 EG LEVEL 3", 99, 0.0, 99.0, 1.0)
	op6_eg_level_4 = Param("OP6 EG LEVEL 4", 0, 0.0, 99.0, 1.0)
	op6_output_level = Param("OP6 OUTPUT LEVEL", 0, 0.0, 99.0, 1.0)
	op6_mode = Param("OP6 MODE", 0, 0.0, 1.0, 0.001)  # Assuming a default range, as the range is not provided for string values
	op6_f_coarse = Param("OP6 F COARSE", 1, 0.0, 31.0, 1.0)
	op6_f_fine = Param("OP6 F FINE", 0, 0.0, 99.0, 1.0)
	op6_osc_detune = Param("OP6 OSC DETUNE", 0.5, -7.0, 7.0, 1.0)
	op6_break_point = Param("OP6 BREAK POINT", 0, 0.0, 1.0, 0.001)  # Assuming a default range, as the range is not provided for string values
	op6_l_scale_depth = Param("OP6 L SCALE DEPTH", 0, 0.0, 99.0, 1.0)
	op6_r_scale_depth = Param("OP6 R SCALE DEPTH", 0, 0.0, 99.0, 1.0)
	op6_l_key_scale = Param("OP6 L KEY SCALE", 0, 0.0, 1.0, 0.001)  # Assuming a default range, as the range is not provided for string values
	op6_r_key_scale = Param("OP6 R KEY SCALE", 0, 0.0, 1.0, 0.001)  # Assuming a default range, as the range is not provided for string values
	op6_rate_scaling = Param("OP6 RATE SCALING", 0, 0.0, 7.0, 1.0)
	op6_a_mod_sens = Param("OP6 A MOD SENS.", 0, 0.0, 3.0, 1.0)
	op6_key_velocity = Param("OP6 KEY VELOCITY", 0, 0.0, 7.0, 1.0)
	op6_switch = Param("OP6 SWITCH", 1, 0.0, 1.0, 0.001)  # Assuming a default range, as the range is not provided for string values
	bypass = Param("Bypass", 0, 0.0, 1.0, 0.001)  # Assuming a default range, as the range is not provided for boolean values
	program = Param("Program", 0, 0.0, 1.0, 0.001)  # Assuming a default range, as the range is not provided for string values

