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
"""
This script generate output CSV
for national 1980-1990 and it is aggregated
from state 1980-1990 file.
"""

import pandas as pd


def _process_national_1980_1990(url):
    """
    Function Loads input txt datasets
    from 1980-1990 on a National Level,
    cleans it and return cleaned dataframe.
    Args:
        url: url of the dataset
    Returns:
        Cleaned Dataframe
    """
    # 0 = Ages 0-4, 1 = Ages 5-9, 2 = Ages 10-14, 3 = Ages 15-19
    # 4 = Ages 20-24, 5 = Ages 25-29, 6 = Ages 30-34, 7 = Ages 35-39
    # 8 = Ages 40-44, 9 = Ages 45-49, 10 = Ages 50-54, 11 = Ages 55-59
    # 12 = Ages 60-64, 13 = Ages 65-69, 14 = Ages 70-74, 15 = Ages 75-79
    # 16 = Ages 80-84, 17 = Ages 85+

    # COLUMNS_TO_SUM = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,\
    #  11, 12, 13, 14, 15, 16, 17]
    _cols = ['Info', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,\
        11, 12, 13, 14, 15, 16, 17]
    #_cols = ['Info', COLUMNS_TO_SUM]

    # reading the csv input file
    df = pd.read_table(url,
                       index_col=False,
                       delim_whitespace=True,
                       engine='python',
                       names=_cols)

    # adding all the ages to get total value
    #df['Total'] = df[COLUMNS_TO_SUM].sum(axis=1)
    df['Total']=df[0]+df[1]+df[2]+df[3]+df[4]+df[5]+df[6]\
        +df[7]+df[8]+df[9]+df[10]+df[11]+df[12]+df[13]+df[14]\
        +df[15]+df[16]+df[17]

    # dropping unwanted columns
    df.drop(columns=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,\
        12, 13, 14, 15, 16, 17], inplace=True)

    # extracting year and geoid from Info column
    df['Info'] = [f'{x:05}' for x in df['Info']]
    df['Info'] = df['Info'].astype(str)
    df['Year'] = df['Info'].str[0:2] + "-198" + df['Info'].str[2]

    # extracting sex and race from the Info column
    df['Race'] = df['Info'].str[3]
    df['Sex'] = df['Info'].str[4]
    # df = df.replace({'Sex':{'1':'Male', '2':'Female}
    # df = df.replace({'Race':{'1':'W', '2': 'B', '3': 'AI',
    # '4': 'AP', '5': 'W', '6':'B', '7':'AI', '8':'AP'}})
    df['Sex'] = df['Sex'].str.replace('1', 'Male')
    df['Sex'] = df['Sex'].str.replace('2', 'Female')
    df['Race'] = df['Race'].str.replace('1', 'W')
    df['Race'] = df['Race'].str.replace('2', 'B')
    df['Race'] = df['Race'].str.replace('3', 'AI')
    df['Race'] = df['Race'].str.replace('4', 'AP')
    df['Race'] = df['Race'].str.replace('5', 'W')
    df['Race'] = df['Race'].str.replace('6', 'B')
    df['Race'] = df['Race'].str.replace('7', 'AI')
    df['Race'] = df['Race'].str.replace('8', 'AP')
    df['SR'] = df['Sex'] + ' ' + df['Race']
    df.drop(columns=['Info', 'Sex', 'Race'], inplace=True)

    # it groups the df as per columns provided
    # performs the provided functions on the data
    df = df.groupby(['Year','SR'])\
        .sum().transpose().stack(0).reset_index()

    # splitting year and geoId
    df['geo_ID'] = df['Year'].str.split('-', expand=True)[0]
    df['geo_ID'] = 'geoId/' + df['geo_ID']
    df['Year'] = df['Year'].str.split('-', expand=True)[1]

    # dropping unwanted column
    df.drop(columns=['level_0'], inplace=True)

    # providing proper column names
    df.columns = [
        'Year', 'Count_Person_Female_AmericanIndianAndAlaskaNativeAlone',
        'Count_Person_Female_AsianOrPacificIslander',
        'Count_Person_Female_BlackOrAfricanAmericanAlone',
        'Count_Person_Female_WhiteAlone',
        'Count_Person_Male_AmericanIndianAndAlaskaNativeAlone',
        'Count_Person_Male_AsianOrPacificIslander',
        'Count_Person_Male_BlackOrAfricanAmericanAlone',
        'Count_Person_Male_WhiteAlone', 'geo_ID'
    ]

    # aggregating columns to get Count_Person_Male
    df["Count_Person_Male"] = df.loc[:,['Count_Person_Male_'+\
        'AmericanIndianAndAlaskaNativeAlone',
        'Count_Person_Male_AsianOrPacificIslander',
        'Count_Person_Male_BlackOrAfricanAmericanAlone',
        'Count_Person_Male_WhiteAlone']].sum(axis=1)

    # aggregating columns to get Count_Person_Female
    df["Count_Person_Female"] = df.loc[:,['Count_Person_Female_'+\
        'AmericanIndianAndAlaskaNativeAlone',
        'Count_Person_Female_AsianOrPacificIslander',
        'Count_Person_Female_BlackOrAfricanAmericanAlone',
        'Count_Person_Female_WhiteAlone']].sum(axis=1)

    df.drop(columns=['geo_ID'], inplace=True)

    df = df.groupby(['Year']).sum().reset_index()

    # inserting geoid in columns
    df.insert(0, 'geo_ID', 'country/USA', True)

    return df


def process_national_1980_1990(url):
    """
    Function writes the output
    dataframe generated to csv
    and return column names.
    Args:
        url: url of the dataset
    Returns:
        Column of cleaned Dataframe
    """
    df = _process_national_1980_1990(url)
    # writing the dataframe to output csv
    df.to_csv("nationals_result_1980_1990.csv")
    return df.columns