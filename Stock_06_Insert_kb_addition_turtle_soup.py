#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import sqlalchemy as sa
import pymysql
import datetime as dt
from pandas_datareader import DataReader
from pandas import Series, DataFrame
import pandas_datareader.data as web

def preprocess():
    # Mysqlへ接続
    url = 'mysql+pymysql://cyamaryan:python@localhost:13306/stock?charset=utf8mb4'
    # engineの作成
    engine = sa.create_engine(url, echo=False)

    # どの日付を起点にするかここでコントロールする
    # 1-(1)文字列からDatetime形式へ変換
    filedate = '20220407'
    tdatetime = dt.datetime.strptime(filedate, '%Y%m%d')
    today = tdatetime.date()
    # 1-(2)date関数のTodayを算出して調整
    # today = dt.date.today() - dt.timedelta(days = 33)
    # 2 スクリプト分のための形式変換
    format(today, "'%Y-%m-%d'")

    query = "select trading_date from stock.kb_values where DATE(`trading_date`) <= " + format(today, "'%Y-%m-%d'") + "group by trading_date order by trading_date desc"
    df_seldate = pd.read_sql(query,con = engine)

def dbinput():
    # 日付（取引日）の範囲抽出　始まりの日付(上記Todayを含む20日分)
    start = df_seldate.iat[20,0]
    query = "select * from stock.kb_values where trading_date >= " + format(start, "'%Y-%m-%d'") + " and trading_date <= "  + format(today, "'%Y-%m-%d'")
    df_values = pd.read_sql(query,con = engine)

def turtle():
    # codeでグループ化(基準日を含む)
    ddf = df_values.groupby('code')

    # ddf.rank():グループ化した表のうち、それぞれの値の順位を取得する
    df_addrank = pd.merge(df_values, ddf.rank(), left_index=True, right_index=True)

    # 最安値が過去2番めに低い日が、基準日よりも4営業日(21-3)よりも前の"コード"を抽出
    second_low = df_addrank[(df_addrank['trading_date_y']  < 18.0) & (df_addrank['low_y'] == 2.0)].code

    # 基準日の行を削除
    df_values2 = df_values[df_values['trading_date'] != today]

    # codeでグループ化(基準日を含まない)
    ddf2 = df_values2.groupby('code')

    # 基準日以外で過去最安値となった行を取得
    df_low = df_values2.loc[ddf2['low'].idxmin(),:]

    # 基準日が含まれている行に、過去最安値となった列をマージ
    df_addmin = pd.merge(df_values, df_low, left_on='code', right_on='code', how='left')

    # 基準日の終値が、基準日を除く過去最安値よりも安い
    df_turtleb = df_addmin[(df_addmin['trading_date_x']  == today) & (df_addmin['adjclose_x'] < df_addmin['low_y'])]

    # 最安値が過去2番めに低い日が、基準日よりも4営業日(21-3)よりも前の"コード"を抽出
    df_turtleb = df_turtleb.query('code in @second_low.values')

    # タートルスーププラスワンの買いのルールに該当するフラグを立てる
    df_turtleb['tsplb'] = 1

    # ここからタートルスープ（売り）の銘柄抽出
    # 基準日を含む過去2番めの最高値日は、基準日よりも4営業日(21-3)前である"コード"を抽出
    second_high = df_addrank[(df_addrank['trading_date_y']  < 18.0) & (df_addrank['high_y'] == 20.0)].code

    # 基準日以外で過去最高値となった行を取得
    df_high = df_values2.loc[ddf2['high'].idxmax(),:]

    # 基準日が含まれている行に、過去最高値となった列をマージ
    df_addmax = pd.merge(df_values, df_high, left_on='code', right_on='code', how='left')

    # 基準日の終値が、基準日を除く過去最高値よりも高い
    df_turtles = df_addmax[(df_addmax['trading_date_x']  == today) & (df_addmax['adjclose_x'] > df_addmax['high_y'])]

    # 基準日を含む過去2番めの最高値日は、基準日よりも4営業日(21-3)前である"コード"を抽出
    df_turtles = df_turtles.query('code in @second_high.values')

    # タートルスーププラスワンの売りのルールに該当するフラグを立てる
    df_turtles['tspls'] = 1

