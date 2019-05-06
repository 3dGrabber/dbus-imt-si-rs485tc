#!/usr/bin/python -u
# coding=utf-8
from time import sleep
from velib_python.ve_dbus_service_async import VeDbusServiceAsync
from imt_si_rs485_sensor import ImtSiRs485Sensor
from watchdog import Watchdog
from signals import DbusSignal, ModbusSignal

import sys
import config as c
import logging

log = logging.getLogger('main')
logging.basicConfig(level=c.LOG_LEVEL)


def print_usage():
	print ('Usage:   ' + __file__ + ' <serial device>')
	print ('Example: ' + __file__ + ' ttyUSB0')


def parse_cmdline_args():
	# type: () -> str

	args = sys.argv[1:]
	if len(args) == 0:
		log.info('missing command line argument for tty device')
		print_usage()
		exit(1)

	return args[0]


def main():

	log.info('starting ' + c.DRIVER_NAME)

	tty = parse_cmdline_args()
	sensor = ImtSiRs485Sensor(tty)

	hw_ver, fw_ver = sensor.identify()
	log.info('found IMT SI-RS485 sensor')

	# add hw and fw version to the signals, they are mandatory
	signals = c.SIGNALS + [DbusSignal('/HardwareVersion', hw_ver), DbusSignal('/FirmwareVersion', fw_ver)]

	service_name = c.SERVICE_NAME + '.' + tty
	watchdog_timeout = (c.UPDATE_INTERVAL + c.SERIAL_TIMEOUT) * 2

	# starting watchdog here, because with VeDbusServiceAsync we are going multi-threaded
	with Watchdog(watchdog_timeout) as watchdog, VeDbusServiceAsync(service_name, signals) as dbus:

		# only the modbus signals are updated, the others are const
		modbus_signals = [s for s in signals if isinstance(s, ModbusSignal)]

		while True:

			watchdog.alive()  # signal the watchdog that we are still alive

			registers = sensor.read_modbus_registers()

			for s in modbus_signals:
				dbus[s.dbus_path] = registers[s.reg_no] * s.gain

			log.debug('iteration finished, sleeping for ' + str(c.UPDATE_INTERVAL) + ' seconds')
			sleep(c.UPDATE_INTERVAL)


# noinspection PyBroadException
try:
	main()

except Exception, e:

	log.error(e.message)

	# show stacktrace only in debug mode
	if c.LOG_LEVEL <= logging.DEBUG:
		ex = sys.exc_info()
		raise ex[0], ex[1], ex[2]

finally:
	log.info(c.DRIVER_NAME + ' has shut down')
