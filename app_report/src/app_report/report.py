import re
import pickle
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

    print(pd.DataFrame(df.iloc[:,1:3]).head())

    return df, clusters


def get_failure_plot_data(database):

    df, cause_encoder, substation_encoder = read_df(database)

    failures_by_month = list(df.groupby(by=[settings.COLUMN_YEAR, settings.COLUMN_MONTH]).sum()[settings.COLUMN_FIC])

    causes = list(df.groupby(by=settings.COLUMN_CAUSE).sum()[settings.COLUMN_FIC].index)
    failures_by_causes = list(df.groupby(by=settings.COLUMN_CAUSE).sum()[settings.COLUMN_FIC])

    months = list(df.groupby(by=settings.COLUMN_MONTH).sum()[settings.COLUMN_FIC].index)
    failures_by_months = list(df.groupby(by=settings.COLUMN_MONTH).sum()[settings.COLUMN_FIC])

    substations = list(df.groupby(by=settings.COLUMN_SUBSTATION).sum()[settings.COLUMN_FIC].index)
    failures_by_substation = list(df.groupby(by=settings.COLUMN_SUBSTATION).sum()[settings.COLUMN_FIC])

    features = {
        'causes': {
            'x': causes,
            'y': failures_by_causes,
        },
        'months': {
            'x': months,
            'y': failures_by_months,

        },
        'substations': {
            'x': substations,
            'y': failures_by_substation,

        }

    }

    return failures_by_month, features


def get_validation_plot_data(database):
    db_name = database.split('.')[0]
    df, clusters = read_validation_df(database)
    cl_plot = pickle.loads(open(settings.CLUSTER_FILE.format(db_name, db_name), 'rb').read())

    return clusters, cl_plot


def get_features(database):
    substations, causes, len_tfs, len_db, start_year, end_year, month_range = get_dataset_features(database)

    clusters, cl_plot = get_validation_plot_data(database)

    date_from = f'{month_range[0]}-{start_year}'
    date_until = f'{month_range[-1]}-{end_year}'

    failures_by_month, failures_plot = get_failure_plot_data(database)

    return len_db, len_tfs, failures_by_month, failures_plot, month_range, clusters, cl_plot
