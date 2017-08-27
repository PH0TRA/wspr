# wspr
Python 3 script using an AD9851 for WSPR mode

Usage mainly identical to the WsprryPi Raspberry Pi script https://github.com/JamesP6000/WsprryPi.
However the AD9851 generates a much cleaner signal than the square wave from the Raspberry Pi.



Usage:
    python wspr.py [options] callsign locator tx_pwr_dBm f1 <f2> <f3> ...
      OR
    python wspr.py [options] --test-tone f

  Options:<br>
    -h --help
      Print out this help screen.<br>
    -r --repeat
      Repeatedly, and in order, transmit on all the specified command line
      freqs.<br>
    -o --offset
      Add a random frequency offset to each transmission:
        +/- 80 Hz for WSPR.<br>
    -t --test-tone freq
      Simply output a test tone at the specified frequency. Only used
      for debugging and to verify calibration.<br>
    -n --no-delay
      Transmit immediately, do not wait for a WSPR TX window. Used
      for testing only.<br>

  Frequencies can be specified either as an absolute TX carrier frequency, or
  using one of the following strings. If a string is used, the transmission
  will happen in the middle of the WSPR region of the selected band: 
    LF MF 160m 80m 60m 40m 30m 20m 17m 15m 12m 10m 6m 4m 2m

  Transmission gaps can be created by specifying a TX frequency of 0

  Note that 'callsign', 'locator', and 'tx_power_dBm' are simply used to fill
  in the appropriate fields of the WSPR message. Normally, tx_power_dBm should
  be 10, representing the signal power coming out of the Pi. Set this value
  appropriately if you are using an external amplifier.

<B>only type 1 messages are supported. The AD9851 is limited to a 70 MHz max <B>.

default pin use:
W_CLK=18
FQ_UD=23
DATA=24
RESET=25

credits:
original code: https://github.com/brainwagon/genwspr
code compatible for the Raspberry Pi https://github.com/JamesP6000/WsprryPi
