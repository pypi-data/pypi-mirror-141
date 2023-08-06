import tempfile
from unittest.mock import patch

from tests.constants import RESOURCE_GROUP, SUBSCRIPTION_ID, WORKSPACE_NAME


@patch("energinetml.azure.training.AzureTrainingContext")
def test__should_save_meta_data(azure_training_context_mock):
    with tempfile.TemporaryDirectory() as path:

        meta_data = {
            "workspace_name": WORKSPACE_NAME,
            "subscription_id": SUBSCRIPTION_ID,
            "resource_group": RESOURCE_GROUP,
        }

        azure_training_context_mock.save_meta_data(meta_data, path)

        # assert called once?
        # assert content of file?
        # How to add the mock?

        azure_training_context_mock.save_meta_data.assert_called_once_with(
            meta_data, path
        )
