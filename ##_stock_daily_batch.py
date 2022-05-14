#!/usr/bin/env python
# coding: utf-8

# In[60]:

def job():

  # 実行は必ず20時以降、翌日の8時前に実施する
  import os
  import numpy as np
  import pandas as pd
  import datetime as dt
  from pandas_datareader import DataReader
  from pandas import Series, DataFrame


  # In[61]:

    
  print(os.getcwd())


  # In[62]:


  today = dt.date.today()


  # In[64]:


  yesterday = today - dt.timedelta(days = 1)


  # In[70]:


  df_list = pd.read_csv('##_toshop&s.csv', index_col=[0], header=[0], parse_dates=[0])


  # In[71]:


  df_list['key'] = df_list["コード"].astype(str) + ".T"


  # In[72]:


  end = dt.datetime.now() - dt.timedelta(days = 1)
  start = end - dt.timedelta(days = 30)


  # In[73]:


  df_stock = DataReader(df_list['key'].values, 'yahoo', start, end)


  # In[116]:


  df_stock.to_csv('stock_' + format(yesterday, '%Y%m%d') + '.csv')


  # In[117]:


  print("output stock")


  # In[ ]:


  print("Start IDNR4")


  # In[74]:


  df_idnr1 = df_stock.tail(4)


  # In[75]:


  # 階層構造を逆にすることができます。今回は列方向で試します。
  df_idnr1 = df_idnr1.swaplevel('Attributes','Symbols',axis=1)


  # In[76]:


  df_idnr1.sort_values(by=['Symbols', 'Attributes'], axis=1, inplace=True)


  # In[77]:


  # マルチインデックスのカラム名を取得する
  list = df_idnr1.columns.get_level_values('Symbols')


  # In[78]:


  # High-Lowの計算結果を新たな列として追加
  for i in list: 
      df_idnr1[i, 'diff'] = df_idnr1[i, 'High'] - df_idnr1[i, 'Low']


  # In[79]:


  df_idnr1.sort_values(by=['Symbols', 'Attributes'], axis=1, inplace=True)


  # In[80]:


  df_sel = df_idnr1.loc[:, (slice(None),'diff')].idxmin()


  # In[81]:


  # 高値と安値の幅が直近で最小になっている銘柄を抽出
  df_sel2 = df_sel.unstack(level=1)


  # In[82]:


  # 直近がファイル作成日付と一致する行を抽出
  df_sel3 = df_sel2['diff'].dt.date == yesterday


  # In[86]:


  # indexを連番に振り直して元のインデックスは削除
  df_idnr2 = df_idnr1.tail(2).reset_index(drop=True)


  # In[87]:


  df_idnr2 = df_idnr2.T


  # In[88]:


  df_idnr2 = df_idnr2.pivot_table(index=['Symbols'], columns=['Attributes'])


  # In[89]:


  # 日付の比較Datetimeから日付のみを取得して比較
  df_idnr3 = df_idnr2[
              (df_idnr2[(0, 'High')] > df_idnr2[(1, 'High')]) &
              (df_idnr2[(0, 'Low')] < df_idnr2[(1, 'Low')])
              ]


  # In[90]:


  #　前日分の情報は削除
  df_idnr4 = df_idnr3.drop(0, axis=1)


  # In[91]:


  # 最上層の列を削除
  df_idnr4 = df_idnr4.droplevel(0, axis=1)


  # In[92]:


  df_idnr5 = df_idnr4[df_sel3]


  # In[94]:


  df_idnr5.to_csv('idnr4_' + format(yesterday, '%Y%m%d') + '.csv')


  # In[95]:


  print("output idnr4")


  # In[ ]:


  print("Start Turtle")


  # In[93]:


  # end = dt.datetime.now()
  difdate = start


  # In[97]:


  # 銘柄ごとの上位3番の金額を取得する＜最安値＞
  def getmax(series, topnum=3, getmin=True, getindex=False):
    if getindex is False:
      series = series.sort_values(ascending=getmin).head(topnum).reset_index(drop=True)
      series.index += 1
      return series
    else:
      return series.sort_values(ascending=getmin).head(topnum).index

  df_min_price1 = df_stock.apply(getmax, axis=0, topnum=3, getindex = False)

  # 'Low'と'Adj Close'だけ残して他は削除 , 'Close', 'Open', 'Volume'),level=1, inplace=True
  df_min_price1.drop(columns=['Close', 'Open', 'High', 'Volume'], inplace=True)

  # indexの順番を入れ替えて、ソート
  df_min_price1 = df_min_price1.swaplevel('Attributes','Symbols', axis=1)
  df_min_price1.sort_values(by=['Symbols', 'Attributes'], axis=1, inplace=True)

  # 終値は最安値を抽出
  df_aclose = df_min_price1.loc[1, (slice(None), 'Adj Close')]

  # SeriesをDataFrameに変換。その際にMaltiIndexのSymbolsをIndexに設定
  df_aclose = df_aclose.unstack(level=1)

  # 安値は2番めに安い金額を抽出（終値が最大の場合、その日の安値も最大であるため）
  df_low = df_min_price1.loc[2, (slice(None), 'Low')]
  df_low = df_low.unstack(level=1)

  # DataFrameをIndexでマージ
  df_min_price2 = pd.merge(df_aclose, df_low, left_index=True, right_index=True)

  # 銘柄ごとの上位3番の日付を取得する＜最安値＞
  def getmax(series, topnum=3, getmin=True, getindex=False):
    if getindex is False:
      series = series.sort_values(ascending=getmin).head(topnum).reset_index(drop=True)
      series.index += 1
      return series
    else:
      return series.sort_values(ascending=getmin).head(topnum).index

  df_min_date1 = df_stock.apply(getmax, axis=0, topnum=3, getindex = True)

  # 'High'と'Adj Close'だけ残して他は削除 , 'Close', 'Open', 'Volume'),level=1, inplace=True
  df_min_date1.drop(columns=['Close', 'Open', 'High', 'Volume'], inplace=True)

  # indexの順番を入れ替えて、ソート
  df_min_date1 = df_min_date1.swaplevel('Attributes','Symbols', axis=1)
  df_min_date1.sort_values(by=['Symbols', 'Attributes'], axis=1, inplace=True)

  # 終値は最高値を出した日を抽出
  df_aclose_d = df_min_date1.loc[0, (slice(None), 'Adj Close')]

  # SeriesをDataFrameに変換。その際にMaltiIndexのSymbolsをIndexに設定
  df_aclose_d = df_aclose_d.unstack(level=1)

  # 安値は2番めに安い金額を出した日を抽出（終値が最小の場合、その日の安値も最小であるため）
  df_low_d = df_min_date1.loc[1, (slice(None), 'Low')]
  df_low_d = df_low_d.unstack(level=1)

  # DataFrameをIndexでマージ
  df_min_date2 = pd.merge(df_aclose_d, df_low_d, left_index=True, right_index=True)

  # 列名を置換
  df_min_date2.rename(columns = {'Adj Close':'Adjdate', 'Low':'Lowdate'}, inplace=True)

  df_min_analysis = pd.merge(df_min_price2, df_min_date2, left_index=True, right_index=True)

  # 日付の比較Datetimeから日付のみを取得して比較
  # todayadj = end - dt.timedelta(days = 4)
  df_min_analysis =df_min_analysis[(df_min_analysis['Adjdate'].dt.date == pd.to_datetime(format(yesterday, '%Y%m%d')).date()) &
                  (df_min_analysis['Adj Close'] - df_min_analysis['Low'] < 0) &
                  (abs(df_min_analysis['Adjdate'] - df_min_analysis['Lowdate']) >= dt.timedelta(days=3))
                  ]

  df_min_analysis.to_csv('tsplus_min_' + format(yesterday, '%Y%m%d') + '.csv')


  # In[ ]:


  print("output tsplus_min")


  # In[98]:


  # 銘柄ごとの上位3番の金額を取得する＜最高値＞
  def getmax(series, topnum=3, getmin=False, getindex=False):
    if getindex is False:
      series = series.sort_values(ascending=getmin).head(topnum).reset_index(drop=True)
      series.index += 1
      return series
    else:
      return series.sort_values(ascending=getmin).head(topnum).index

  df_max_price1 = df_stock.apply(getmax, axis=0, topnum=3, getindex = False)

  # 'High'と'Adj Close'だけ残して他は削除 , 'Close', 'Open', 'Volume'),level=1, inplace=True
  df_max_price1.drop(columns=['Close', 'Open', 'Low', 'Volume'], inplace=True)

  # indexの順番を入れ替えて、ソート
  df_max_price1 = df_max_price1.swaplevel('Attributes','Symbols', axis=1)
  df_max_price1.sort_values(by=['Symbols', 'Attributes'], axis=1, inplace=True)

  # 終値は最高値を抽出
  df_aclose = df_max_price1.loc[1, (slice(None), 'Adj Close')]

  # SeriesをDataFrameに変換。その際にMaltiIndexのSymbolsをIndexに設定
  df_aclose = df_aclose.unstack(level=1)

  # 高値は2番めに高い金額を抽出（終値が最大の場合、その日の高値も最大であるため）
  df_high = df_max_price1.loc[2, (slice(None), 'High')]
  df_high = df_high.unstack(level=1)

  # DataFrameをIndexでマージ
  df_max_price2 = pd.merge(df_aclose, df_high, left_index=True, right_index=True)

  # 銘柄ごとの上位3番の日付を取得する＜最高値＞
  def getmax(series, topnum=3, getmin=False, getindex=False):
    if getindex is False:
      series = series.sort_values(ascending=getmin).head(topnum).reset_index(drop=True)
      series.index += 1
      return series
    else:
      return series.sort_values(ascending=getmin).head(topnum).index

  df_max_date1 = df_stock.apply(getmax, axis=0, topnum=3, getindex = True)

  # 'High'と'Adj Close'だけ残して他は削除 , 'Close', 'Open', 'Volume'),level=1, inplace=True
  df_max_date1.drop(columns=['Close', 'Open', 'Low', 'Volume'], inplace=True)

  # indexの順番を入れ替えて、ソート
  df_max_date1 = df_max_date1.swaplevel('Attributes','Symbols', axis=1)
  df_max_date1.sort_values(by=['Symbols', 'Attributes'], axis=1, inplace=True)

  # 終値は最高値を出した日を抽出
  df_aclose_d = df_max_date1.loc[0, (slice(None), 'Adj Close')]

  # SeriesをDataFrameに変換。その際にMaltiIndexのSymbolsをIndexに設定
  df_aclose_d = df_aclose_d.unstack(level=1)

  # 高値は2番めに高い金額を出した日を抽出（終値が最大の場合、その日の高値も最大であるため）
  df_high_d = df_max_date1.loc[1, (slice(None), 'High')]
  df_high_d = df_high_d.unstack(level=1)

  # DataFrameをIndexでマージ
  df_max_date2 = pd.merge(df_aclose_d, df_high_d, left_index=True, right_index=True)

  # 列名を置換
  df_max_date2.rename(columns = {'Adj Close':'Adjdate', 'High':'Highdate'}, inplace=True)

  df_max_analysis = pd.merge(df_max_price2, df_max_date2, left_index=True, right_index=True)

  # 日付の比較Datetimeから日付のみを取得して比較
  # todayadj = end - dt.timedelta(days = 4)
  df_max_analysis =df_max_analysis[(df_max_analysis['Adjdate'].dt.date == pd.to_datetime(format(yesterday, '%Y%m%d')).date()) &
                  (df_max_analysis['Adj Close'] - df_max_analysis['High'] > 0) &
                  (abs(df_max_analysis['Adjdate'] - df_max_analysis['Highdate']) >= dt.timedelta(days=3))
                  ]

  df_max_analysis.to_csv('tsplus_max_' + format(yesterday, '%Y%m%d') + '.csv')


  # In[99]:


  print("output tsplus_max")


  # In[100]:


  print("Start 80-20S")


  # In[101]:


  # 階層構造を逆にすることができます。今回は列方向で試します。
  df_stock2 = df_stock.swaplevel('Attributes','Symbols',axis=1)


  # In[102]:


  df_stock2.sort_values(by=['Symbols', 'Attributes'], axis=1, inplace=True)


  # In[103]:


  # マルチインデックスのカラム名を取得する
  list = df_stock2.columns.get_level_values('Symbols')


  # In[104]:


  # RSIの計算
  def rsi(df):
      # 前日との差分を計算
      df_diff = df[i,"Close"].diff(1)

      # 計算用のDataFrameを定義
      df_up, df_down = df_diff.copy(), df_diff.copy()
      
      # df_upはマイナス値を0に変換
      # df_downはプラス値を0に変換して正負反転
      df_up[df_up < 0] = 0
      df_down[df_down > 0] = 0
      df_down = df_down * -1
      
      # 期間03でそれぞれの平均を算出
      df_up_sma03 = df_up.rolling(window=3, center=False).mean()
      df_down_sma03 = df_down.rolling(window=3, center=False).mean()

      # RSIを算出
      df[i, "RSI"] = 100.0 * (df_up_sma03 / (df_up_sma03 + df_down_sma03))

      return df

  for i in list: 
      df_stock2 = rsi(df_stock2)


  # In[105]:


  # High-Lowの計算結果を新たな列として追加
  for i in list: 
      df_stock2[i, 'diff'] = df_stock2[i, 'High'] - df_stock2[i, 'Low']
      df_stock2[i, 'eighty'] = df_stock2[i, 'High'] - df_stock2[i, 'diff'] * 0.2
      df_stock2[i, 'twenty'] = df_stock2[i, 'Low'] + df_stock2[i, 'diff'] * 0.2
      df_stock2[i, 'RSI_diff'] = df_stock2[i,"RSI"].diff(1)


  # In[106]:


  df_stock2.sort_values(by=['Symbols', 'Attributes'], axis=1, inplace=True)


  # In[107]:


  # 日付の比較Datetimeから最後の日のみを取得
  df_stock3 = df_stock2.tail(1)


  # In[108]:


  df_stock3 = df_stock3.T


  # In[109]:


  df_stock3 = df_stock3.pivot_table(index=['Symbols'], columns=['Attributes'])


  # In[110]:


  df_stock3 = df_stock3.droplevel(0, axis=1)


  # In[111]:


  # 日付の比較Datetimeから日付のみを取得して比較
  df_stock4 = df_stock3[(df_stock3['RSI'] < 30) &
                  (df_stock3['Open'] >= df_stock3['eighty']) &
                  (df_stock3['Close'] <= df_stock3['twenty'])
                  ]


  # In[112]:


  # 日付の比較Datetimeから日付のみを取得して比較
  df_stock5 = df_stock3[(df_stock3['RSI'] > 70) &
                  (df_stock3['Close'] >= df_stock3['eighty']) &
                  (df_stock3['Open'] <= df_stock3['twenty'])
                  ]


  # In[118]:


  df_stock4.to_csv('pin_80_20_買い_' + format(yesterday, '%Y%m%d') + '.csv')


  # In[119]:


  df_stock5.to_csv('pin_80_20_売り_' + format(yesterday, '%Y%m%d') + '.csv')


  # In[120]:


  print("output pin_80_20")


  # In[121]:


  # 行にNaNデータがある銘柄をリスト化（後で再取得を計る）
  df_nanlist = df_stock[df_stock.isnull().any(axis=1)]


  # In[123]:


  df_nanlist.to_csv('nanlist_' + format(yesterday, '%Y%m%d') + '.csv')


  # In[ ]:

job()


