EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:switches
LIBS:relays
LIBS:motors
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L VCC #PWR?
U 1 1 5A5CDE0A
P 3750 1700
F 0 "#PWR?" H 3750 1550 50  0001 C CNN
F 1 "VCC" H 3750 1850 50  0000 C CNN
F 2 "" H 3750 1700 50  0001 C CNN
F 3 "" H 3750 1700 50  0001 C CNN
	1    3750 1700
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 5A5CDE1E
P 3600 1700
F 0 "#PWR?" H 3600 1450 50  0001 C CNN
F 1 "GND" H 3600 1550 50  0000 C CNN
F 2 "" H 3600 1700 50  0001 C CNN
F 3 "" H 3600 1700 50  0001 C CNN
	1    3600 1700
	1    0    0    -1  
$EndComp
$Comp
L Conn_01x04 J?
U 1 1 5A5CDEBE
P 4550 2150
F 0 "J?" H 4550 2350 50  0000 C CNN
F 1 "Conn_01x04" H 4550 1850 50  0000 C CNN
F 2 "" H 4550 2150 50  0001 C CNN
F 3 "" H 4550 2150 50  0001 C CNN
	1    4550 2150
	1    0    0    -1  
$EndComp
$Comp
L Conn_01x04 J?
U 1 1 5A5CDF18
P 4550 2700
F 0 "J?" H 4550 2900 50  0000 C CNN
F 1 "Conn_01x04" H 4550 2400 50  0000 C CNN
F 2 "" H 4550 2700 50  0001 C CNN
F 3 "" H 4550 2700 50  0001 C CNN
	1    4550 2700
	1    0    0    -1  
$EndComp
$Comp
L Conn_01x04 J?
U 1 1 5A5CDF9D
P 4550 3250
F 0 "J?" H 4550 3450 50  0000 C CNN
F 1 "Conn_01x04" H 4550 2950 50  0000 C CNN
F 2 "" H 4550 3250 50  0001 C CNN
F 3 "" H 4550 3250 50  0001 C CNN
	1    4550 3250
	1    0    0    -1  
$EndComp
$Comp
L Conn_01x04 J?
U 1 1 5A5CDFBB
P 4550 3800
F 0 "J?" H 4550 4000 50  0000 C CNN
F 1 "Conn_01x04" H 4550 3500 50  0000 C CNN
F 2 "" H 4550 3800 50  0001 C CNN
F 3 "" H 4550 3800 50  0001 C CNN
	1    4550 3800
	1    0    0    -1  
$EndComp
Wire Bus Line
	3700 2050 3700 4050
Wire Bus Line
	3750 2050 3750 4050
Wire Bus Line
	3800 2050 3800 4050
Wire Bus Line
	3850 2050 3850 4050
Wire Wire Line
	4350 2600 3700 2600
Wire Wire Line
	4350 2700 3750 2700
Wire Wire Line
	4350 2800 3800 2800
Wire Wire Line
	4350 2900 3850 2900
Wire Wire Line
	4350 2050 3700 2050
Wire Wire Line
	4350 2150 3750 2150
Wire Wire Line
	4350 2250 3800 2250
Wire Wire Line
	4350 2350 3850 2350
Wire Wire Line
	4350 3150 3700 3150
Wire Wire Line
	4350 3250 3750 3250
Wire Wire Line
	4350 3350 3800 3350
Wire Wire Line
	4350 3450 3850 3450
Wire Wire Line
	4350 3700 3700 3700
Wire Wire Line
	4350 3800 3750 3800
Wire Wire Line
	4350 3900 3800 3900
Wire Wire Line
	4350 4000 3850 4000
Wire Wire Line
	3600 1700 3700 1700
Wire Wire Line
	3700 1700 3700 2050
Wire Wire Line
	3750 1700 3750 2050
$EndSCHEMATC
