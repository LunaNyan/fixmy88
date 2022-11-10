# 나히다의 뿅망치

SC-8850 전용 Control Change를 NRPN으로 일괄 변경합니다.

## 사용 방법

> pip install -r requirements.txt
> 
> main.py [MIDI File] [Output File] [2port]

2port Switch : 트랙 이름을 식별하여 'B'로 시작하는 경우 Port B로, 이외는 Port A로 지정합니다.

## NRPN으로 변경되는 Control Change
아래 컨트롤들은 모두 Data Entry MSB(CC#6)으로 조절합니다.

- TVF LPF (CC#74) → MSB 1 / LSB 32
- Resonance (CC#71) → MSB 1 / LSB 33
- TVF&TVA Envelope
  - Attack Time (CC#73) → MSB 1 / LSB 99
  - Decay Time (CC#75) → MSB 1 / LSB 100
  - Release Time (CC#72) → MSB 1 / LSB 102
- Vibrato
  - Rate (CC#76) → MSB 1 / LSB 8
  - Depth (CC#77) → MSB 1 / LSB 9
  - Delay (CC#78) → MSB 1 / LSB 10
