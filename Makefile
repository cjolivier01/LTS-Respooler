SHELL := /bin/bash

TOPDIR := $(shell pwd)
COMPILE_COMMANDS := compile_commands.json

PIO ?= pio
PIO_BIN := $(shell command -v $(PIO) 2>/dev/null)
PIO_SHEBANG := $(shell if [ -n "$(PIO_BIN)" ]; then sed -n '1s/^#!//p' "$(PIO_BIN)" 2>/dev/null; fi)
PIO_PYTHON ?= $(if $(PIO_SHEBANG),$(PIO_SHEBANG),python3)
ENV ?= control_board_v4
ACTIVE_ENVS ?= control_board_v4 driver_board_v1
DETECTED_PORT := $(shell $(PIO_PYTHON) "$(TOPDIR)/tools/find_esp32_port.py" 2>/dev/null)
PORT ?= $(DETECTED_PORT)
BAUD ?= 115200
PIO_ARGS ?=
MONITOR_ARGS ?= --echo

define with_port
port="$(PORT)"; \
if [ -z "$$port" ]; then \
	printf 'No ESP32 serial port detected. Run "make ports" or set PORT=/dev/tty...\n' >&2; \
	exit 2; \
fi; \
printf 'Using port %s\n' "$$port"; \
$(1)
endef

all: help

.PHONY: all help bld build control driver build-all upload monitor upload-monitor ports clean distclean erase check compiledb ota-bin factory-bin drawings drawings-check FORCE

bld build:
	$(PIO) run -e $(ENV) $(PIO_ARGS)

control:
	$(PIO) run -e control_board_v4 $(PIO_ARGS)

driver:
	$(PIO) run -e driver_board_v1 $(PIO_ARGS)

build-all:
	$(PIO) run $(foreach env,$(ACTIVE_ENVS),-e $(env)) $(PIO_ARGS)

upload:
	@$(call with_port,exec $(PIO) run -e $(ENV) -t upload --upload-port "$$port" $(PIO_ARGS))

monitor:
	@$(call with_port,exec $(PIO) device monitor --port "$$port" --baud $(BAUD) $(MONITOR_ARGS))

upload-monitor: upload monitor

ports:
	$(PIO) device list
	@printf '\nPreferred ESP32 port: '
	@$(PIO_PYTHON) "$(TOPDIR)/tools/find_esp32_port.py" || printf '(none detected)\n'

clean:
	$(PIO) run -e $(ENV) -t clean

distclean:
	@case "$(ENV)" in control_board_v4|driver_board_v1) ;; \
		*) printf 'Refusing to remove an unknown environment: %s\n' "$(ENV)" >&2; exit 2 ;; \
	esac
	rm -rf "$(TOPDIR)/.pio/build/$(ENV)"

erase:
	@$(call with_port,exec $(PIO) run -e $(ENV) -t erase --upload-port "$$port" $(PIO_ARGS))

check:
	$(PIO) check -e $(ENV) $(PIO_ARGS)

compiledb: $(COMPILE_COMMANDS)

$(COMPILE_COMMANDS): FORCE
	$(PIO) run -e $(ENV) -t compiledb $(PIO_ARGS)
	@if [ ! -f "$(TOPDIR)/$(COMPILE_COMMANDS)" ]; then \
		db="$$(find "$(TOPDIR)/.pio/build/$(ENV)" -name compile_commands.json -print -quit)"; \
		if [ -n "$$db" ]; then cp "$$db" "$(TOPDIR)/$(COMPILE_COMMANDS)"; fi; \
	fi
	@test -f "$(TOPDIR)/$(COMPILE_COMMANDS)" || { printf 'Failed to generate %s.\n' "$(COMPILE_COMMANDS)" >&2; exit 1; }

# Copy the app-only binary used by OTA/web flashing without replacing a release.
ota-bin: build
	@mkdir -p "$(TOPDIR)/dist"
	cp "$(TOPDIR)/.pio/build/$(ENV)/firmware.bin" "$(TOPDIR)/dist/$(ENV)_OTA.bin"
	@printf 'Created dist/%s_OTA.bin\n' "$(ENV)"

# Copy the combined bootloader + partition table + app image for a blank board.
factory-bin: build
	@mkdir -p "$(TOPDIR)/dist"
	cp "$(TOPDIR)/.pio/build/$(ENV)/firmware.factory.bin" "$(TOPDIR)/dist/$(ENV)_factory.bin"
	@printf 'Created dist/%s_factory.bin\n' "$(ENV)"

drawings:
	python3 "$(TOPDIR)/tools/render_drawings.py"

drawings-check:
	python3 "$(TOPDIR)/tools/render_drawings.py" --check

help:
	@printf '%s\n' \
		'Available make targets:' \
		'' \
		'Build and flash' \
		'---------------' \
		'build           Build ENV (default: control_board_v4).' \
		'bld             Alias for build.' \
		'control         Build the ESP32-S3 Control Board V4 firmware.' \
		'driver          Build the ESP32 Driver Board V1 firmware.' \
		'build-all       Build both supported boards.' \
		'upload          Flash ENV, auto-detecting PORT when possible.' \
		'monitor         Open the 115200-baud serial monitor.' \
		'upload-monitor  Flash ENV, then open its serial monitor.' \
		'ports           List serial devices and the preferred port.' \
		'ota-bin         Copy ENV app binary to dist/ENV_OTA.bin.' \
		'factory-bin     Copy a complete blank-board image to dist/.' \
		'drawings        Render the perfboard SVG sources to PNG.' \
		'drawings-check  Verify the checked-in PNG drawings are current.' \
		'' \
		'Maintenance' \
		'-----------' \
		'clean           Run PlatformIO clean for ENV.' \
		'distclean       Remove only .pio/build/ENV.' \
		'erase           Erase ENV board flash.' \
		'check           Run PlatformIO static analysis for ENV.' \
		'compiledb       Generate root compile_commands.json.' \
		'' \
		'Variables' \
		'---------' \
		'ENV             control_board_v4 (default) or driver_board_v1.' \
		'PORT            Upload/monitor port; auto-detected when unset.' \
		'BAUD            Monitor baud rate (default: 115200).' \
		'PIO             PlatformIO executable (default: pio).' \
		'PIO_ARGS        Extra arguments passed to PlatformIO.' \
		'MONITOR_ARGS    Extra monitor arguments (default: --echo).'

FORCE:
