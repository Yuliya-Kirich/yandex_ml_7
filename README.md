# MLOps-пайплайн для сервиса-агрегатора такси

Проект модуля 7 курса MLOps Яндекс Практикума.

## Цель проекта

Разработать воспроизводимый ML-пайплайн для обработки данных о поездках такси, обучения нескольких моделей, оценки их качества и сохранения лучшей модели.

## Используемые технологии

- **Apache Airflow** - оркестрация обработки данных по расписанию.
- **Pandera** - валидация данных.
- **Yandex Object Storage (S3)** - хранение датасетов и моделей.
- **ClearML** - управление ML-экспериментами и пайплайнами.
- **ClearML Agents** - выполнение задач обучения.
- **Kubernetes (K3s) и Helm** - управление агентами.
- **Docker Compose** - развёртывание инфраструктуры.
- **Python, pandas, scikit-learn, boto3, joblib** - обработка данных и машинное обучение.

## Структура проекта

```text
.
├── dags/
│   ├── final_task_dag.py
│   └── taxi_schema.py
├── pipeline.py
├── pipeline_steps.py
├── train_model.py
├── requirements.txt
└── README.md
```

## Обработка данных в Airflow

DAG `final_task_dag` запускается каждый час.

**Основные этапы:**

1. Загрузка исходного датасета из объектного хранилища.
2. Очистка и преобразование данных.
3. Проверка структуры данных с помощью Pandera.
4. Сохранение обработанного датасета в объектное хранилище.

## ML-пайплайн в ClearML

Пайплайн состоит из пяти этапов:

1. `load_data` - загрузка обработанных данных.
2. `train_model_1` - обучение первой модели.
3. `train_model_2` - обучение второй модели.
4. `evaluate` - сравнение моделей по RMSE.
5. `save_model` - сохранение лучшей модели.

Используется алгоритм `GradientBoostingRegressor` с двумя наборами гиперпараметров.

| Параметр | Модель 1 | Модель 2 |
|---|---|---|
| `n_estimators` | 100 | 200 |
| `learning_rate` | 0.05 | 0.1 |

Обучение выполняется через два ClearML Agent, развёрнутых в Kubernetes.

## Хранение артефактов

Для хранения используется S3-совместимое объектное хранилище.

**Логическая структура:**

```text
raw/
    uber.csv
processed/
    uber_processed.csv
models/
    best_taxi_model.joblib
```

Учётные данные и секретные ключи не публикуются в репозитории.

## Результаты

- Реализована обработка данных по расписанию в Airflow.
- Настроена валидация данных через Pandera.
- Получен обработанный датасет из **199 256 строк**.
- Успешно выполнены все пять этапов ClearML Pipeline.
- Обучены две модели и проведено сравнение по RMSE.
- Лучшая модель сохранена в S3 в формате Joblib.

## Запуск

Для запуска необходимы настроенные Airflow, ClearML Server, ClearML Agents и доступ к объектному хранилищу.

**Установка зависимостей:**

```bash
pip install -r requirements.txt
```

**Запуск ML-пайплайна:**

```bash
python pipeline.py
```

Перед запуском необходимо настроить доступ к ClearML и объектному хранилищу. Секреты хранятся вне публичного Git-репозитория.

## Скриншоты выполнения

1. Интерфейсы Airflow и ClearML.
![Airflow.png](screenshots%2FAirflow.png)
![ClearML_HOME.png](screenshots%2FClearML_HOME.png)

3. Активных ClearML Agents.
![clearml-agents.png](screenshots%2Fclearml-agents.png)

3. Успешного выполнения DAG в Airflow.
![airflow-dag.png](screenshots%2Fairflow-dag.png)

4. Завершённого ML-пайплайна в ClearML.
![clearml-pipeline.png](screenshots%2Fclearml-pipeline.png)

5. Параллельного обучения моделей.
Обе модели запускались одновременно на разных ClearML Workers.
![parallel-training1.png](screenshots%2Fparallel-training1.png)
![parallel-training2.png](screenshots%2Fparallel-training2.png)

6. Выбора лучшей модели.
![best-model.png](screenshots%2Fbest-model.png)

7. Сохранённого артефакта в S3.
![s3-model.png](screenshots%2Fs3-model.png)