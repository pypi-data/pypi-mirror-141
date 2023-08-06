"""MLonMCU ESP32-C3 Target definitions"""

import os
import re
import csv
from pathlib import Path

# from mlonmcu.context import MlonMcuContext
from mlonmcu.logging import get_logger

logger = get_logger()

from .common import cli, execute
from .target import Target
from .metrics import Metrics

from .elf import get_results


class Esp32c3Target(Target):

    FEATURES = []

    DEFAULTS = {
        "timeout_sec": 0,  # disabled
    }

    # REQUIRED = ["espidf.path"]
    REQUIRED = []

    def __init__(self, features=None, config=None, context=None):
        super().__init__("esp32c3", features=features, config=config, context=context)

    @property
    def supported_platforms(self):
        return ["espidf"]

    @property
    def timeout_sec(self):
        return int(self.config["timeout_sec"])

    def get_board_name(self):
        return self.name

    def exec(self, program, *args, cwd=os.getcwd(), **kwargs):
        """Use target to execute a executable with given arguments"""
        if len(args) > 0:
            raise RuntimeError("Program arguments are not supported for real hardware devices")

        assert self.platform is not None, "ESP32 targets needs a platform to execute programs"

        if self.timeout_sec > 0:
            raise NotImplementedError

        # ESP-IDF actually wants a project directory, but we only get the elf now. As a workaround we assume the elf is right in the build directory inside the project directory

        ret = self.platform.run()
        return ret

    def parse_stdout(self, out):
        cpu_cycles = re.search(r"Total Cycles: (.*)", out)
        if not cpu_cycles:
            raise RuntimeError("unexpected script output (cycles)")
        cycles = int(float(cpu_cycles.group(1)))
        cpu_time_us = re.search(r"Total Time: (.*) us", out)
        if not cpu_cycles:
            raise RuntimeError("unexpected script output (time_us)")
        time_us = int(float(cpu_time_us.group(1)))
        return cycles, time_us

    def get_metrics(self, elf, directory, verbose=False):
        if verbose:
            out = self.exec(elf, cwd=directory, live=True)
        else:
            out = self.exec(elf, cwd=directory, live=False, print_func=lambda *args, **kwargs: None)
        cycles, time_us = self.parse_stdout(out)

        metrics = Metrics()
        metrics.add("Total Cycles", cycles)
        metrics.add("Runtime [s]", time_us / 1e6)
        static_mem = get_results(elf)

        rom_ro, rom_code, rom_misc, ram_data, ram_zdata = (
            static_mem["rom_rodata"],
            static_mem["rom_code"],
            static_mem["rom_misc"],
            static_mem["ram_data"],
            static_mem["ram_zdata"],
        )
        rom_total = rom_ro + rom_code + rom_misc
        ram_total = ram_data + ram_zdata
        metrics.add("Total ROM", rom_total)
        metrics.add("Total RAM", ram_total)
        metrics.add("ROM read-only", rom_ro)
        metrics.add("ROM code", rom_code)
        metrics.add("ROM misc", rom_misc)
        metrics.add("RAM data", ram_data)
        metrics.add("RAM zero-init data", ram_zdata)

        return metrics
