import os
import yaml
import pathlib

from .environment import *

# def load_environment_from_file(filename):
#     """Utility to initialize a mlonmcu environment from a YAML file."""
#     if isinstance(filename, str):
#         filename = pathlib.Path(filename)
#     with open(filename, encoding="utf-8") as yaml_file:
#         data = yaml.safe_load(yaml_file)
#         if data:
#             if "home" in data:
#                 print(data["home"], filename.parent)
#                 assert os.path.realpath(data["home"]) == os.path.realpath(filename.parent)
#             else:
#                 data["home"] = filename.parent
#             env = Environment(data)
#             return env
#         raise RuntimeError(f"Error opening environment file: {filename}")
#     return None


def create_environment_dict(environment):
    data = {}
    data["home"] = environment.home
    data["logging"] = {
        "level": environment.defaults.log_level.name,
        "to_file": environment.defaults.log_to_file,
    }
    data["paths"] = {
        path: str(path_config.path)
        if isinstance(path_config, PathConfig)
        else [str(config.path) for config in path_config]
        for path, path_config in environment.paths.items()
    }  # TODO: allow relative paths
    data["repos"] = {repo: vars(repo_config) for repo, repo_config in environment.repos.items()}
    data["frameworks"] = {
        "default": environment.defaults.default_framework if environment.defaults.default_framework else None,
        **{
            framework.name: {
                "enabled": framework.enabled,
                "backends": {
                    "default": environment.defaults.default_backends[framework.name]
                    if environment.defaults.default_backends and environment.defaults.default_backends[framework.name]
                    else None,
                    **{
                        backend.name: {
                            "enabled": backend.enabled,
                            "features": {
                                backend_feature.name: backend_feature.supported for backend_feature in backend.features
                            },
                        }
                        for backend in framework.backends
                    },
                },
                "features": {
                    framework_feature.name: framework_feature.supported for framework_feature in framework.features
                },
            }
            for framework in environment.frameworks
        },
    }
    data["frontends"] = {
        # "default": None,  # unimplemented?
        **{
            frontend.name: {
                "enabled": frontend.enabled,
                "features": {
                    frontend_feature.name: frontend_feature.supported for frontend_feature in frontend.features
                },
            }
            for frontend in environment.frontends
        },
    }
    data["platforms"] = {
        # "default": None,  # unimplemented?
        **{
            platform.name: {
                "enabled": platform.enabled,
                "features": {
                    platform_feature.name: platform_feature.supported for platform_feature in platform.features
                },
            }
            for platform in environment.platforms
        },
    }
    data["targets"] = {
        "default": environment.defaults.default_target,
        **{
            target.name: {
                "enabled": target.enabled,
                "features": {target_feature.name: target_feature.supported for target_feature in target.features},
            }
            for target in environment.targets
        },
    }
    data["vars"] = environment.vars
    return data


def write_environment_to_file(environment, filename):
    """Utility to initialize a mlonmcu environment from a YAML file."""
    if isinstance(filename, str):
        filename = pathlib.Path(filename)
    data = create_environment_dict(environment)
    with open(filename, "w") as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False, sort_keys=False)
