"""MLonMCU Target definitions"""

import os
import tempfile
import time
from pathlib import Path
from typing import List


# from mlonmcu.context import MlonMcuContext
from mlonmcu.config import filter_config
from mlonmcu.feature.feature import Feature
from mlonmcu.feature.type import FeatureType
from mlonmcu.feature.features import get_matching_features
from mlonmcu.artifact import Artifact, ArtifactFormat


# TODO: class TargetFactory:
from .common import execute
from .metrics import Metrics
from .elf import get_results


class Target:
    """Base target class

    Attributes
    ----------
    name : str
        Default name of the target
    features : list
        List of target features which should be enabled
    config : dict
        User config defined via key-value pairs
    inspect_program : str
        Program which can be used to inspect executables (i.e. readelf)
    inspect_program_args : list
        List of additional arguments to the inspect_program
    env : os._Environ
        Optinal map of environment variables
    context : MlonMcuContext
        Optional context for resolving dependency paths
    """

    FEATURES = []
    DEFAULTS = {}
    REQUIRED = []

    def __init__(
        self,
        name: str,
        features: List[Feature] = None,
        config: dict = None,
        context=None,
    ):
        self.name = name
        self.config = config if config else {}
        self.features = self.process_features(features)
        self.config = filter_config(self.config, self.name, self.DEFAULTS, self.REQUIRED)
        self.inspect_program = "readelf"
        self.inspect_program_args = ["--all"]
        self.env = os.environ
        self.context = context
        self.artifacts = []
        self.platform = None

    def add_platform(self, platform):
        self.platform = platform

    @property
    def supported_platforms(self):
        return ["mlif"]

    def __repr__(self):
        return f"Target({self.name})"

    def process_features(self, features):
        if features is None:
            return []
        features = get_matching_features(features, FeatureType.TARGET)
        for feature in features:
            assert feature.name in self.FEATURES, f"Incompatible feature: {feature.name}"
            feature.add_target_config(self.name, self.config)
        return features

    def exec(self, program: Path, *args, **kwargs):
        """Use target to execute a executable with given arguments"""
        raise NotImplementedError

    def inspect(self, program: Path, *args, **kwargs):
        """Use target to inspect a executable"""
        return execute(self.inspect_program, program, *self.inspect_program_args, *args, **kwargs)

    def get_metrics(self, elf, directory, verbose=True):
        # This should not be accurate, just a fallback which should be overwritten
        start_time = time.time()
        if verbose:
            out = self.exec(elf, cwd=directory, live=True)
        else:
            out = self.exec(elf, cwd=directory, live=False, print_func=lambda *args, **kwargs: None)
        # TODO: do something with out?
        end_time = time.time()
        diff = end_time - start_time
        # size instead of readelf?
        metrics = Metrics()
        metrics.add("Runtime [s]", diff)

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

    def generate_metrics(self, elf, verbose=False):
        artifacts = []
        with tempfile.TemporaryDirectory() as temp_dir:
            metrics = self.get_metrics(elf, temp_dir, verbose=verbose)
            content = metrics.to_csv(include_optional=True)  # TODO: store df instead?
            artifact = Artifact("metrics.csv", content=content, fmt=ArtifactFormat.TEXT)
            # Alternative: artifact = Artifact("metrics.csv", data=df/dict, fmt=ArtifactFormat.DATA)
            artifacts.append(artifact)
        self.artifacts = artifacts

    def export_metrics(self, path):
        assert len(self.artifacts) > 0, "No artifacts found, please run generate_metrics() first"

        if not isinstance(path, Path):
            path = Path(path)

        is_dir = len(path.suffix) == 0
        if is_dir:
            assert (
                path.is_dir()
            ), "The supplied path does not exists."  # Make sure it actually exists (we do not create it by default)
            for artifact in self.artifacts:
                artifact.export(path)
        else:
            raise NotImplementedError

    def get_target_system(self):
        return self.name

    def get_cmake_args(self):
        target_system = self.get_target_system()
        return [f"-DTARGET_SYSTEM={target_system}"]

    def get_arch(self):
        raise NotImplementedError

    def get_required_cache_flags(self):
        ret = {}

        ret["cmsisnn.lib"] = [
            self.get_arch()
        ]  # TODO: this should be handled differently (Target arch specific libs), maybe via features or wildcards, boolean flag?
        return ret
