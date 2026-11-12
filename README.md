# ⚙️🧵 Welcome to the LTS Respooler GitHub! 🧵⚙️

The LTS Respooler is a compact and slightly over-engineered filament Respooler optimized for Bambu Lab spools. It integrates a filament runout sensor and wireless app-connectivity for ease of use. The LTS Respooler Pro uses a 9g servo motor to precisely position the Filament Guide. You can find all the files related to it here. That includes the raw .txt ESP32 Code, the .bin firmware files and the PCB Gerber files.

## ➡️ Upcoming features and files:

- Official attachment for spools bigger than 1 kg

## 🚀 Getting started

- All the 3D files can be downloaded and printed from [MakerWorld](https://makerworld.com/@lukas.tu)
- Assembly Intructions and the Needed Hardware PDF can also be found there
- Most of the Hardware can be ordered from Bambu Lab's Maker's Supply
- PCBs can be ordered from my [Website](https://lts-design.com) or on [PCBWay](https://www.pcbway.com/project/member/?bmbno=7102E4BB-3522-48)
- Flash the newest firmware version to your ESP32 or LTS Control Board using the [Web Flasher](https://flash.lts-design.com)

## Firmware development

This repository is a VS Code/PlatformIO project. It supports the two current
firmware targets:

| PlatformIO environment | Hardware | Firmware source |
| --- | --- | --- |
| `control_board_v4` (default) | LTS Control Board V4/V4.1, ESP32-S3-WROOM-1 | `Firmware/(.txt) Control Board Code` |
| `driver_board_v1` | LTS Driver Board V1, ESP32-WROOM-32 | `Firmware/(.txt) Driver Board Code` |

Install [VS Code](https://code.visualstudio.com/) and the recommended
[PlatformIO IDE extension](https://platformio.org/install/ide?install=vscode),
then open the repository directory. The included VS Code tasks can build either
board without any machine-specific paths.

From a terminal:

```sh
make                 # show available targets
make build           # build the Control Board V4 firmware
make driver          # build the Driver Board V1 firmware
make build-all       # build both
make upload          # flash the control board (auto-detect the serial port)
make upload ENV=driver_board_v1 PORT=/dev/ttyUSB0
make monitor
```

PlatformIO downloads the pinned ESP32 platform and library versions on the
first build. Build products are under `.pio/build/<environment>/`:

- `firmware.bin` is the application-only image for OTA/web updates.
- `firmware.factory.bin` is the combined image for programming a blank board.

Use `make ota-bin` or `make factory-bin` to copy a clearly named image into the
ignored `dist/` directory. These targets do not replace the published release
binaries in `Firmware/`.

The repository previously contained only raw Arduino sketch text and released
`.bin` files; it had no Arduino project, dependency manifest, or build command.
The small C++ entry points in `src/` supply the function declarations that the
Arduino IDE normally generates and include those original sketches unchanged.
See [Firmware/README.md](Firmware/README.md) for board and flash details.

## 📋 License

This project is licensed under the MIT license, giving you the freedom to use it however you like. Contributions, modifications, and improvements are very welcome! :)
