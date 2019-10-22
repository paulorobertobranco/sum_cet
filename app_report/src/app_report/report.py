from app_load.src.app_load.load import get_dataset_features, read_df
import app_home.src.app_home.settings as settings


def get_failure_plot_data(database):

    df, cause_encoder, substation_encoder = read_df(database)
    return list(df.groupby(by=[settings.COLUMN_YEAR, settings.COLUMN_MONTH]).sum()[settings.COLUMN_FIC])


def get_features(database):
    substations, causes, len_tfs, len_db, start_year, end_year, month_range = get_dataset_features(database)

    date_from = f'{month_range[0]}-{start_year}'
    date_until = f'{month_range[-1]}-{end_year}'

    failures = get_failure_plot_data(database)

    return date_from, date_until, failures, month_range