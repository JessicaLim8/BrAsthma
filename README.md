# brAsthma

A bra that uses force sensors and pulse sensors to determine if asthmatic patients are at risk of an asthma attack

### Data collection
- Averages of input are taken over a set range, and compared in relation to previously collected data, as well as presets
- bpm data can be collected via pulse sensor, or bpm data can be used to stimulate reality
- Force sensors data is obtained and calibrated so that initaial force experiences is a zero-ing of force

### Warning Output
- Vibrator motors will run if a dangerous condition is being met
- It will run until this condition has resolved itself
- There are two motors, one for force, one for pulse

### Pulse sensor
Dangerous conditions include
- Levels too high above the threshold, in accordance to the inidivuals resting heart rate
- Levels that have increased too much in comparison to the previous heart rate interval average

### Force sensor
Dangerous levels include
- Levels that are too low below the threshold (meaning the chest has not expanded enough)
- Levels that have decreased to much in comparison to previous readings (indication a failure of proper breathing)
