metadata = {'apiLevel': '2.13'}
def run(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware(
        load_name='corning_96_wellplate_360ul_flat',
        location=1)
    tiprack_1 = protocol.load_labware(
        load_name='opentrons_96_tiprack_300ul',
        location=2)
    tiprack_2 = protocol.load_labware(
        load_name='opentrons_96_tiprack_300ul',
        location=3)
    reservoir = protocol.load_labware(
        load_name='usascientific_12_reservoir_22ml',
        location=4)
    p300 = protocol.load_instrument(
        instrument_name='p300_single',
        mount='right',
        tip_racks=[tiprack_1, tiprack_2])
    p300.distribute(50, reservoir['A12'], plate.wells())

    for i in range(8):
        # save the source well and destination column to variables
        source = reservoir.wells()[i]
        source = reservoir.wells()[i]
        row = plate.rows()[i]

    p300.transfer(30, source, row[0], mix_after=(3, 25))

    p300.transfer(
        30, row[:11], row[1:],
        mix_after=(3, 25))