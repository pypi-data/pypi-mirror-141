from kfp.components import create_component_from_func
from kfp.v2 import dsl
from kfp.v2.dsl import Input, Output, Dataset, Model
from kfp.components import load_component_from_file


def component_func(func, comp_yml_file, pckgs_to_install):

    """
    :param func:
    :type func:
    :param comp_yml_file:
    :type str:
    :param pckgs_to_install:
    :type list:
    :return:  component yaml file
    :rtype: str
    """
    print('func = ', func.__name__)
    print(f'{comp_yml_file} will be generated soon')
    print(f'this component require dependencies: {pckgs_to_install}')
    component = create_component_from_func(func,
                                           output_component_file=comp_yml_file,
                                           packages_to_install=pckgs_to_install)
    operation = load_component_from_file(comp_yml_file)

    return operation


@dsl.component(
    packages_to_install=[
        "pandas",
        "scikit-learn",
        "fsspec",
        "gcsfs"
    ]
)
def train_model(
        training_path: str,
        params: dict,
        label_feature: str,
        sklearn_model: str,
        model_artifact: Output[
            Model
        ],
):
    from datetime import datetime
    import pickle
    import pytz
    import pandas as pd
    from sklearn.utils import all_estimators

    def define_model(mlclass: str,
                     params: dict):
        estimators = all_estimators()
        try:
            for name, ClassifierClass in estimators:
                if mlclass == name:
                    estimator = ClassifierClass(**params)
                    return estimator
        except:
            print(f"package {mlclass} is not within sklearn  list of estimators")

    tz = pytz.timezone("Pacific/Auckland")
    start_timestamp = datetime.now(tz)

    print("Training operation started")

    df = pd.read_csv(training_path, index_col=False)
    x_train = df.drop(label_feature, axis=1)
    y_train = df[[label_feature]]
    model = define_model(sklearn_model, params)  # *LinearRegression(n_jobs=-1)
    model.fit(X=x_train, y=y_train)

    pickle.dump(model, open(model_artifact.path, "wb"))

    end_timestamp = datetime.now(tz)
    # Add metadata
    model_artifact.metadata["start_datetime"] = str(start_timestamp)
    model_artifact.metadata["end_datetime"] = str(end_timestamp)

    print("Training operation completed")


@dsl.component(packages_to_install=["google-cloud-aiplatform"])
def upload_model(
        model_artifact: Input[Model],
        project: str,
        location: str,
        display_name: str,
        artifact_uri: str,
        serving_container_image_uri: str,
        labels: dict,
):
    from google.cloud import aiplatform
    from google.cloud import storage

    print("Upload operation started")

    # Upload artifact
    storage_client = storage.Client()
    artifact_bucket = artifact_uri[5:].split("/")[0]
    artifact_path = artifact_uri[5:].split("/", 1)[1]
    bucket = storage_client.bucket(artifact_bucket)
    blob = bucket.blob(f"{artifact_path}/model.pkl")
    blob.upload_from_filename(model_artifact.path)

    labels["version"] = labels["version"].replace(".", "-")

    aiplatform.init(project=project, location=location)
    model = aiplatform.Model.upload(
        display_name=display_name,
        artifact_uri=artifact_uri,
        serving_container_image_uri=serving_container_image_uri,
        labels=labels,
    )
    model.wait()

    print("Upload operation completed")
    print(model.display_name)
    print(model.resource_name)


@dsl.component(packages_to_install=["requests"])
def send_metadata(
        model_metadata: dict,
        training_dataset: Input[Dataset],
        model_artifact: Input[Model],
        model_registry_uri: str,
        model_type: str,
):
    import requests

    metadata = {
        **model_metadata,
        **training_dataset.metadata,
        **model_artifact.metadata,
    }
    requests.post(
        f"{model_registry_uri}/api/{model_type}/metadata",
        data=metadata,
    )
