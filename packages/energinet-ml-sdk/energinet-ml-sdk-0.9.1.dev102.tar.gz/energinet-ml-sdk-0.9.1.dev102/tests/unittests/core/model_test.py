import json
import os
import tempfile
from unittest.mock import Mock, patch

import pytest

from energinetml.core.model import Model, TrainedModel
from energinetml.core.project import MachineLearningProject
from energinetml.core.requirements import RequirementList
from tests.constants import (
    COMPUTE_TARGET,
    DATASETS,
    EXPERIMENT,
    FEATURES,
    MODEL_NAME,
    PARAMETERS,
    VM_SIZE,
)


class TestModel:
    def test__project__project_does_not_exists__should_return_none(self, model):
        """
        :param Model model:
        """
        assert model.project is None

    def test__project__project_exists__should_return_project_object(
        self, model_with_project
    ):  # noqa: E501
        """
        :param Model model_with_project:
        """
        assert isinstance(model_with_project.project, MachineLearningProject), type(
            model_with_project.project
        )

    def test__trained_model_path(self, model):
        """
        :param Model model:
        """
        assert model.trained_model_path == os.path.join(
            model.path, "outputs", "model.pkl"
        )

    def test__data_folder_path(self, model):
        """
        :param Model model:
        """
        assert model.data_folder_path == os.path.join(model.path, "data")

    def test__requirements_file_path(self, model):
        """
        :param Model model:
        """
        assert model.requirements_file_path == os.path.join(
            model.path, "requirements.txt"
        )

    def test__datasets_parsed(self, model):
        """
        :param Model model:
        """
        datasets_local = dict(model.datasets_parsed.local)
        datasets_cloud = dict(model.datasets_parsed.cloud)

        assert datasets_local["iris"] is None
        assert datasets_local["local"] == "2"

        assert datasets_cloud["iris"] is None
        assert datasets_cloud["cloud"] == "3"

    def test__requirements__model_has_requirements_file__should_return_model_requirements(  # noqa: E501
        self, model
    ):
        """
        :param Model model:
        """
        with open(os.path.join(model.path, "requirements.txt"), "w") as f:
            f.write("some-package==1.0.0")

        assert isinstance(model.requirements, RequirementList)
        assert "some-package" in model.requirements
        assert model.requirements.get("some-package").specs == [("==", "1.0.0")]

    def test__requirements__model_has_no_requirements_file_but_project_has__should_return_project_requirements(  # noqa: E501
        self, model_with_project
    ):
        """
        :param Model model_with_project:
        """
        assert isinstance(model_with_project.requirements, RequirementList)
        assert (
            model_with_project.requirements is model_with_project.project.requirements
        )

    def test__requirements__no_requirements_exists__should_return_empty_requirements_list(  # noqa: E501
        self, model
    ):
        """
        :param Model model:
        """
        assert isinstance(model.requirements, RequirementList)
        assert model.requirements == []

    @patch("energinetml.core.model.FileMatcher")
    def test__files__should_return_file_matcher_object(self, file_matcher_class, model):
        """
        :param Mock file_matcher_class:
        :param Model model:
        """
        file_matcher_instance = Mock()
        file_matcher_class.return_value = file_matcher_instance

        assert model.files is file_matcher_instance
        file_matcher_class.assert_called_once_with(
            root_path=model.path,
            include=model.files_include,
            exclude=model.files_exclude,
            recursive=True,
        )

    def test__generate_seed(self, model):
        """
        :param Model model:
        """
        assert isinstance(model.generate_seed(), int)
        assert 0 <= model.generate_seed() <= 10 ** 9

    def test__train(self, model):
        """
        :param Model model:
        """
        with pytest.raises(NotImplementedError):
            model.train(datasets=[], logger=None, seed=None)

    def test__predict(self, model):
        """
        :param Model model:
        """
        with pytest.raises(NotImplementedError):
            model.predict(trained_model=None, identifier=None, input_data=None)

    def test__create__should_create_project_files(self):
        with tempfile.TemporaryDirectory() as path:
            project = Model.create(
                path=path,
                name=MODEL_NAME,
                experiment=EXPERIMENT,
                compute_target=COMPUTE_TARGET,
                vm_size=VM_SIZE,
                datasets=DATASETS,
                features=FEATURES,
                parameters=PARAMETERS,
            )

            assert os.path.isfile(os.path.join(project.path, "model.json"))
            assert os.path.isfile(os.path.join(project.path, "model.py"))
            assert os.path.isfile(os.path.join(project.path, "__init__.py"))

            # model.json
            with open(os.path.join(project.path, "model.json")) as f:
                config = json.load(f)
                assert config["name"] == MODEL_NAME
                assert config["experiment"] == EXPERIMENT
                assert config["compute_target"] == COMPUTE_TARGET
                assert config["vm_size"] == VM_SIZE
                assert config["datasets"] == DATASETS
                assert config["features"] == FEATURES
                assert config["parameters"] == PARAMETERS

    def test__as_dict__should_return_object_as_a_dictionary(self, model_with_project):
        return_dict = model_with_project.as_dict()

        assert type(return_dict) == dict
        assert return_dict["name"] == MODEL_NAME
        assert return_dict["experiment"] == EXPERIMENT
        assert return_dict["compute_target"] == COMPUTE_TARGET
        assert return_dict["vm_size"] == VM_SIZE
        assert return_dict["datasets"] == DATASETS
        assert return_dict["features"] == FEATURES
        assert return_dict["parameters"] == PARAMETERS


class TestTrainedModel:
    def test__init_with_both_model_and_models__should_raise_value_error(self):
        with pytest.raises(ValueError):
            TrainedModel(model="x", models={"x": "y"})

    def test__identifiers(self):
        uut = TrainedModel(models={"x": "y", "z": "w"})

        assert uut.identifiers == ["x", "z"]

    def test__has_model(self):
        uut = TrainedModel(models={"x": "y", "z": "w"})

        assert uut.has_model("x")
        assert uut.has_model("z")
        assert not uut.has_model("y")

    def test__get_model__has_default_model(self):
        model = Mock()
        uut = TrainedModel(model=model)

        assert uut.get_model() is model

        with pytest.raises(ValueError):
            uut.get_model("x")

    def test__get_model__has_models(self):
        x = Mock()
        z = Mock()
        uut = TrainedModel(models={"x": x, "z": z})

        assert uut.get_model("x") is x
        assert uut.get_model("z") is z

        with pytest.raises(ValueError):
            uut.get_model()
        with pytest.raises(ValueError):
            uut.get_model("y")

    def test__get_default_model__has_default_model(self):
        model = Mock()
        uut = TrainedModel(model=model)

        assert uut.get_default_model() is model

    def test__get_default_model__has_models(self):
        x = Mock()
        z = Mock()
        uut = TrainedModel(models={"x": x, "z": z})

        with pytest.raises(ValueError):
            uut.get_default_model()

    def test__verify__features_is_not_a_list(self):
        uut = TrainedModel(model="x", features=None)

        with pytest.raises(uut.Invalid):
            uut.verify()

    def test__verify__features_is_not_strings_exclusively(self):
        uut = TrainedModel(model="x", features=["a", "b", 1])

        with pytest.raises(uut.Invalid):
            uut.verify()

    def test__verify__features_are_invalid(self):
        uut = TrainedModel(model="x", features=[" ", " "])

        with pytest.raises(uut.Invalid):
            uut.verify()

    def test__verify__features_are_valid__should_not_raise(self):
        uut = TrainedModel(model="x", features=["a", "b"])

        uut.verify()
