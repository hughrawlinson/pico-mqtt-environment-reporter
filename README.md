# MQTT Environment Reporter

A tiny Pico W program to report values from an I<sup>2</sup>C HTS221 Temperature
and Humidity sensor and an LPS22HB pressure sensor to my home MQTT server. The
program is in main.py, and uses configuratin in the `secrets.py` file. My
secrets are not in this repository, but you can use `example_secrets.py` as a
template.

You will also need to install the `hts221` and `umqtt.simple` packages.

I use the MQTT integration on Home Assistant to make these data available for
home automation.
