import pandas as pd 
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import os
from env_setup import auth
from statsmodels.tsa.ar_model import AutoReg

try:
    key_path = os.environ['SHEET_KEY_PATH']
except KeyError:
    # path not yet set
    auth(os.path.join('..', '.env', 'google_credentials.json'))
    key_path = os.environ['SHEET_KEY_PATH']


scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(key_path, scope)
gc = gspread.authorize(credentials)
spreadsheet_key = '1mKOeKWf8f_mUmxbDQeHMA-P6lk6SfZf4Q9CRBH44EHU'
book = gc.open_by_key(spreadsheet_key)
worksheet = book.worksheet("Results_number")
table = worksheet.get_all_values()

def getBuildingDF():
    df = pd.DataFrame(table[3:], columns=table[2])
    df_raw_bdata = df.drop(["SampleID","ManholeID"],axis=1)
    df_raw_bdata = df_raw_bdata.drop(df.tail(8).index)
    df_raw_bdata = df_raw_bdata.iloc[:, :-5]
    df_raw_bdata.iloc[:,1:] = df_raw_bdata.iloc[:,1:].fillna(0).replace("",0).replace("ND",0).astype(float)
    cases_by_build = df_raw_bdata.groupby("Building(s)")[df_raw_bdata.columns[1:]].apply(lambda x: (x > 0).sum())
    return cases_by_build

def getBuildingCases(df):
    return df.sum(axis=1).sort_values(ascending=False)

def getAutoCorrelationByBuild(case_df):
    results = []
    for building_name in case_df.index:
        values_app = pd.DataFrame(case_df.loc[building_name])
        dataframe = pd.concat([values_app.shift(1), values_app], axis=1)
        dataframe.columns = ['t-1', 't+1']
        result = dataframe.corr()['t-1']['t+1']
        results.append((0 if np.isnan(result) else result,building_name))
    results.sort(reverse=True)
    return results

def makePrediction(offset,train):
    model = AutoReg(train, lags=offset,old_names=False)
    model_fit = model.fit()
    return model_fit.predict(start=len(train), end=len(train), dynamic=False)

def predictAreaCase(results,case_df):
    above7 = [elem for elem in results if elem[0] >= 0.7]
    predictions = []
    for build in above7:
        print(build[1],makePrediction(1,case_df.loc[build[1]].values))
        predictions.append((build[1],makePrediction(2,case_df.loc[build[1]].values)[0]))
    return predictions

if __name__ == "__main__":
    case_df = getBuildingDF()
    building_stats = getBuildingCases(case_df)
    print(building_stats)
    ranked_correlation = getAutoCorrelationByBuild(case_df)
    print(ranked_correlation)
    predictAreaCase(ranked_correlation,case_df)

