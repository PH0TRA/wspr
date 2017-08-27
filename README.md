# wspr
Python 3 script using an AD9851 for WSPR mode

Usage mainly identical to the WsprryPi Raspberry Pi script https://github.com/JamesP6000/WsprryPi


Usage:
    wspr [options] callsign locator tx_pwr_dBm f1 <f2> <f3> ...
      OR
    wspr [options] --test-tone f

  Options:
    -h --help
      Print out this help screen.
    -p --ppm ppm
      Known PPM correction to 19.2MHz RPi nominal crystal frequency.
    -s --self-calibration
      Check NTP before every transmission to obtain the PPM error of the
      crystal (default setting!).
    -f --free-running
      Do not use NTP to correct frequency error of RPi crystal.
    -r --repeat
      Repeatedly, and in order, transmit on all the specified command line
      freqs.
    -x --terminate <n>
      Terminate after n transmissions have been completed.
    -o --offset
      Add a random frequency offset to each transmission:
        +/- 80 Hz for WSPR
        +/- 8 Hz for WSPR-15
    -t --test-tone freq
      Simply output a test tone at the specified frequency. Only used
      for debugging and to verify calibration.
    -n --no-delay
      Transmit immediately, do not wait for a WSPR TX window. Used
      for testing only.

  Frequencies can be specified either as an absolute TX carrier frequency, or
  using one of the following strings. If a string is used, the transmission
  will happen in the middle of the WSPR region of the selected band.
    LF LF-15 MF MF-15 160m 160m-15 80m 60m 40m 30m 20m 17m 15m 12m 10m 6m 4m 2m
  <B>-15 indicates the WSPR-15 region of band <B>.

  Transmission gaps can be created by specifying a TX frequency of 0

  Note that 'callsign', 'locator', and 'tx_power_dBm' are simply used to fill
  in the appropriate fields of the WSPR message. Normally, tx_power_dBm should
  be 10, representing the signal power coming out of the Pi. Set this value
  appropriately if you are using an external amplifier.

credits:
original code: https://github.com/brainwagon/genwspr
code compatible for the Raspberry Pi https://github.com/JamesP6000/WsprryPi
