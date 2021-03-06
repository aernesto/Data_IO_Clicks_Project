"""
The aim of this script is to create a database in hdf5 format
"""

# import copy
import time
import sys
from official_fcns import *


def create_hfd5_data_structure(hdf5file, groupname, num_trials, num_samples, max_trials=1000000):
    """
    :param hdf5file: h5py.File
    :param groupname:
    :param num_trials: nb of trials
    :param max_trials: for db decision datasets max nb of rows
    :param num_samples: for db decision datasets; nb of cols
    :return: created group
    """
    group = hdf5file.create_group(groupname)
    dt = h5py.special_dtype(vlen=np.dtype('f'))
    group.create_dataset('trials', (num_trials, 3), maxshape=(max_trials, 10), dtype=dt)
    group.create_dataset('trial_info', (num_trials, 3), maxshape=(max_trials, 10), dtype='f')
    group.create_dataset('decision_lin', (num_trials, num_samples), dtype='i', maxshape=(max_trials, num_samples))
    group.create_dataset('decision_nonlin', (num_trials, num_samples),
                         dtype='i', maxshape=(max_trials, num_samples))
    return group


def populate_hfd5_db(fname, four_par, num_of_trials, number_of_samples=1):
    """
    Generate stimulus data and store as hdf5 file.
    This is the main function called by this script.
    """
    # open/create file
    f = h5py.File(fname, 'a')
    ll, lh, h, t = four_par

    # create group corresponding to parameters
    group_name = build_group_name(four_par)

    if group_name in f:  # if dataset already exists, exit without doing anything
        print('data already present, file left untouched')
    else:  # if dataset doesn't exist, create it
        print('creating dataset with group name {}'.format(group_name))
        grp = create_hfd5_data_structure(f, group_name, num_of_trials, num_samples=number_of_samples)

        # create trials dataset
        trials_data = grp['trials']
        # get row indices of new data to insert
        row_indices = np.r_[:num_of_trials]

        # create info on data
        info_data = grp['trial_info']  # info dataset
        info_data.attrs['h'] = h
        info_data.attrs['T'] = t
        info_data.attrs['low_click_rate'] = ll
        info_data.attrs['high_click_rate'] = lh
        info_data.attrs['S'] = (lh - ll) / np.sqrt(ll + lh)
        data_version = 1  # version number of new data to insert

    # populate database
    for row_idx in row_indices:
        # vector of CP times
        cptimes = gen_cp(t, h)
        trials_data[row_idx, 2] = cptimes

        # stimulus (left clicks, right clicks)
        (left_clicks, right_clicks), init_state, end_state = gen_stim(cptimes, ll, lh, t)
        trials_data[row_idx, :2] = left_clicks, right_clicks

        # populate info dataset
        info_data[row_idx, :] = init_state, end_state, data_version

    info_data.attrs['last_version'] = data_version
    f.flush()
    f.close()


def dump_info(four_parameters, s, nt, nruns):
    print('S value: {}'.format(s))
    print('low click rate: {}'.format(four_parameters[0]))
    print('high click rate: {}'.format(four_parameters[1]))
    print('hazard rate: {}'.format(four_parameters[2]))
    print('interr. time: {}'.format(four_parameters[3]))
    print('nb of trials / hist: {}'.format(nruns))
    print('nb of trials in sequence: {}'.format(nt))


if __name__ == '__main__':
    """
    aim is to create a small size database with data from a single dataset
    arguments passed to the script should be in the following order:
    1. low rate
    2. S
    3. hazard rate
    4. interrogation time
    5. db filename
    6. num_trials
    7. num_samples
    """
    if len(sys.argv) == 8:
        # low click rate
        try:
            lr = float(sys.argv[1])
        except ValueError:
            print('\nError msg: first command line arg corresponding to low click rate should be a positive scalar\n')
            exit(1)

        # S (Skellam SNR)
        try:
            S = float(sys.argv[2])
        except ValueError:
            print('\nError msg: second command line arg corresponding to S should be in [0.5,1,...,10]\n')
            exit(1)

        # hazard rate
        try:
            hazard = float(sys.argv[3])
        except ValueError:
            print('\nError msg: third command line arg corresponding to h should be a non-negative scalar\n')
            exit(1)

        # interrogation time
        try:
            int_time = float(sys.argv[4])
        except ValueError:
            print('\nError msg: fourth command line arg corresponding to T should be a positive scalar\n')
            exit(1)

        # hdf5 db filename
        try:
            filename = sys.argv[5]
            if filename[-3:] != '.h5':
                raise ValueError("By convention, db filename should end with '.h5'")
        except ValueError as err:
            print('\nError msg: fifth command line arg corresponding to filename has a pb')
            print(err.args)
            exit(1)

        # Number of Trials
        try:
            number_of_trials = int(sys.argv[6])
        except ValueError:
            print('\nError msg: sixth command line arg corresponding to number of trials should be an integer\n')
            exit(1)

        # Number of Samples
        try:
            nsamples = int(sys.argv[7])
        except ValueError:
            print('\nError msg: seventh command line arg corresponding to number of samples should be an integer\n')
            exit(1)


        start_time = time.time()

        hr = get_lambda_high(lr, S)
        fp = (lr, hr, hazard, int_time)
        grp_name = build_group_name(fp)
        true_g = get_best_gamma(S, hazard)

        populate_hfd5_db(filename, fp, number_of_trials)

        print("--- {} seconds ---".format(time.time() - start_time))
    else:
        raise OSError('Script called with wrong number of command line args')
        exit(1)
