from TSL2561 import TSL2561

chip = TSL2561()
print(chip.read_channel0())
print(chip.read_channel1())
print(chip.calculate_lux(chip.read_channel0()))
print(chip.get_visible_lux())
print(chip.get_full_lux())
print(chip.get_ir_lux())
