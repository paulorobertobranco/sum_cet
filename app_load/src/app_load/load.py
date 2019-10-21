import pickle
import numpy as np
import pandas as pd
from os import mkdir
from os import listdir
from os.path import isfile
from sklearn.svm import SVC
from collections import defaultdict
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
import app_home.src.app_home.settings as settings
from sklearn.cluster import AgglomerativeClustering
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


def list_input_files():

    input_files = [f for f in listdir(settings.INPUT_PATH.format('')) if isfile(settings.INPUT_PATH.format(f)) and
                   (f.endswith('.csv') or f.endswith('.xlsx'))]

    loaded_input_files = [f for f in input_files if
                          isfile(settings.DAT_FILE.format(f.split('.')[0], f.split('.')[0]))]

    not_loaded_input_files = [f for f in input_files if f not in loaded_input_files]

    return loaded_input_files, not_loaded_input_files


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


def get_dataset_features(database):

    extension = database.split('.')[1]
    if extension == 'csv':
        df = pd.read_csv(settings.INPUT_PATH.format(database), usecols=[settings.COLUMN_CAUSE, settings.COLUMN_SUBSTATION, settings.COLUMN_TRANSFORMER, settings.COLUMN_YEAR, settings.COLUMN_MONTH])
        df[settings.COLUMN_MONTH] = (df[settings.COLUMN_MONTH].apply(lambda x: str(x).split('/')[0])).astype('int')
        start_year, end_year, month_range = get_date_ranges(df)

    return df[settings.COLUMN_SUBSTATION].unique(), df[settings.COLUMN_CAUSE].unique(), len(df[settings.COLUMN_TRANSFORMER].unique()), len(df), start_year, end_year, month_range


def read_df(filename):

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


def compute_features(tf, tf_rows, start_year, month_range):

    real_serie = []
    gap_since_last_failure = []
    failure_count = []
    mean_active_time = []

    gap = 0
    count = 0
    active_time_list = [1]

    for m in month_range:
        mean_active_time.append(np.mean(active_time_list))
        failure_count.append(float(count))
        gap_since_last_failure.append(gap)

        if tf_rows[(tf_rows[settings.COLUMN_MONTH] == m) & (tf_rows[settings.COLUMN_YEAR] == start_year)].empty:
            gap += 1.
            real_serie.append(0.)
            active_time_list[-1] += 1.
        else:
            gap = 0.
            if active_time_list[-1] != 0:
                active_time_list.append(0.)
            count += tf_rows[(tf_rows[settings.COLUMN_MONTH] == m) & (tf_rows[settings.COLUMN_YEAR] == start_year)][
                settings.COLUMN_FIC].sum()
            real_serie.append(
                tf_rows[(tf_rows[settings.COLUMN_MONTH] == m) & (tf_rows[settings.COLUMN_YEAR] == start_year)][settings.COLUMN_FIC].sum())

        if m == 12:
            start_year += 1

    target_serie = []
    three_mf = []

    for i, j in enumerate(real_serie):
        try:
            if not any(real_serie[i + 1:i + 4]):
                target_serie.append(0.)
            else:
                target_serie.append(1.)
        except:
            try:
                if not any(real_serie[i + 1:]):
                    target_serie.append(0.)
                else:
                    target_serie.append(1.)
            except:
                target_serie.append(0.)

        try:
            if not any(real_serie[i - 2:i + 1]):
                three_mf.append(0.)
            else:
                three_mf.append(np.sum(real_serie[i - 2:i + 1]))
        except:
            if not any(real_serie[tf][:i]):
                three_mf.append(0.)
            else:
                three_mf.append(np.sum(real_serie[i - 2:i + 1]))

    return real_serie, gap_since_last_failure, failure_count, three_mf, mean_active_time, target_serie


def save_dat_file(df, output, start_year, month_range):

    computed_features_by_cause = {}

    for g in df[settings.COLUMN_CAUSE_ENCODER].unique():

        df_computed_features = defaultdict(list)
        g_rows = df[df[settings.COLUMN_CAUSE_ENCODER] == g]

        for tf in g_rows[settings.COLUMN_TRANSFORMER].unique():

            tf_rows = g_rows[g_rows[settings.COLUMN_TRANSFORMER] == tf]

            df_computed_features['tf'] += [tf_rows[settings.COLUMN_TRANSFORMER].iloc[0]] * len(month_range)
            df_computed_features['substation'] += [tf_rows[settings.COLUMN_SUBSTATION_ENCODER].iloc[0]] * len(month_range)
            df_computed_features['pot'] += [tf_rows[settings.COLUMN_POTENCY].iloc[0]] * len(month_range)
            df_computed_features['month'] += month_range

            real_serie, failure_gap, failure_count, three_month, mean_active_time, label_serie = compute_features(tf, tf_rows, start_year, month_range)

            df_computed_features['3months_failure'] += three_month
            df_computed_features['failure_gap'] += failure_gap
            df_computed_features['failure_count'] += failure_count
            df_computed_features['mean_active_time'] += mean_active_time
            df_computed_features['label'] += label_serie

        for c in df_computed_features.keys():
            df_computed_features[c] = np.float_(df_computed_features[c])

        computed_features_by_cause[g] = pd.DataFrame(df_computed_features)

    open(output, 'wb').write(pickle.dumps(computed_features_by_cause))

    return computed_features_by_cause


def get_train_dat_file(dat_df, train_size):

    dat_df_train = {}

    for cause in dat_df.keys():
        dat_df_train[cause] = pd.DataFrame(columns=dat_df[cause].columns)
        for tf in dat_df[cause]['tf'].unique():
            tf_rows = dat_df[cause][dat_df[cause]['tf'] == tf]
            dat_df_train[cause] = dat_df_train[cause].append(tf_rows.iloc[2:train_size, :])

    return dat_df_train


def get_correlations(dat_df_train):

    corr_label = {}
    for cause_encoder_id in dat_df_train.keys():
        corr = dat_df_train[cause_encoder_id].corr()

        corr_label[cause_encoder_id] = corr.iloc[1:-1, -1]

    return pd.DataFrame(corr_label).T.replace(np.nan, 0)


def get_clusters(correlation_df, output, pca_comp=2, n_clusters=3):

    pca_fit = PCA(n_components=pca_comp).fit(correlation_df)
    pca = pca_fit.transform(correlation_df)
    cluster = AgglomerativeClustering(n_clusters=n_clusters).fit(pca)

    kl = cluster.labels_

    cls = defaultdict(list)

    for i, k in zip(correlation_df.index, kl):
        cls[k].append(i)

    pca_df = pd.DataFrame(pca)
    pca_df['cluster_id'] = kl
    pca_df['cluster_id'] = pca_df['cluster_id'].astype('int')

    pca_plot = pd.DataFrame(np.column_stack((pca, kl.astype(int))))
    pca_plot.iloc[:, -1] = pca_plot.iloc[:, -1].astype(int)

    if pca_comp == 2:
        fig, ax = plt.subplots()
    else:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

    for c in sorted(pca_plot.iloc[:, -1].unique()):

        if pca_comp == 2:
            ax.scatter(pca_plot[pca_plot.iloc[:, -1] == c][0], pca_plot[pca_plot.iloc[:, -1] == c][1],
                       label='cluster ' + str(c + 1) + ' (' + str(len(pca_plot[pca_plot.iloc[:, -1] == c])) + ')')
        else:
            ax.scatter(pca_plot[pca_plot.iloc[:, -1] == c][0], pca_plot[pca_plot.iloc[:, -1] == c][1],
                       pca_plot[pca_plot.iloc[:, -1] == c][2],
                       label='cluster ' + str(c + 1) + ' (' + str(len(pca_plot[pca_plot.iloc[:, -1] == c])) + ')')
    ax.grid(True)
    ax.legend(loc='best', markerscale=.5)
    ax.set_xlabel('pca component 1 ({:.2f})'.format(pca_fit.explained_variance_ratio_[0]))
    ax.set_ylabel('pca component 2 ({:.2f})'.format(pca_fit.explained_variance_ratio_[1]))
    if pca_comp == 3:
        ax.set_zlabel('pca component 3 ({:.2f})'.format(pca_fit.explained_variance_ratio_[2]))

    plt.savefig(output, dpi=300)
    plt.close()

    return pca_df, cls


def get_balanced_train_test(df, clusters, month_range, start_year, train_size):

    cluster_train = []
    cluster_test = []

    print('TRAIN MONTHS: ' + str(month_range[2:train_size]))
    print('TEST MONTHS: ' + str(month_range[train_size:-3]))

    test_size = len(month_range[train_size:-3])

    for cl_id in clusters.keys():

        cluster_rows = df[df[settings.COLUMN_CAUSE_ENCODER].isin(clusters[cl_id])]

        dtrain = defaultdict(list)
        dtest = defaultdict(list)

        for tf in cluster_rows[settings.COLUMN_TRANSFORMER].unique():
            tf_rows = cluster_rows[cluster_rows[settings.COLUMN_TRANSFORMER] == tf]

            dtrain[settings.DAT_COLUMN_TRANSFORMER] += [tf_rows[settings.COLUMN_TRANSFORMER].iloc[0]] * (train_size - 2)
            dtest[settings.DAT_COLUMN_TRANSFORMER] += [tf_rows[settings.COLUMN_TRANSFORMER].iloc[0]] * (test_size)

            dtrain[settings.DAT_COLUMN_SUBSTATION] += [tf_rows[settings.COLUMN_SUBSTATION_ENCODER].iloc[0]] * (train_size - 2)
            dtest[settings.DAT_COLUMN_SUBSTATION] += [tf_rows[settings.COLUMN_SUBSTATION_ENCODER].iloc[0]] * (test_size)

            dtrain[settings.DAT_COLUMN_POTENCY] += [tf_rows[settings.COLUMN_POTENCY].iloc[0]] * (train_size - 2)
            dtest[settings.DAT_COLUMN_POTENCY] += [tf_rows[settings.COLUMN_POTENCY].iloc[0]] * (test_size)

            dtrain[settings.DAT_COLUMN_MONTH] += month_range[2:train_size]
            dtest[settings.DAT_COLUMN_MONTH] += month_range[train_size:-3]

            real_serie, failure_gap, failure_count, three_month, mean_active_time, label_serie = compute_features(tf, tf_rows, start_year, month_range)

            dtrain[settings.DAT_COLUMN_LTM] += three_month[2:train_size]
            dtest[settings.DAT_COLUMN_LTM] += three_month[train_size:-3]

            dtrain[settings.DAT_COLUMN_FG] += failure_gap[2:train_size]
            dtest[settings.DAT_COLUMN_FG] += failure_gap[train_size:-3]

            dtrain[settings.DAT_COLUMN_FC] += failure_count[2:train_size]
            dtest[settings.DAT_COLUMN_FC] += failure_count[train_size:-3]

            dtrain[settings.DAT_COLUMN_MAT] += mean_active_time[2:train_size]
            dtest[settings.DAT_COLUMN_MAT] += mean_active_time[train_size:-3]

            dtrain[settings.DAT_COLUMN_LABEL] += label_serie[2:train_size]
            dtest[settings.DAT_COLUMN_LABEL] += label_serie[train_size:-3]

        ### BALANCE TRAIN SET ###

        tr = pd.DataFrame(dtrain)

        missing_month = False

        for mt in month_range[2:train_size]:

            mt_rows = tr[tr[settings.DAT_COLUMN_MONTH] == mt]
            size_1 = len(mt_rows[mt_rows[settings.DAT_COLUMN_LABEL] == 1])
            size_0 = len(mt_rows[mt_rows[settings.DAT_COLUMN_LABEL] == 0])

            if size_1 == 0:
                missing_month = True
                break

            mn = min([size_0, size_1])
            mx = max([size_0, size_1])

            id_mx = np.argmax([size_0, size_1])

            tr.drop(mt_rows[mt_rows[settings.DAT_COLUMN_LABEL] == id_mx].sample(n=(mx - mn)).index, inplace=True)

        if missing_month:
            continue

        #########################

        ### BALANCE TEST SET ###

        te = pd.DataFrame(dtest)

        missing_month = False

        for mt in month_range[train_size:-3]:

            mt_rows = te[te[settings.DAT_COLUMN_MONTH] == mt]
            size_1 = len(mt_rows[mt_rows[settings.DAT_COLUMN_LABEL] == 1])
            size_0 = len(mt_rows[mt_rows[settings.DAT_COLUMN_LABEL] == 0])

            if size_1 == 0:
                missing_month = True
                break

            mn = min([size_0, size_1])
            mx = max([size_0, size_1])

            id_mx = np.argmax([size_0, size_1])

            te.drop(mt_rows[mt_rows[settings.DAT_COLUMN_LABEL] == id_mx].sample(n=(mx - mn)).index, inplace=True)

        if missing_month:
            continue

        #########################

        cluster_train.append(tr)
        cluster_test.append(te)

    return cluster_train, cluster_test


def run_group_online_model(train, test, model_output):

    result = {
        'month': [],
        'transformers': [],
        'failure_probabilities': [],
        'true_labels': []
    }

    model = SVC(kernel='rbf', gamma='scale', probability=True, C=1.5)

    x_train = train.iloc[:, 1:-1].copy()
    y_train = np.array(train.iloc[:, -1].copy())

    mslist = sorted(list(test[settings.DAT_COLUMN_MONTH].unique()))
    mslist = mslist[-1:] + mslist[:-1]

    for m in mslist:

        model.fit(x_train, y_train)

        t = test[test[settings.DAT_COLUMN_MONTH] == m]

        x_test = t.iloc[:, 1:-1].copy()
        y_test = np.array(t.iloc[:, -1].copy())

        test_predictions_prob = model.predict_proba(x_test)

        result['transformers'].append(list(t[settings.DAT_COLUMN_TRANSFORMER]))
        result['month'].append(m)
        result['failure_probabilities'].append(list(test_predictions_prob[:, 1]))
        result['true_labels'].append(list(y_test))

        x_train = x_train.append(x_test)
        y_train = np.concatenate((y_train, y_test), axis=0)

    open(model_output, 'wb').write(pickle.dumps(model))
    return pd.DataFrame(result)


def run(database, train_size, clusters=None):

    if clusters:

        # TODO: IMPLEMENT MANUAL CLUSTERING
        print('NOT IMPLEMENTED')
        return

    # DATABASE NAME
    name = database.split('.')[0]

    # CREATING DIRs
    mkdir(settings.RESULT_PATH.format(name))
    mkdir(settings.DAT_PATH.format(name))
    mkdir(settings.VALIDATION_PATH.format(name))
    mkdir(settings.PLOT_PATH.format(name))
    mkdir(settings.MODEL_PATH.format(name))

    # READING DATA
    df, cause_encoder, substation_encoder = read_df(database)
    _, _, _, _, start_year, end_year, month_range = get_dataset_features(database)

    # COMPUTING FEATURES
    dat_file = settings.DAT_FILE.format(name, name)
    dat_df = save_dat_file(df, dat_file, start_year, month_range)
    # dat_df = pickle.loads(open(dat_file, 'rb').read())

    # CLUSTERIZATION
    dat_df_train = get_train_dat_file(dat_df, train_size)
    correlations = get_correlations(dat_df_train)
    cluster_plot_file = settings.PLOT_FILE.format(name, name)
    _, cls = get_clusters(correlations, cluster_plot_file)

    # COMPUTING FEATURES FOR CLUSTERIZED DATA
    train, test = get_balanced_train_test(df, cls, month_range, start_year, train_size)

    result_file = settings.VALIDATION_FILE.format(name, name)

    result = pd.DataFrame()

    for cl_id in sorted(cls.keys()):

        model_file = settings.MODEL_FILE.format(name, name, str(cl_id))

        ce = cause_encoder.inverse_transform(cls[cl_id])
        r = run_group_online_model(train[cl_id], test[cl_id], model_file)

        r['cluster'] = [', '.join(ce)] * len(r)
        r['cluster_id'] = [cl_id] * len(r)

        result = result.append(r, ignore_index=True)

    result.to_csv(result_file, sep='\t', index=False)