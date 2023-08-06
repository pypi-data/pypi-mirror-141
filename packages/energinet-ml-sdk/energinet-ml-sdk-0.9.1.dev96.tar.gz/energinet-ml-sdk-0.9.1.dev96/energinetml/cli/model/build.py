#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[summary]
"""
import json
import os

import click

from energinetml.core.docker import build_prediction_api_docker_image
from energinetml.core.model import Model
from energinetml.settings import DEFAULT_RELATIVE_ARTIFACT_PATH


@click.command()
@click.option(
    "--tag",
    "-t",
    required=True,
    help="Name and optionally a tag in the `name:tag` format",
)
@click.option(
    "--model-version",
    "model_version",
    required=True,
    type=str,
    help="Model version (used for logging)",
)
@click.option(
    "--artifact-path",
    "artifact_path",
    required=True,
    type=str,
    help="Path to model artifact",
)
def build(tag: str, model_version: str, artifact_path: str) -> None:
    """Build a Docker image with a HTTP web API for model prediction."""
    meta_file_path = (
        f"{artifact_path}/{DEFAULT_RELATIVE_ARTIFACT_PATH}/{Model._META_FILE_NAME}"
    )

    with open(meta_file_path, "r") as f:
        meta = json.load(f)
        model_path = meta["module_name"].replace(".", "/")

    build_prediction_api_docker_image(
        path=f"{artifact_path}/{model_path}",
        trained_model_file_path=os.path.join(
            artifact_path,
            DEFAULT_RELATIVE_ARTIFACT_PATH,
            Model._TRAINED_MODEL_FILE_NAME,
        ),
        model_version=model_version,
        tag=tag,
    )
