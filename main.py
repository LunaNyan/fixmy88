import mido
from sys import argv, exit

print("Nahida's Rubber Hammer : Convert SC-8850 Exclusive Control to NRPN")

if len(argv) == 1:
    print("Usage : main.py (MIDI File) [Output File] [2port]")
    print("e.g. main.py test.mid → test_out.mid")
    exit(1)

try:
    if argv[3] == "2port":
        dualport = True
    else:
        print("type '2port' properly")
        i = input("Use 2-Port mode?")
        if i == "y" or i == "Y":
            dualport = True
        else:
            dualport = False
except IndexError:
    try:
        if argv[2] == "2port":
            dualport = True
        else:
            dualport = False
    except IndexError:
        dualport = False

f = mido.MidiFile(argv[1])
mid_cnv = mido.MidiFile()

mid_cnv.charset = f.charset
mid_cnv.ticks_per_beat = f.ticks_per_beat

cnt = 1

for tr in f.tracks:
    # each tracks
    tro = mido.MidiTrack()
    cc_prev = -1
    for msg in tr:
        if msg.type == 'track_name':
            print("Processing : " + msg.name + " [" + str(cnt) + " / " + str(len(f.tracks)) + "]")
        # Dual-Port Mitigation
        if dualport and msg.type == 'track_name':
            if msg.name.startswith("B"):
                print("Port B Found")
                tro.append(msg)
                tro.append(mido.MetaMessage('midi_port', port=1, time=0))
            else:
                tro.append(msg)
                tro.append(mido.MetaMessage('midi_port', port=0, time=0))
        # RPN null 스킵
        if msg.is_cc(100) or msg.is_cc(101):
            if msg.value == 127:
                continue
            else:
                tro.append(msg)
        # CC Mitigation
        if msg.is_cc(74):
            # TVF LPF
            if cc_prev != msg.control:
                tro.append(mido.Message('control_change', channel=msg.channel, control=98, value=1, time=0))
                tro.append(mido.Message('control_change', channel=msg.channel, control=99, value=32, time=0))
            tro.append(mido.Message('control_change', channel=msg.channel, control=6, value=msg.value, time=msg.time))
            cc_prev = msg.control
        elif msg.is_cc(71):
            # TVF Resonance
            if cc_prev != msg.control:
                tro.append(mido.Message('control_change', channel=msg.channel, control=98, value=1, time=0))
                tro.append(mido.Message('control_change', channel=msg.channel, control=99, value=33, time=0))
            tro.append(mido.Message('control_change', channel=msg.channel, control=6, value=msg.value, time=msg.time))
            cc_prev = msg.control
        elif msg.is_cc(73):
            # TVF & TVA Attack Time
            if cc_prev != msg.control:
                tro.append(mido.Message('control_change', channel=msg.channel, control=98, value=1, time=0))
                tro.append(mido.Message('control_change', channel=msg.channel, control=99, value=99, time=0))
            tro.append(mido.Message('control_change', channel=msg.channel, control=6, value=msg.value, time=msg.time))
            cc_prev = msg.control
        elif msg.is_cc(75):
            # TVF & TVA Decay Time
            if cc_prev != msg.control:
                tro.append(mido.Message('control_change', channel=msg.channel, control=98, value=1, time=0))
                tro.append(mido.Message('control_change', channel=msg.channel, control=99, value=100, time=0))
            tro.append(mido.Message('control_change', channel=msg.channel, control=6, value=msg.value, time=msg.time))
            cc_prev = msg.control
        elif msg.is_cc(72):
            # TVF & TVA Release Time
            if cc_prev != msg.control:
                tro.append(mido.Message('control_change', channel=msg.channel, control=98, value=1, time=0))
                tro.append(mido.Message('control_change', channel=msg.channel, control=99, value=102, time=0))
            tro.append(mido.Message('control_change', channel=msg.channel, control=6, value=msg.value, time=msg.time))
            cc_prev = msg.control
        elif msg.is_cc(76):
            # Vibrato Rate
            if cc_prev != msg.control:
                tro.append(mido.Message('control_change', channel=msg.channel, control=98, value=1, time=0))
                tro.append(mido.Message('control_change', channel=msg.channel, control=99, value=8, time=0))
            tro.append(mido.Message('control_change', channel=msg.channel, control=6, value=msg.value, time=msg.time))
            cc_prev = msg.control
        elif msg.is_cc(77):
            # Vibrato Depth
            if cc_prev != msg.control:
                tro.append(mido.Message('control_change', channel=msg.channel, control=98, value=1, time=0))
                tro.append(mido.Message('control_change', channel=msg.channel, control=99, value=9, time=0))
            tro.append(mido.Message('control_change', channel=msg.channel, control=6, value=msg.value, time=msg.time))
            cc_prev = msg.control
        elif msg.is_cc(78):
            # Vibrato Delay
            if cc_prev != msg.control:
                tro.append(mido.Message('control_change', channel=msg.channel, control=98, value=1, time=0))
                tro.append(mido.Message('control_change', channel=msg.channel, control=99, value=10, time=0))
            tro.append(mido.Message('control_change', channel=msg.channel, control=6, value=msg.value, time=msg.time))
            cc_prev = msg.control
        else:
            # Normal Message
            tro.append(msg)
            cc_prev = -1
    print("Copied " + str(len(tro)) + " Messages")
    mid_cnv.tracks.append(tro)
    cnt += 1

print("Saving")
if len(argv) == 2:
    # Output Path가 지정되지 않음
    sfn = argv[1] + "_out.mid"
elif len(argv) == 3 and argv[2] == "2port":
    # argv 개수는 3개이나 Output Path가 지정되지 않음
    sfn = argv[1].replace(".mid", "") + "_out.mid"
elif argv[2].endswith(".mid"):
    sfn = argv[2]
else:
    sfn = argv[2] + ".mid"
mid_cnv.save(sfn)
print("Done")
