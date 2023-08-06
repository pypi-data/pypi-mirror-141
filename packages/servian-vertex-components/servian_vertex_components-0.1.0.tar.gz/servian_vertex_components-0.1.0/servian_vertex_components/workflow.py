import yaml
from datetime import datetime
from google.cloud import aiplatform


class workflow:
    def __init__(self, metadata_file="metadata.yaml"):
        """

        :type metadata_file: str
        """
        metadata = self.load_metadata(metadata_file)
        self.ENV = "experiment"
        self.MODEL_VERSION = datetime.now().strftime("%Y%m%d%H%M%S")

        # Imported from metadata.yaml
        self.MODEL_ID = metadata["model"]["id"]
        self.MODEL_NAME = metadata["model"]["name"]
        self.MODEL_TYPE = metadata["model"]["type"]
        self.TRAINING_IMAGE = metadata["training"]["image"]
        self.PREDICTION_IMAGE = metadata["prediction"]["image"]
        self.GCP_PROJECT_ID = metadata[self.ENV]["gcp_project_id"]
        self.GCP_REGION = metadata[self.ENV]["gcp_region"]
        self.GCS_BUCKET = metadata[self.ENV]["gcs_bucket"]
        self.SERVICE_ACCOUNT = metadata[self.ENV]["service_account"]
        self.MODEL_REGISTRY_URI = metadata[self.ENV]["model_registry_uri"]

        self.pipeline_name = f"train-{self.MODEL_NAME}"
        self.pipeline_id = f"{self.pipeline_name}-{self.MODEL_VERSION}".replace(".", "-")
        self.pipeline_root = f"{self.GCS_BUCKET}/models/{self.MODEL_NAME}/{self.MODEL_VERSION}/pipeline_root"
        self.model_artifact_uri = f"{self.GCS_BUCKET}/models/{self.MODEL_NAME}/{self.MODEL_VERSION}/artifacts"
        self.model_display_name = f"{self.MODEL_NAME}_{self.MODEL_VERSION}"

        self.model_metadata = {
                "environment": self.ENV,
                "model_id": self.MODEL_ID,
                "version": self.MODEL_VERSION,
                "pipeline_id": self.pipeline_id,
                            }
        aiplatform.init(project=self.GCP_PROJECT_ID, staging_bucket=self.GCS_BUCKET)

    @staticmethod
    def load_metadata(file_path="metadata.yaml"):
        with open(f"../{file_path}") as f:
            metadata = yaml.load(f, Loader=yaml.FullLoader)
        return metadata
