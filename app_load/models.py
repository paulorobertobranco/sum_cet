from django.db import models
from os import listdir
import pandas as pd
from os.path import isfile
from typing import List, Text

INPUT_PATH = 'input_files/{}'


class Database:

    def __init__(self, filename):
        name, extension = filename.split(".")
        self.__filename = filename
        self.__name = name
        self.__extension = extension

    def __str__(self):
        return self.db_name

    @property
    def filename(self):
        return self.__filename

    @property
    def name(self):
        return self.__name

    @property
    def extension(self):
        return self.__extension

    def __read_df(self):

        input_filename = settings.INPUT_PATH.format(filename)

        df = pd.read_csv(input_filename)
        df[settings.COLUMN_MONTH] = (df[settings.COLUMN_MONTH].apply(lambda x: str(x).split('/')[0])).astype('float')
        df.sort_values(by=[settings.COLUMN_TRANSFORMER, settings.COLUMN_YEAR, settings.COLUMN_MONTH], inplace=True)
        df.reset_index(drop=True, inplace=True)

        cause_encoder = LabelEncoder().fit(df[settings.COLUMN_CAUSE])
        substation_encoder = LabelEncoder().fit(df[settings.COLUMN_SUBSTATION])

        df[settings.COLUMN_SUBSTATION_ENCODER] = substation_encoder.transform(df[settings.COLUMN_SUBSTATION])
        df[settings.COLUMN_CAUSE_ENCODER] = cause_encoder.transform(df[settings.COLUMN_CAUSE])

        return df, cause_encoder, substation_encoder

    @staticmethod
    def list_inputs() -> List[Text]:

        """
        List database (.csv, .xlsx) file names located in dir '/input_files/'.

        :return:
            input_file_list: List[Text]
                A list of input files names (.csv, .xlsx) located in dir '/input_files/'.

        """

        input_files = [f for f in listdir(INPUT_PATH.format('')) if isfile(INPUT_PATH.format(f)) and
                       (f.endswith('.csv') or f.endswith('.xlsx'))]

        return input_files

    def date_ranges(date_df):

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


# TEST

if __name__ == '__main__':
    db = Database('test.csv')
    print(db.filename)
    print(db.name)
