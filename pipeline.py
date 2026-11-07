from clearml.automation import PipelineController


def create_pipeline():
    pipeline = PipelineController(
        name="Taxi Fare Prediction Pipeline",
        project="Taxi MLOps",
        version="1.0.0",
    )

    return pipeline


if __name__ == "__main__":
    pipeline = create_pipeline()

    pipeline.start_locally(
        run_pipeline_steps_locally=False,
    )