
INPUT_PATH = 'input_files/{}'
RESULT_PATH = 'processed_files/{}'
DAT_PATH = RESULT_PATH + '/dat/'
CLUSTER_PATH = RESULT_PATH + '/cluster/'
VALIDATION_PATH = RESULT_PATH + '/validation/'
PLOT_PATH = RESULT_PATH + '/plots/'
MODEL_PATH = RESULT_PATH + '/model/'

DAT_FILE = DAT_PATH + '{}.dat'
PLOT_FILE = PLOT_PATH + 'cluster_{}.png'
MODEL_FILE = MODEL_PATH + 'model_{}_cluster_{}.dat'
VALIDATION_FILE = VALIDATION_PATH + 'validation_{}.csv'

############# INPUT DATASET #############

COLUMN_YEAR = 'Ano Evento'
COLUMN_MONTH = 'Mês Evento'
COLUMN_SUBSTATION = 'Subestação Hier.Geoelétrica'
COLUMN_SUBSTATION_ENCODER = 'sub_encoder'
COLUMN_TRANSFORMER = 'Transformador Hier.Geoelétrica'
COLUMN_POTENCY = 'Pot'
COLUMN_GROUP_CAUSE = 'Grupo Causa GPO'
COLUMN_CAUSE = 'Causa Evento'
COLUMN_CAUSE_ENCODER = 'cause_encoder'
COLUMN_FIC = 'FIC Transformador'
COLUMN_DIC = 'DIC Transformador'
COLUMN_FEEDER = 'Alimentador Hier.Geoelétrica'
COLUMN_FEEDER_BLOCK = 'Bloco Alimentador Hier.Geoelétrica'

COLUMNS = [COLUMN_YEAR, COLUMN_MONTH, COLUMN_SUBSTATION, COLUMN_TRANSFORMER,
           COLUMN_POTENCY, COLUMN_CAUSE, COLUMN_FIC, COLUMN_FEEDER_BLOCK,
           COLUMN_FEEDER, COLUMN_GROUP_CAUSE]

#########################################

############# DAT DATAFRAME #############

DAT_COLUMN_YEAR = 'year'
DAT_COLUMN_MONTH = 'month'
DAT_COLUMN_SUBSTATION = 'substation'
DAT_COLUMN_POTENCY = 'potency'
DAT_COLUMN_TRANSFORMER = 'transformer'
DAT_COLUMN_CAUSE = 'cause'
DAT_COLUMN_LTM = 'last_three_months'
DAT_COLUMN_FG = 'failure_gap'
DAT_COLUMN_FC = 'failure_count'
DAT_COLUMN_MAT = 'mean_active_time'
DAT_COLUMN_LABEL = 'label'
DAT_COLUMN_FIC = 'fic'

#########################################