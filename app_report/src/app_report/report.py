import re
import pandas as pd
from app_load.src.app_load.load import get_dataset_features, read_df
import app_home.src.app_home.settings as settings


def read_validation_df(database):
    db_name = database.split('.')[0]

    df = pd.read_csv(settings.VALIDATION_FILE.format(db_name, db_name), sep='\t')
    clusters = df['cluster'].unique()

    df['failure_probabilities'] = df['failure_probabilities'].apply(lambda x: list(map(float, re.findall(r'[\d\.\d]+', x))))
    df['true_labels'] = df['true_labels'].apply(lambda x: list(map(float, re.findall(r'[\d\.\d]+', x))))
    df['transformers'] = df['transformers'].apply(lambda x: list(map(int, re.findall(r'[\d\.\d]+', x))))
    df['cluster'] = df['cluster'].apply(lambda x: re.split(', ', x))
    return df, clusters


def get_failure_plot_data(database):

    df, cause_encoder, substation_encoder = read_df(database)

    failures_by_month = list(df.groupby(by=[settings.COLUMN_YEAR, settings.COLUMN_MONTH]).sum()[settings.COLUMN_FIC])

    causes = list(df.groupby(by=settings.COLUMN_CAUSE).sum()[settings.COLUMN_FIC].index)
    failures_by_causes = list(df.groupby(by=settings.COLUMN_CAUSE).sum()[settings.COLUMN_FIC])

    return causes, failures_by_causes, failures_by_month


def get_validation_plot_data(database):
    df, clusters = read_validation_df(database)
    print(df['cluster'][0])
    return clusters


def get_features(database):
    substations, causes, len_tfs, len_db, start_year, end_year, month_range = get_dataset_features(database)

    clusters = get_validation_plot_data(database)

    date_from = f'{month_range[0]}-{start_year}'
    date_until = f'{month_range[-1]}-{end_year}'

    causes, failures_by_causes, failures_by_month = get_failure_plot_data(database)

    return len_db, len_tfs, causes, failures_by_causes, failures_by_month, month_range, clusters
