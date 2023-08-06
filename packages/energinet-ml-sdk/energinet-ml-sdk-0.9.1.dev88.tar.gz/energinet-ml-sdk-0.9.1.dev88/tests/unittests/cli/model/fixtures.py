# Project
import tempfile

import pytest

from energinetml.core.model import Model, TrainedModel
from energinetml.core.project import MachineLearningProject

PROJECT_NAME = "NAME"
SUBSCRIPTION_ID = "SUBSCRIPTION-ID"
RESOURCE_GROUP = "RESOURCE-GROUP"
WORKSPACE_NAME = "WORKSPACE-NAME"
VNET = "VNET"
SUBNET = "SUBNET"


# Model
MODEL_NAME = "NAME"
EXPERIMENT = "EXPERIMENT"
COMPUTE_TARGET = "COMPUTE-TARGET"
VM_SIZE = "VM-SIZE"
DATASETS = ["iris", "hades:2"]
FEATURES = ["feature1", "feature2"]
PARAMETERS = {"param1": "value1", "param2": "value2"}
FILES_INCLUDE = ["file1", "file2"]

# This satisfies SonarCloud
JSON_FILE_NAME = "something.json"
VALID_JSON = '{"valid": "json"}'


@pytest.fixture
def model_path():
    with tempfile.TemporaryDirectory() as path:
        project = MachineLearningProject.create(
            path=path,
            name=PROJECT_NAME,
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            workspace_name=WORKSPACE_NAME,
            vnet_name=VNET,
            subnet_name=SUBNET,
        )

        model_path = project.default_model_path(MODEL_NAME)

        model = Model.create(
            path=model_path,
            name=MODEL_NAME,
            experiment=EXPERIMENT,
            compute_target=COMPUTE_TARGET,
            vm_size=VM_SIZE,
            datasets=DATASETS,
            features=FEATURES,
            parameters=PARAMETERS,
            files_include=FILES_INCLUDE,
        )

        TrainedModel(model="123", params={"asd": 123}, features=FEATURES).dump(
            model.trained_model_path
        )

        yield model_path
