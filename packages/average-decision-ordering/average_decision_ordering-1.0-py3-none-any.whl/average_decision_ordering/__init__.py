#! /usr/bin/env python

import random

import numpy as np
import pandas as pd


def heaviside(x):
    """Calculates the heaviside function for any input

    Args:
        x (float): input variable to have the heaviside function calculated

    Returns:
        float: result of the heaviside function
    """
    return 0.5 * (np.sign(x) + 1)

def norm(x):
    """normalizes the array to values between 0 and 1

    Args:
        x (list): list of floating point values

    Returns:
        list: normalized list of floating point values
    """
    return (x-min(x))/(max(x)-min(x))

def random_pairs(x, y, l):
    """Generates random pairs from two lists of floating point values

    Args:
        x (list): list of floating point numbers
        y (list): list of floating point numbers
        l (int): Size of final list of randomized pairs

    Returns:
        dataframe: pandas dataframe with randomized pairs from the inputs x and y
    """
    random.shuffle(x)
    random.shuffle(y)
    min_size = min(len(x), len(y))
    x = x[:min_size]
    y = y[:min_size]
    rp = np.vstack((x,y)).T
    loop_count = 0
    while len(rp) < l:
        random.shuffle(x)
        random.shuffle(y)
        app_rp = np.vstack((x,y)).T
        rp = np.concatenate((rp, app_rp), axis=0)
        loop_count += 1
        if loop_count > 100:
            break
    df = pd.DataFrame({"x":rp[:,0], "y":rp[:,1]})
    df.drop_duplicates(inplace=True, keep='first')
    return df.to_numpy()

def calc_do(fx0, fx1, gx0, gx1):
    """Calculates the difference ordering between two background pairs (fx0, gx0) and two signal pairs (fx1, gx1)

    Args:
        fx0 (float): First background value
        fx1 (float): First signal value
        gx0 (float): Second background value
        gx1 (float): Second signal value

    Returns:
        float: single decision ordering result
    """

    dfx = fx0 - fx1
    dgx = gx0 - gx1
    dos = heaviside(np.multiply(dfx, dgx))
    return dos

def calc_ado(fx, gx, target, n_pairs):
    """Calculates the average decision ordering from two lists of floating point values after normalization

    Args:
        fx (list): first list of floating point values
        gx (list): second list of floating point values
        target (list): list of binary classification targets (i.e. 0,1)
        n_pairs (int): number of pairs to average over

    Returns:
        float: average decision ordering
    """
    if n_pairs > len(fx)*len(gx):
        print("Requested pairs exceeds maximum sig/bkg combinations available")
        print("Please choose a value for n_pairs < len(fx)*len(gx)")
        return
    # normalize input data
    fx = norm(fx)
    gx = norm(gx)
        
    # Combine the data into a single dataframe
    dfy = pd.DataFrame({"fx": fx, "gx": gx, "y": target})

    # Separate data into signal and background
    dfy_sb = dfy.groupby("y")
    
    # Set signal/background dataframes
    df0 = dfy_sb.get_group(0)
    df1 = dfy_sb.get_group(1)

    # get the separate sig/bkg indices
    idx0 = df0.index.values.tolist()
    idx1 = df1.index.values.tolist()

    # generate random index pairs
    idx_pairs = random_pairs(idx0, idx1, n_pairs)
    idxp0 = idx_pairs[:, 0]
    idxp1 = idx_pairs[:, 1]

    # grab the fx and gx values for those sig/bkg pairs
    dfy0 = dfy.iloc[idxp0]
    dfy1 = dfy.iloc[idxp1]
    fx0 = dfy0["fx"].values
    fx1 = dfy1["fx"].values
    gx0 = dfy0["gx"].values
    gx1 = dfy1["gx"].values

    # find differently ordered pairs
    dos = calc_do(fx0=fx0, fx1=fx1, gx0=gx0, gx1=gx1)
    ado_val = np.mean(dos)
    if ado_val < 0.5:
        ado_val = 1.0 - ado_val

    return ado_val
