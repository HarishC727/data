# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''
This script generate output CSV
for state 1990-2000 and Count_Person_Male
and Count_person_Female are aggregated for this file.
'''

import pandas as pd


def _process_state_1990_2000(urls):
    '''
    Function Loads input txt datasets
    from 1990-2000 on a State Level,
    cleans it and return cleaned dataframe.
    '''
    final_df = pd.DataFrame()
    for url in urls:
        # reading the csv input file
        df = pd.read_table(url,
                           skiprows=15,
                           header=None,
                           delim_whitespace=True,
                           index_col=False,
                           engine='python')

        # NHWM = Non-Hispnic White Male, NHFM = Non-Hispnic White Female,
        # NHBM = Non-Hispnic Black Male, NHFM = Non-Hispnic Black Female,
        # NHAIANM = Non-Hispanic American Indian and Alaska Native Male,
        # NHAIANF = Non-Hispanic American Indian and Alaska Native Female,
        # NHAPIM = Non-Hispanic Asian and Pacific Islander Male,
        # NHAPIF = Non-Hispanic Asian and Pacific Islander Female,
        # HWM = Hispnic White Male, HFM = Hispnic White Female,
        # HBM = Hispnic Black Male, HFM = Hispnic Black Female,
        # HAIANM = Hispanic American Indian and Alaska Native Male,
        # HAIANF = Hispanic American Indian and Alaska Native Female,
        # HAPIM = Hispanic Asian and Pacific Islander Male,
        # HAPIF = Hispanic Asian and Pacific Islander Female,
        df.columns = [
            'Year', 'geo_ID', 'Age', 'NHWM', 'NHWF', 'NHBM', 'NHBF', 'NHAIANM',
            'NHAIANF', 'NHAPIM', 'NHAPIF', 'HWM', 'HWF', 'HBM', 'HBF', 'HAIANM',
            'HAIANF', 'HAPIM', 'HAPIF'
        ]

        # adding hispanic and non-hispanic columns to get total values
        df['Count_Person_Male_WhiteAlone'] = df["NHWM"] + df["HWM"]
        df['Count_Person_Female_WhiteAlone'] = df["NHWF"] + df["HWF"]
        df['Count_Person_Male_BlackOrAfricanAmericanAlone'] = df["NHBM"] + df[
            "HBM"]
        df['Count_Person_Female_BlackOrAfricanAmericanAlone']\
            =df["NHBF"]+df["HBF"]
        df['Count_Person_Male_AmericanIndianAndAlaskaNativeAlone']\
            =df["NHAIANM"]+df["HAIANM"]
        df['Count_Person_Female_AmericanIndianAndAlaskaNativeAlone']\
            =df["NHAIANF"]+df["HAIANF"]
        df['Count_Person_Male_AsianOrPacificIslander']\
             = df["NHAPIM"] + df["HAPIM"]
        df['Count_Person_Female_AsianOrPacificIslander']\
            = df["NHAPIF"] + df["HAPIF"]

        # dropping unwanted columns which are having origin
        df.drop(columns=[
            'Age', 'NHWM', 'NHWF', 'NHBM', 'NHBF', 'NHAIANM', 'NHAIANF',
            'NHAPIM', 'NHAPIF', 'HWM', 'HWF', 'HBM', 'HBF', 'HAIANM', 'HAIANF',
            'HAPIM', 'HAPIF'
        ],
                inplace=True)

        # providing geoId to the dataframe and
        # making the geoId of 2 digit as state
        df['geo_ID'] = [f'{x:02}' for x in df['geo_ID']]
        df['geo_ID'] = 'geoId/' + df['geo_ID']

        # it groups the df as per columns provided
        # performs the provided functions on the data
        df = df.groupby(['Year', 'geo_ID']).agg('sum').reset_index()

        # concatenating the value to final dataframe
        final_df = pd.concat([final_df, df])

    # aggregating columns to get Count_Person_Male
    final_df["Count_Person_Male"] = final_df.loc[:, [
        'Count_Person_Male_WhiteAlone',
        'Count_Person_Male_BlackOrAfricanAmericanAlone',
        'Count_Person_Male_AmericanIndianAndAlaskaNativeAlone',
        'Count_Person_Male_AsianOrPacificIslander'
    ]].sum(axis=1)

    # aggregating columns to get Count_Person_Female
    final_df["Count_Person_Female"] = final_df.loc[:, [
        'Count_Person_Female_WhiteAlone',
        'Count_Person_Female_BlackOrAfricanAmericanAlone',
        'Count_Person_Female_AmericanIndianAndAlaskaNativeAlone',
        'Count_Person_Female_AsianOrPacificIslander'
    ]].sum(axis=1)

    return final_df


def process_state_1990_2000(urls):
    '''
    Function writes the output
    dataframe generated to csv
    and return column names.
    '''
    final_df = _process_state_1990_2000(urls)
    # writing the dataframe to output csv
    final_df.to_csv("state_result_1990_2000.csv")
    return final_df.columns