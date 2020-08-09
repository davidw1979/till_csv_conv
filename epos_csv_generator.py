import numpy as np
import pandas as pd
import sys


def add_blank_rows(qty, df):
    # create blank row
    blank_row = pd.DataFrame([[np.nan] * len(df.columns)], columns=df.columns)

    # add blank rows
    for i in range(0, qty):
        # append single blank row to dataframe
        df = df.append(blank_row)

    return df


def correct_index_record(df):
    # reset index
    df = df.reset_index(drop=True)

    # correct record values
    for index, row in df.iterrows():
        if row["Record"] != index + 1:
            df.loc[index, "Record"] = index + 1
    
    return df


def calc_blanks(num):
    if num < 50:
        req = 50 - num
    else:
        req = 50 - (num % 50)

    return req


def main():
    # check argument usage is correct
    if len(sys.argv) != 2:
        exit("Incorrect usage. This program takes 1 command line argument - the csv filename.")

    # load files & set start & highest department variables
    df = pd.read_csv(sys.argv[1])
    current_dept = 1
    final_dept = df.iloc[len(df) - 1]["Department Link"]

    # set new dataframe as data with first Department Link
    new_df = df.drop(df[df['Department Link'] != current_dept].index)

    # generate required blank rows for new dataframe
    blanks_needed = calc_blanks(len(new_df))
    new_df = add_blank_rows(blanks_needed, new_df)

    # main loop -> iterate over all department link groups
    while current_dept < final_dept:
        # create temp dataframe of next department link value
        current_dept += 1
        temp_df = df.drop(df[df['Department Link'] != current_dept].index)

        # calculate blank rows to take upto next 50 for temp
        blanks_needed = calc_blanks(len(temp_df))

        # join onto final dataframe and add required blank rows
        new_df = new_df.append(temp_df)
        new_df = add_blank_rows(blanks_needed, new_df)
    
    # correct all indexes & records
    new_df = correct_index_record(new_df)
    print('only ran correction once')

    # create output csv file
    new_df.to_csv('output.csv', index=False)
    return 0

if __name__ == "__main__":
    main()
