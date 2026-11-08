from clearml.automation import PipelineController

from pipeline_steps import load_data, train_model, evaluate_models, save_model

def create_pipeline():
    pipeline = PipelineController(
        name="Taxi Fare Prediction Pipeline",
        project="Taxi MLOps",
        version="1.0.0",
    )

    pipeline.add_function_step(
        name="load_data",
        function=load_data,
        function_return=["df"],
        execution_queue="default",
        packages=[
            "boto3>=1.34,<2",
            "pandas>=2.1,<3",
        ],
        docker="python:3.10",
    )


    pipeline.add_function_step(
        name="train_model_1",
        function=train_model,
        function_kwargs={
            "df": "${load_data.df}",
            "n_estimators": 100,
            "learning_rate": 0.05,
        },
        function_return=["model", "X_test", "y_test"],
        parents=["load_data"],
        execution_queue="default",
        packages=[
            "pandas>=2.1,<3",
            "scikit-learn>=1.4,<2",
        ],
        docker="python:3.10",
    )

    pipeline.add_function_step(
        name="train_model_2",
        function=train_model,
        function_kwargs={
            "df": "${load_data.df}",
            "n_estimators": 200,
            "learning_rate": 0.1,
        },
        function_return=["model", "X_test", "y_test"],
        parents=["load_data"],
        execution_queue="default",
        packages=[
            "pandas>=2.1,<3",
            "scikit-learn>=1.4,<2",
        ],
        docker="python:3.10",
    )

    pipeline.add_function_step(
        name="evaluate",
        function=evaluate_models,
        function_kwargs={
            "model_1": "${train_model_1.model}",
            "X_test_1": "${train_model_1.X_test}",
            "y_test_1": "${train_model_1.y_test}",
            "model_2": "${train_model_2.model}",
            "X_test_2": "${train_model_2.X_test}",
            "y_test_2": "${train_model_2.y_test}",
        },
        function_return=[
            "best_model",
            "best_model_name",
            "best_rmse",
        ],
        parents=["train_model_1", "train_model_2"],
        execution_queue="default",
        packages=[
            "scikit-learn>=1.4,<2",
        ],
        docker="python:3.10",
    )

    pipeline.add_function_step(
        name="save_model",
        function=save_model,
        function_kwargs={
            "model": "${evaluate.best_model}",
            "model_name": "best_taxi_model",
        },
        function_return=["model_path"],
        parents=["evaluate"],
        execution_queue="default",
        packages=[
            "boto3>=1.34,<2",
            "joblib>=1.3,<2",
            "scikit-learn>=1.4,<2",
        ],
        docker="python:3.10",
    )
    
    return pipeline


if __name__ == "__main__":
    pipeline = create_pipeline()

    pipeline.start_locally(
        run_pipeline_steps_locally=False,
    )