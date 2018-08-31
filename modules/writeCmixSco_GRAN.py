import numpy as np
# GENERATE THE RTcmix score ! (alternate to generating the midi score)
def writeCmixSco_GRAN(tones_dict,base_name):
    # ====================
    score_name = base_name + '.sco'
    dur = tones_dict['durs']
    dur_string = 'dur = ' + str(dur) + '\n'

    p1 = tones_dict['p1']
    indexes = np.arange(len(p1))
    print(len(p1), len(indexes))
    cmixline = np.zeros(2*len(p1))
    cmixline[1::2] = p1
    cmixline[0:-1:2] = indexes
    p1_pitch_cmixline = str(cmixline.tolist()).strip('[').strip(']')

    f_out = open("./" + score_name , 'w')
    # YOU MUST DELETE THE SOUND FILE BEFORE RUNNING (either with python or with -clobber )
    f_out.write("set_option(\"clobber = on\")\n") #"\n" added
    f_out.write("rtsetparams(44100, 2)\n")
    f_out.write("reset(44100)\n")
    f_out.write("load(\"GRANSYNTH\")\n")
    f_out.write(dur_string)

    output_string = 'rtoutput(\"' + base_name + '.wav\")\n'
    # don't need the brackets to make it an array !
    print(output_string)
    f_out.write(output_string)

    #f_out.write("waveform = maketable(\"sine\", 1000, 1.0, 0.4, 0.2)\n")
    #f_out.write("ampenv = maketable(\"window\", 1000, \"hamming\")\n")

    #f_out.write("amp = maketable(\"line\", 500, 0,0, 1,1, 2,0.5, 3,1, 4,0)\n")
    f_out.write("amp = 7000 \n")
    #f_out.write("wave = maketable(\"wave\", 2000, 1, 0, 0.7, 0, 0.4)\n")
    f_out.write("wave = maketable(\"wave\", 2000, \"sine\")\n")
    f_out.write("granenv = maketable(\"window\", 2000, \"hanning\")\n")
    #f_out.write("hoptime = maketable(\"line\", \"nonorm\", 1000, 0,0.01, 1,0.002, 2,0.05)\n")
    f_out.write("hoptime = 0.01\n") # "maketable(\"line\", \"nonorm\", 1000, 0,0.01, 1,0.002, 2,0.05)\n")
    #f_out.write("hoptime = maketable(\"line\", \"nonorm\", 1000, 0,0.01, 1,0.002, 2,0.05)\n")

    #f_out.write("hopjitter = 0.0001\n") # randomness around hoptime !
    f_out.write("hopjitter = 0.00\n")
    f_out.write("mindur = .05\n")
    f_out.write("maxdur = .05\n")
    #f_out.write("mindur = .04\n")
    #f_out.write("maxdur = .06\n")
    f_out.write("minamp = maxamp = 1\n")
    # this is the first one to map data to.. mean pitch around which the randomness is built.
    #f_out.write("pitch = maketable(\"line\", \"nonorm\", 1000, 0,1, 1,20)\n")
    pitch_cmd = "pitch = maketable(\"line\", \"nonorm\", 1000, " + p1_pitch_cmixline + ')\n'
    f_out.write(pitch_cmd)
    #f_out.write("transpcoll = maketable(\"literal\", \"nonorm\", 0, 0, .02, .03, .05, .07, .10)\n")
    f_out.write("transpcoll = maketable(\"literal\", \"nonorm\", 0, 0)\n")
    f_out.write("pitchjitter = 1\n")

    f_out.write("st = 0\n")
    f_out.write("GRANSYNTH(st, dur, amp, wave, granenv, hoptime, hopjitter, mindur, maxdur, minamp, maxamp, 1.0*pitch, transpcoll, pitchjitter, 14, 0, 1)\n")
#    f_out.write("GRANSYNTH(st, dur, amp*7000, wave, granenv, hoptime, hopjitter, mindur, maxdur, minamp, maxamp, 0.9*pitch, transpcoll, pitchjitter, 14, 0, 1)\n")
#    f_out.write("GRANSYNTH(st, dur, amp*7000, wave, granenv, hoptime, hopjitter, mindur, maxdur, minamp, maxamp, 0.7*pitch, transpcoll, pitchjitter, 14, 0, 1)\n")

    return score_name
    # tab_han = 'waveform'
    #
    # times = tones_dict['times']
    # notes = tones_dict['notes']
    # durs = tones_dict['durs']
    # amps = tones_dict['amps']
    # pans = tones_dict['pans']
    #
    # for i,note_val in enumerate(notes):
    #     t_start = times[i]
    #     dur = durs[i]
    #     freq = note_val # coming in from enumerate
    #     amp = amps[i]
    #     pan = pans[i]
    #
    #     note_string = 'WAVETABLE(' + str(t_start) + ', ' \
    #                   + str(dur)  + ', ' + str(amp) + '*ampenv' + ', ' \
    #                   + str(freq)  + ', ' + str(pan)  + ', ' \
    #                   +  tab_han + ')\n'
    #     f_out.write(note_string)
    # f_out.close()
