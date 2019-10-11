import pandas as pd
import app_home.src.app_home.settings as settings


def add_failure_to_database(data):
    print(data)

    df = pd.read_csv(settings.INPUT_PATH.format(data['selected_file']))

    tf_row = df[df[settings.COLUMN_TRANSFORMER] == int(data['transformer'])].iloc[0, :]

    new_failure = {
        settings.COLUMN_YEAR: int(data['year']),
        settings.COLUMN_MONTH: data['month'] + '/' + data['year'],
        settings.COLUMN_SUBSTATION: tf_row[settings.COLUMN_SUBSTATION],
        settings.COLUMN_FEEDER: tf_row[settings.COLUMN_FEEDER],
        settings.COLUMN_FEEDER_BLOCK: tf_row[settings.COLUMN_FEEDER_BLOCK],
        settings.COLUMN_TRANSFORMER: int(data['transformer']),
        settings.COLUMN_POTENCY: tf_row[settings.COLUMN_POTENCY],
        'Cod Grupo Causa GPO': 0,
        settings.COLUMN_GROUP_CAUSE: '########',
        'Cod Causa Evento': 0,
        settings.COLUMN_CAUSE: data['cause'],
        settings.COLUMN_DIC: 0.,
        settings.COLUMN_FIC: int(data['fic']),
        'Duração': 0.
    }

    df = df.append(new_failure, ignore_index=True)
    print(df.tail(n=1))


def get_date_ranges(date_df):

    start_year = min(date_df[settings.COLUMN_YEAR].unique())
    end_year = max(date_df[settings.COLUMN_YEAR].unique())

    start_month = min(date_df[date_df[settings.COLUMN_YEAR] == start_year][settings.COLUMN_MONTH])
    end_month = max(date_df[date_df[settings.COLUMN_YEAR] == end_year][settings.COLUMN_MONTH])

    year_range = range(start_year, end_year+1)

    if len(year_range) >= 3:
        month_range = list(range(start_month, 13)) + list(range(1,13)) * (len(year_range)-2) + list(range(1, end_month+1))

    elif len(year_range) == 2:
        month_range = list(range(start_month, 13)) + list(range(1, end_month + 1))
    else:
        month_range = list(range(start_month, end_month + 1))

    return start_year, end_year, month_range


def get_database_features(database):

    extension = database.split('.')[1]
    if extension == 'csv':
        df = pd.read_csv(settings.INPUT_PATH.format(database), usecols=[settings.COLUMN_CAUSE, settings.COLUMN_SUBSTATION, settings.COLUMN_TRANSFORMER, settings.COLUMN_YEAR, settings.COLUMN_MONTH])
        df[settings.COLUMN_MONTH] = (df[settings.COLUMN_MONTH].apply(lambda x: str(x).split('/')[0])).astype('int')
        start_year, end_year, month_range = get_date_ranges(df)

        return df[settings.COLUMN_SUBSTATION].unique(), df[settings.COLUMN_CAUSE].unique(), len(df[settings.COLUMN_TRANSFORMER].unique()), len(df), start_year, end_year, month_range