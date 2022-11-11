import mido
from sys import argv, exit

if len(argv) < 1:
    print("Usage : main.py (MIDI File) [Output File] [2port]")
    print("e.g. main.py test.mid → test_out.mid")
    exit(1)

try:
    if argv[3] == "2port":
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
        # CC Mitigation
        if msg.is_cc(74):
            # TVF LPF
            print("TVF LPF = " + str(msg.value))
            if cc_prev != msg.control:
                tro.append(mido.Message('control_change', channel=msg.channel, control=98, value=1, time=0))
                tro.append(mido.Message('control_change', channel=msg.channel, control=99, value=32, time=0))
            tro.append(mido.Message('control_change', channel=msg.channel, control=6, value=msg.value, time=msg.time))
            cc_prev = msg.control
        elif msg.is_cc(71):
            # TVF Resonance
            print("TVF Resonance = " + str(msg.value))
            if cc_prev != msg.control:
                tro.append(mido.Message('control_change', channel=msg.channel, control=98, value=1, time=0))
                tro.append(mido.Message('control_change', channel=msg.channel, control=99, value=33, time=0))
            tro.append(mido.Message('control_change', channel=msg.channel, control=6, value=msg.value, time=msg.time))
            cc_prev = msg.control
        elif msg.is_cc(73):
            # TVF & TVA Attack Time
            print("TVF & TVA Attack Time = " + str(msg.value))
            if cc_prev != msg.control:
                tro.append(mido.Message('control_change', channel=msg.channel, control=98, value=1, time=0))
                tro.append(mido.Message('control_change', channel=msg.channel, control=99, value=99, time=0))
            tro.append(mido.Message('control_change', channel=msg.channel, control=6, value=msg.value, time=msg.time))
            cc_prev = msg.control
        elif msg.is_cc(75):
            # TVF & TVA Decay Time
            print("TVF & TVA Decay Time = " + str(msg.value))
            if cc_prev != msg.control:
                tro.append(mido.Message('control_change', channel=msg.channel, control=98, value=1, time=0))
                tro.append(mido.Message('control_change', channel=msg.channel, control=99, value=100, time=0))
            tro.append(mido.Message('control_change', channel=msg.channel, control=6, value=msg.value, time=msg.time))
            cc_prev = msg.control
        elif msg.is_cc(72):
            # TVF & TVA Release Time
            print("TVF & TVA Release Time = " + str(msg.value))
            if cc_prev != msg.control:
                tro.append(mido.Message('control_change', channel=msg.channel, control=98, value=1, time=0))
                tro.append(mido.Message('control_change', channel=msg.channel, control=99, value=102, time=0))
            tro.append(mido.Message('control_change', channel=msg.channel, control=6, value=msg.value, time=msg.time))
            cc_prev = msg.control
        elif msg.is_cc(76):
            # Vibrato Rate
            print("Vibrato Rate = " + str(msg.value))
            if cc_prev != msg.control:
                tro.append(mido.Message('control_change', channel=msg.channel, control=98, value=1, time=0))
                tro.append(mido.Message('control_change', channel=msg.channel, control=99, value=8, time=0))
            tro.append(mido.Message('control_change', channel=msg.channel, control=6, value=msg.value, time=msg.time))
            cc_prev = msg.control
        elif msg.is_cc(77):
            # Vibrato Depth
            print("Vibrato Depth = " + str(msg.value))
            if cc_prev != msg.control:
                tro.append(mido.Message('control_change', channel=msg.channel, control=98, value=1, time=0))
                tro.append(mido.Message('control_change', channel=msg.channel, control=99, value=9, time=0))
            tro.append(mido.Message('control_change', channel=msg.channel, control=6, value=msg.value, time=msg.time))
            cc_prev = msg.control
        elif msg.is_cc(78):
            # Vibrato Delay
            print("Vibrato Delay = " + str(msg.value))
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
    sfn = argv[1] + "_out.mid"
elif argv[2].endswith(".mid"):
    sfn = argv[2]
else:
    sfn = argv[2] + ".mid"
mid_cnv.save(sfn)
print("Done")
