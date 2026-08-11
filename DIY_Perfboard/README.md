# LTS Respooler ESP32-S3 Perfboard Build

This is a point-to-point replacement for the LTS Driver Board, using the repository's **Control Board V4 / ESP32-S3 firmware pin map**. It is not a copy of the Control Board PCB.

The recommended arrangement uses socketed modules so that the ESP32-S3, TMC2209, buck converter, and fan switch can be replaced individually. The perfboard assembly will not fit the stock electronics enclosure without modification.

Shopping links and availability were checked on 2026-08-11. Prices and marketplace sellers change; verify the displayed specification before ordering.

## Important compatibility requirements

- Use an **ESP32-S3** development board exposing GPIO 9, 10, 11, 12, 13, 14, 17, 18, 21, 40, and 47. The reference layout uses an Espressif ESP32-S3-DevKitC-1 containing an ESP32-S3-WROOM-1.
- Use the **Control Board V4 firmware**, not the ESP32-WROOM-32 / Driver Board firmware.
- The TMC2209 carrier must have **0.11 ohm sense resistors**, normally marked `R110`, because the firmware defines `R_SENSE 0.11f`.
- The TMC2209 UART address is zero. Tie `MS1` and `MS2` low unless the chosen carrier already does this reliably.
- Never connect the stepper motor, fan, or servo power to a GPIO pin.
- All grounds—12 V input, 5 V supply, ESP32, TMC2209, servo, fan, LED, button, and sensor—must be common.

## Recommended shopping list

### Core electronics

| Qty | Item | Required specification | Recommended source | Alternatives / notes |
|---:|---|---|---|---|
| 1 | ESP32-S3 development board | ESP32-S3-WROOM-1, 8 MB flash, DevKitC-1 pin breakout | [Adafruit ESP32-S3-DevKitC-1](https://www.adafruit.com/product/5312) | [Amazon US search](https://www.amazon.com/s?k=ESP32-S3-DevKitC-1-N8). Extra PSRAM is harmless; do not substitute a classic ESP32-WROOM-32 board with this wiring. |
| 1 | TMC2209 StepStick carrier and heatsink | UART-capable, standard 2×8 StepStick pins, `R110` sense resistors | [BIGTREETECH TMC2209 on Amazon](https://www.amazon.com/dp/B08SMDY3SQ) | The original LTS BOM names this listing. Confirm the actual board is marked `R110`; marketplace listings may change revisions. |
| 1 | NEMA 17 stepper motor | Bipolar 4-wire, 1.8°, 42×42×38 mm, 5 mm shaft | [STEPPERONLINE motor on Amazon](https://www.amazon.com/dp/B0B38GX54H) | This is the exact listing from the original LTS BOM. Determine coil pairs with an ohmmeter rather than trusting wire colors. |
| 1 | 12 V DC supply | Regulated, center-positive, at least 3 A recommended | [12 V 5 A supply at Adafruit](https://www.adafruit.com/product/352) | The [original LTS 12 V listing](https://www.amazon.com/dp/B091XSVV1Y) is rated only for the original minimum. A 3–5 A supply gives more margin; fit a 2–3 A fuse on the board. |
| 1 | 12 V to 5 V buck converter | Fixed 5 V, at least 2.5 A continuous | [Adafruit 5 V 3 A UBEC](https://www.adafruit.com/product/1385) | Board-mount option: [Pololu D24V22F5, 5 V 2.5 A](https://www.pololu.com/product/2858). Budget option: [LM2596 modules on Amazon](https://www.amazon.com/s?k=LM2596+5V+buck+converter); adjust and meter-check before connecting electronics. |
| 1 | Fan MOSFET driver | Accepts 3.3 V logic, low-side switched output, flyback diode | [Adafruit MOSFET Driver](https://www.adafruit.com/product/5648) | It includes an AO3406 MOSFET and 1N4007 diode. A discrete logic-level N-MOSFET, 1 kΩ gate resistor, 10 kΩ pulldown, and flyback diode can replace it. |
| 1 | Pad-per-hole perfboard | 2.54 mm pitch, approximately 90×150 mm | [Amazon US search](https://www.amazon.com/s?k=9x15cm+2.54mm+perfboard) | Use pad-per-hole board, not stripboard, unless you deliberately cut every required strip. |

### Original parts that fit the printed Respooler Pro

These are the exact Maker's Supply parts in the author's current MakerWorld BOM. Generic alternatives may not fit the printed parts.

| Qty | Original part | Connection to perfboard | Source |
|---:|---|---|---|
| 1 | PG001 9 g positional digital servo, 180°, clutch protected | Signal through 330 Ω to GPIO12; red to +5 V; brown/black to GND | [Bambu Maker's Supply PG001](https://store.bambulab.com/products/9g-servo-motor-with-clutch-protection?id=42123031019656) |
| 1 pack | XA008 momentary button module | GPIO10 to switch; other switch terminal to GND | [Bambu Maker's Supply XA008](https://store.bambulab.com/products/momentary-button-module-with-2pin-sh1-0-connector-1pcs?id=602277975952400385) |
| 1 pack | KB003 WS2812 RGB LED | +5 V, GND, and DIN through 330 Ω from GPIO9 | [Bambu Maker's Supply KB003](https://store.bambulab.com/products/ws2812-rgb-led-with-idc0-8-4pin-2pcs?id=592917518379696130) |
| 1 | JB001 3004 slim micro fan, 5 V | Fan `+` to MOSFET driver `+`; fan `-` to switched `-` | [Bambu Maker's Supply JB001](https://store.bambulab.com/products/3004-slim-micro-fan-5v-with-2pin-sh1-0?id=42564236017800) |
| 1 pack | IA006 self-locking switch used as filament sensor | GPIO11 to switch; other switch terminal to GND | [Bambu Maker's Supply IA006](https://store.bambulab.com/products/self-locking-button-switch-with-sh1-0-connector?id=42123262427272) |
| 1 pack | IC007 200 mm SH1.0 wire pairs | Sensor/accessory wiring | [Bambu Maker's Supply IC007](https://store.bambulab.com/products/wire-pair-with-sh1-0?id=42122988978312) |

The KB003 LED uses a small 0.8 mm-pitch connector that is awkward on perfboard. The easiest DIY alternative is a normal three-pad WS2812B/NeoPixel breakout with `5V`, `DIN`, and `GND`, but it may require a modified control-panel mount. Do not connect a bare, ordinary RGB LED in its place; the firmware sends the WS2812 protocol.

### Perfboard hardware and passives

| Qty | Part | Purpose |
|---:|---|---|
| 2×22 contacts | 2.54 mm female header strips | Socket the ESP32-S3 DevKitC-1 |
| 2×8 contacts | 2.54 mm female header strips | Socket the TMC2209; this helps prevent destructive reversed insertion |
| 1 | 2-pin 5.08 mm screw terminal or 5.5×2.1 mm barrel-jack pigtail | 12 V input |
| 1 | 4-pin 5.08 mm screw terminal or matching motor connector | Stepper A1/A2/B1/B2 |
| 3 | 2-pin terminals/pigtails | Button, sensor, and fan |
| 1 | 3-pin male header | Servo signal, +5 V, GND |
| 1 | 3-pin header | WS2812 +5 V, DIN, GND if using a generic breakout |
| 1 | 2-pin header and jumper | `JP1`, removable buck-5-V feed to ESP32 5 V pin |
| 1 | 2–3 A inline fuse and holder, or resettable fuse | Protect the 12 V wiring |
| 1 | 100 µF, 35 V electrolytic | TMC2209 VM bulk capacitor, close to the carrier |
| 1 | 470–1000 µF, 10 V electrolytic | 5 V servo/ESP bulk capacitor |
| 2 | 100 nF ceramic | Local 5 V and LED decoupling |
| 3 | 330 Ω, 1/4 W | Servo signal, WS2812 data, optional connection LED |
| 1 | 1 kΩ, 1/4 W | ESP32 TX to single-wire TMC2209 UART net |
| 1 each | Red, orange, violet, blue, green, black hookup wire | 12 V, 5 V, 3.3 V, GPIO, UART, and GND nets |
| as needed | 22 AWG stranded wire | 12 V, 5 V, motor phases, fan, servo power |
| as needed | 26 AWG solid wire | Short logic interconnects on perfboard |
| 1 | TMC2209 heatsink | Install with airflow and without shorting pads |

Useful searches: [female headers](https://www.amazon.com/s?k=2.54mm+female+header+strip), [screw terminals](https://www.amazon.com/s?k=5.08mm+screw+terminal+2+pin+4+pin), [capacitor assortment](https://www.amazon.com/s?k=electrolytic+capacitor+assortment+35V), and [hookup wire](https://www.amazon.com/s?k=22+26+AWG+hookup+wire+kit).

## Authoritative point-to-point netlist

Physical pin order varies among ESP32-S3 and TMC2209 board revisions. Wire by the **printed pin names**, not merely by the apparent position in the layout drawing.

### Power

| From | To |
|---|---|
| 12 V input `+` | Fuse F1 input |
| Fuse F1 output | `+12V` bus |
| 12 V input `-` | `GND` bus |
| `+12V` bus | TMC2209 `VM` and buck converter input `+` |
| `GND` bus | Both TMC2209 GND pins, buck input/output GND, ESP32 GND, and every accessory ground |
| C1 100 µF/35 V `+` | `+12V` beside TMC2209 `VM` |
| C1 `-` | `GND` beside TMC2209 |
| Buck 5 V output | `+5V` bus |
| C2 470–1000 µF/10 V `+` | `+5V`, close to servo connector |
| C2 `-` | `GND` |
| `+5V` bus | JP1 then ESP32 `5V`; servo `+`; WS2812 `5V`; fan-driver `V+` |
| ESP32 `3V3` | TMC2209 `VIO` / `VCC_IO` only |

Remove JP1 before attaching USB unless the exact DevKit schematic explicitly guarantees that its USB 5 V and header 5 V are safely isolated. Grounds remain connected.

### TMC2209 logic and motor

| ESP32-S3 / net | TMC2209 carrier |
|---|---|
| GPIO14 | `STEP` |
| GPIO21 | `DIR` |
| GPIO40 | `EN` / `ENN` |
| GPIO18 (`UART RX`) | Active `PDN_UART` pin directly |
| GPIO17 (`UART TX`) | 1 kΩ resistor, then the same `PDN_UART` net |
| GND | `MS1` and `MS2`, selecting UART address 0 |
| No connection | `CLK`, `DIAG`, `INDEX` unless required by the carrier's own documentation |
| Motor coil A pair | `A1` and `A2` |
| Motor coil B pair | `B1` and `B2` |

For a BIGTREETECH V1.2 carrier, its manual says the fourth pin on the EN/MS/PDN header is the factory-selected UART pin. Check the solder-jumper position on the actual module.

### Accessories

| ESP32-S3 / supply | Accessory |
|---|---|
| GPIO10 | Momentary button; other button terminal to GND |
| GPIO11 | Filament switch; other switch terminal to GND. The firmware interprets LOW as filament present. |
| GPIO12 through 330 Ω | Servo signal; servo power from +5 V and GND |
| GPIO9 through 330 Ω | WS2812 `DIN`; LED power from +5 V and GND |
| GPIO13 | Fan-driver `IN`; driver `V+` to +5 V and driver GND to GND |
| Fan `+` / fan `-` | Fan-driver `+` output / switched `-` output |
| +3.3 V → 1 kΩ → LED anode; LED cathode → GPIO47 | Optional active-low Bluetooth/connection LED |

## Construction and first-power procedure

1. Keep the ESP32 antenna end beyond the perfboard edge. Maintain at least 15 mm free of copper, wires, screws, and metal around and below the antenna.
2. Use sockets for the ESP32 and TMC2209. Clearly mark TMC2209 pin 1 and `VM`; inserting a StepStick backward commonly destroys both boards.
3. Keep the 12 V, motor-phase, 5 V, and GND wires short and use 22 AWG wire. Route UART and GPIO wiring away from the motor wires.
4. With all modules and accessories removed, continuity-test every power bus and verify no rail is shorted to ground.
5. Power only the 12 V input and verify the buck output is **5.0 V**. If using an adjustable LM2596, set it before connecting anything.
6. Remove power. Insert the ESP32 and TMC2209 in the marked orientations and fit the TMC heatsink.
7. Find the motor's two coil pairs with an ohmmeter. A coil pair has low resistance; unrelated wires read open. Connect one pair to A1/A2 and the other to B1/B2.
8. Never connect or disconnect the stepper motor while the TMC2209 is powered.
9. Flash `ControlBoard_V4_latest.bin` or build the Control Board source. Do not flash `ESP32-WROOM-32_latest.bin` for this pin map.
10. Initially test at low speed with the mechanism unloaded. Confirm TMC UART communication and check driver/motor temperature before a long run.

## Drawings

- `LTS_Respooler_DIY_Perfboard_Layout.svg` / `.png`: component-side placement and routed net overview.
- `LTS_Respooler_DIY_Wiring_Schematic.svg` / `.png`: electrically authoritative block schematic.

The SVG files are the editable vector originals. The PNG files are generated
previews rendered at the SVGs' native dimensions. To regenerate or verify them
from the repository root:

```sh
make drawings
make drawings-check
```

The renderer is `tools/render_drawings.py` and requires Google Chrome or
Chromium. Set `DRAWING_BROWSER=/path/to/chrome` if it is not available under a
standard executable name. Browser text rendering can vary across operating
systems, so regenerate both previews with the same browser installation.

## Original project references

- [LTS Respooler Pro MakerWorld page](https://makerworld.com/en/models/2301596-lts-respooler-pro-motorized-filament-winder)
- [Original Respooler Pro bill of materials PDF](https://makerworld.bblmw.com/makerworld/model/USc6c25aefa6e12d/design/6dc33f30fc75256f.pdf)
- [Original assembly guide PDF](https://makerworld.bblmw.com/makerworld/model/USc6c25aefa6e12d/design/215e891244bb37a6.pdf)
- [BIGTREETECH TMC2209 V1.2 manual and schematic](https://github.com/bigtreetech/BIGTREETECH-TMC2209-V1.2)
