import pandas as pd
import numpy as np
import requests
import math
import json
import os
import ffn
from finlab import get_token
from finlab import data
from finlab.utils import logger


def allow_asset_types(asset_types):
    def decorator(function):
        def wrapper(*args, **kwargs):

            if args[0].asset_type not in asset_types:
                raise Exception(f'Report.{function.__name__} for {args[0].asset_type} is not implemented. '
                                f'Allowed asset type: {str(asset_types)}')

            return function(*args, **kwargs)
        return wrapper
    return decorator


class Report(object):

    def __init__(self, creturn, position, fee_ratio, tax_ratio, trade_at, next_trading_date):
        self.creturn = creturn
        self.position = position
        self.benchmark = None
        self.fee_ratio = fee_ratio
        self.tax_ratio = tax_ratio
        self.trade_at = trade_at
        self.update_date = position.index[-1]
        self.asset_type = 'tw_stock' if (
            position.columns.str.find('USDT') == -1).all() else 'crypto'

        position_changed = position.diff().abs().sum(axis=1)
        self.last_trading_date = position_changed[position_changed != 0].index[-1] \
            if (position_changed != 0).sum() != 0 else position.index[0]
        self.next_trading_date = next_trading_date

    def get_benchmark(self):
        if self.asset_type == 'tw_stock':
            return data.get('benchmark_return:發行量加權股價報酬指數').squeeze()
        elif self.asset_type == 'crypto':
            return data.get('crypto:close').pct_change().mean(axis=1).add(1).cumprod().resample('1d').last()

    def get_price(self, price_at, adj=True):

        if self.asset_type == 'tw_stock':

            if adj:
                return data.get(f'etl:adj_{price_at}')
            else:
                chname = {'open': '開盤價', 'close': '收盤價',
                          'high': '最高價', 'low': '最低價', 'volume': '成交股數'}
                return data.get(f'price:{chname}')

        elif self.asset_type == 'crypto':
            return data.get(f'crypto:{price_at}')

    def get_stock_names(self):
        stock_names = data.cs.get_stock_names()

        if stock_names == {}:
            categories = data.get('security_categories')
            new_stock_names = dict(
                zip(categories['stock_id'], categories['name']))
            data.cs.cache_stock_names(new_stock_names)
            stock_names = data.cs.get_stock_names()

        return stock_names

    def display(self):

        if self.benchmark is not None:
            performance = pd.DataFrame({
                'strategy': self.creturn,
                'benchmark': self.benchmark.dropna()}).dropna().rebase()
        else:
            performance = pd.DataFrame({
                'strategy': self.creturn}).dropna().rebase()
        try:
            fig = self.create_performance_figure(
                performance, (self.position != 0).sum(axis=1))
            p = self.position.iloc[-1]

            from IPython.display import display
            display(fig)
            display(p[p != 0])
            display(self.position.index[-1])
            # return fig
        except:
            pass

    @staticmethod
    def create_performance_figure(performance_detail, nstocks):

        from plotly.subplots import make_subplots
        import plotly.graph_objs as go
        # plot performance

        def diff(s, period):
            return (s / s.shift(period)-1)

        drawdowns = performance_detail.to_drawdown_series()

        fig = go.Figure(make_subplots(
            rows=4, cols=1, shared_xaxes=True, row_heights=[2, 1, 1, 1]))
        fig.add_scatter(x=performance_detail.index, y=performance_detail.strategy/100-1,
                        name='strategy', row=1, col=1, legendgroup='performnace', fill='tozeroy')
        fig.add_scatter(x=drawdowns.index, y=drawdowns.strategy, name='strategy - drawdown',
                        row=2, col=1, legendgroup='drawdown', fill='tozeroy')
        fig.add_scatter(x=performance_detail.index, y=diff(performance_detail.strategy, 20),
                        fill='tozeroy', name='strategy - month rolling return',
                        row=3, col=1, legendgroup='rolling performance',)

        if 'benchmark' in performance_detail.columns:
            fig.add_scatter(x=performance_detail.index, y=performance_detail.benchmark/100-1,
                            name='benchmark', row=1, col=1, legendgroup='performance', line={'color': 'gray'})
            fig.add_scatter(x=drawdowns.index, y=drawdowns.benchmark, name='benchmark - drawdown',
                            row=2, col=1, legendgroup='drawdown', line={'color': 'gray'})
            fig.add_scatter(x=performance_detail.index, y=diff(performance_detail.benchmark, 20),
                            fill='tozeroy', name='benchmark - month rolling return',
                            row=3, col=1, legendgroup='rolling performance', line={'color': 'rgba(0,0,0,0.2)'})

        fig.add_scatter(x=nstocks.index, y=nstocks, row=4,
                        col=1, name='nstocks', fill='tozeroy')
        fig.update_layout(legend={'bgcolor': 'rgba(0,0,0,0)'},
                          margin=dict(l=60, r=20, t=40, b=20),
                          height=600,
                          width=800,
                          xaxis4=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ]),
                x=0,
                y=1,
            ),
            rangeslider={'visible': True, 'thickness': 0.1},
            type="date",
        ),
            yaxis={'tickformat': ',.0%', },
            yaxis2={'tickformat': ',.0%', },
            yaxis3={'tickformat': ',.0%', },
        )
        return fig

    def upload(self, name=None, mae_mfe_charts=False):

        name = os.environ.get(
            'FINLAB_FORCED_STRATEGY_NAME', None) or name or '未命名'

        # calculate statistic values
        s = self.creturn.resample('1d').last().calc_stats()
        s.set_riskfree_rate(0.02)

        # drawdown_detail
        drawdown_details = s.drawdown_details.sort_values('Length').tail(5)
        drawdown_details['Start'] = drawdown_details['Start'].astype(
            str).str.split(' ').str[0]
        drawdown_details['End'] = drawdown_details['End'].astype(
            str).str.split(' ').str[0]
        drawdown_details = drawdown_details.set_index('Start').to_dict('index')

        # stats
        stats = s.stats.to_dict()
        stats['start'] = stats['start'].strftime('%Y-%m-%d')
        stats['end'] = stats['end'].strftime('%Y-%m-%d')

        # creturn
        if self.asset_type == 'crypto':
            return_ = self.creturn.resample(
                '1d').last().ffill().dropna().rebase()
        else:
            return_ = self.creturn.ffill().dropna().rebase()
        creturn = {'time': return_.index.astype(
            str).to_list(), 'value': return_.values.tolist()}

        # benchmark
        benchmark = self.get_benchmark()\
            .dropna().reindex(self.creturn.index, method='ffill')\
            .ffill().rebase().values.tolist()

        # return table
        return_table = s.return_table.transpose().to_dict()

        # ndays return
        ndays_return = {d: self.get_ndays_return(
            return_, d) for d in [1, 5, 10, 20, 60]}

        # mae_mfe_plotly_html
        from plotly.io import to_html
        fig = self.display_mae_mfe_analysis() if mae_mfe_charts else None
        mae_mfe_plotly_html = to_html(
            fig, full_html=False, include_plotlyjs='cdn') if fig else None

        d = {
            # backtest info
            'drawdown_details': drawdown_details,
            'stats': stats,
            'returns': creturn,
            'benchmark': benchmark,
            'ndays_return': ndays_return,
            'return_table': return_table,
            'fee_ratio': self.fee_ratio,
            'tax_ratio': self.tax_ratio,
            'trade_at': self.trade_at,
            'asset_type': self.asset_type,
            'mae_mfe_plotly_html': mae_mfe_plotly_html,

            # dates
            'update_date': self.update_date.strftime('%Y-%m-%d'),
            'last_trading_date': self.last_trading_date.strftime('%Y-%m-%d'),
            'next_trading_date': self.next_trading_date.strftime('%Y-%m-%d'),

            # key data
            'position': self.position_info(self.position),

            # public
            'public_performance': False,
            'public_code': False,
            'public_position': False,
        }

        payload = {'data': json.dumps(d),
                   'api_token': get_token(),
                   'collection': 'strategies',
                   'document_id': name}

        res = requests.post(
            'https://asia-east2-fdata-299302.cloudfunctions.net/write_database', data=payload).text

        try:
            return json.loads(res)
        except:
            return {'status': 'error', 'message': res}

    def position_info(self, position):

        # calculate lastest position changes
        diff = position.diff().abs().sum(axis=1)
        position_change_dates = diff.index[diff != 0]
        present_date = position_change_dates[-1] if len(
            position_change_dates) > 0 else position.index[0]
        previous_date = position_change_dates[-2] if len(
            position_change_dates) > 1 else position.index[0]
        p1 = position.loc[previous_date]
        p2 = position.loc[present_date]

        # record position changes
        status = pd.Series('持有', p2.index)
        status[(p1 == 0) & (p2 != 0)] = '買進'
        status[(p1 != 0) & (p2 == 0)] = '賣出'
        status = status[(p1 != 0) | (p2 != 0)].sort_values()

        # record present position weight
        weights = p2[status.index]

        # find entry dates
        entry_dates = {}
        for sid in status.index:
            has_position = (position[sid] != 0)
            first_day_enter_position = has_position & (
                ~has_position.shift(fill_value=False))
            first_day_enter_position = first_day_enter_position[first_day_enter_position].index[-1]
            entry_dates[sid] = first_day_enter_position.strftime('%Y-%m-%d')

        # find exit dates
        exit_dates = {}
        for sid, sstatus in status.items():
            if sstatus == '賣出':
                exit_dates[sid] = present_date.strftime('%Y-%m-%d')
            else:
                exit_dates[sid] = None

        # find return
        creturn = {}
        for sid in status.index:
            creturn[sid] = self.get_return(
                self.trade_at, sid, entry_dates[sid], exit_dates[sid])

        # data formation
        df = pd.DataFrame({'status': status, 'weight': weights,
                          'entry_date': entry_dates, 'exit_date': exit_dates, 'return': creturn})
        df.sort_values(['status', 'entry_date'], inplace=True)
        df['entry_date'] = df['entry_date'].fillna('')
        df['exit_date'] = df['exit_date'].fillna('')

        if self.asset_type == 'tw_stock':
            stock_names = self.get_stock_names()
            df.index = df.index + \
                df.index.map(lambda sid: stock_names.get(sid, ''))

        ret = df.to_dict('index')
        ret['update_date'] = self.update_date.strftime('%Y-%m-%d')
        ret['next_trading_date'] = self.next_trading_date.strftime('%Y-%m-%d')
        ret['trade_at'] = self.trade_at
        return ret

    @staticmethod
    def get_ndays_return(creturn, n):
        last_date_eq = creturn.iloc[-1]
        ref_date_eq = creturn.iloc[-1-n]
        return last_date_eq / ref_date_eq - 1

    def get_return(self, trade_at, stock_id, sdate, edate=None):

        price = self.get_price(trade_at, adj=True)

        utc = price.index.tzinfo is not None
        sdate = pd.to_datetime(sdate, utc=utc)
        edate = pd.to_datetime(edate, utc=utc)

        if stock_id not in price.columns:
            return 0

        if sdate >= price.index[-1]:
            return 0

        price = price[stock_id]

        # get start index
        if sdate in price.index:
            sdate = price.loc[sdate:].index[1]
        else:
            sdate = price.loc[sdate:].index[0]

        assert sdate in price.index
        sindex = price.index.get_loc(sdate)

        # get end index
        if edate is None or edate >= price.index[-1]:
            eindex = len(price) - 1
        elif edate in price.index:
            eindex = price.index.get_loc(edate) + 1
        else:
            edate = price.loc[edate:].index[0]
            eindex = price.index.get_loc(edate)

        evalue = np.nan
        while math.isnan(evalue) and eindex > -1:
            evalue = price.iloc[eindex]
            eindex -= 1

        svalue = np.nan
        while math.isnan(svalue) and sindex < len(price):
            svalue = price.iloc[sindex]
            sindex += 1

        return evalue / svalue - 1

    @allow_asset_types(['tw_stock'])
    def get_trade_record(self, time_scale=None, edge_ratio_series=False, edge_ratio_time_range=None, atr_freq=21):
        buy_signals = self.position > 0
        sig = buy_signals - (buy_signals.shift().fillna(0))

        # get trade entry & exit record
        record_set = []
        for stock_id in sig.columns:
            target_sig = sig[stock_id]
            posit_values = self.position[stock_id]
            entry_sig_date = target_sig[target_sig > 0].index
            exit_sig_date = target_sig[target_sig < 0].index
            target_positions = posit_values[posit_values > 0].values

            for entry, exit_, pos in zip(entry_sig_date, exit_sig_date, target_positions):
                trade_record = {'stock_id': stock_id, 'entry_sig_date': entry,
                                'exit_sig_date': exit_, 'position': pos}
                record_set.append(trade_record)

        df = pd.DataFrame(record_set)
        target_price = data.get(
            f'etl:adj_{self.trade_at}').ffill().shift(-1).dropna(how='all')
        atr_df = cal_atr(atr_freq).shift(-1).dropna(how='all')
        close_map = target_price.unstack().to_frame()
        close_map.index.names = ('stock_id', 'date')
        close_map.columns = ['target_price']

        # calculate fluctuation record
        def get_mae_mfe_price(stock_id, entry_sig_date, exit_sig_date, position=None, time_scale=None):
            result = {}
            if time_scale:
                price_period = target_price.loc[entry_sig_date:,
                                                stock_id].iloc[:time_scale]
                atr = atr_df.loc[entry_sig_date:,
                                 stock_id].iloc[:time_scale][-1]
            else:
                price_period = target_price.loc[entry_sig_date:exit_sig_date, stock_id]
                atr = atr_df.loc[entry_sig_date:exit_sig_date, stock_id][-1]
                mdd = abs(
                    round(((price_period / price_period.cummax() - 1) * 100).min(), 2))
                result['mdd'] = mdd

            mae_price = price_period.min()
            g_mfe_price = price_period.max()
            mae_price_index = price_period[price_period == mae_price]

            try:
                mae_price_index = mae_price_index.index[0]
                b_mfe_price = price_period[price_period.index <
                                           mae_price_index].max()
            except:
                b_mfe_price = np.nan

            if pd.isna(b_mfe_price):
                b_mfe_price = g_mfe_price

            result.update({'stock_id': stock_id, 'entry_sig_date': entry_sig_date, 'exit_sig_date': exit_sig_date,
                           'position': position, 'period': len(price_period), 'atr': atr,
                           'mae_price': mae_price, 'b_mfe_price': b_mfe_price, 'g_mfe_price': g_mfe_price})
            return result

        def get_fluctuation(time_scale=None):
            fluctuation = pd.DataFrame(
                [get_mae_mfe_price(time_scale=time_scale, *record[1]) for record in df.iterrows()])
            fluctuation = fluctuation.set_index(['stock_id', 'exit_sig_date'])
            fluctuation['exit_price'] = close_map['target_price']
            fluctuation = fluctuation.reset_index().set_index(
                ['stock_id', 'entry_sig_date'])
            fluctuation['entry_price'] = close_map['target_price']

            # get return
            for return_name, exit_col in [('return', 'exit_price'), ('mae_return', 'mae_price'),
                                          ('b_mfe_return', 'b_mfe_price'), ('g_mfe_return', 'g_mfe_price')]:
                fluctuation[return_name] = round(
                    ((fluctuation[exit_col] - self.tax_ratio * fluctuation[exit_col] - self.fee_ratio * (
                        fluctuation['entry_price'] + fluctuation[exit_col])) / fluctuation[
                        'entry_price'] - 1) * 100, 2)
                if return_name in ['mae_return']:
                    fluctuation[return_name] = abs(fluctuation[return_name])
                elif return_name in ['b_mfe_return', 'g_mfe_return']:
                    fluctuation[return_name] = fluctuation[return_name].apply(
                        lambda s: 0 if s < 0 else s)
                fluctuation[return_name] = fluctuation[return_name].apply(
                    lambda s: 0 if (np.isinf(s)) or (pd.isna(s)) else s)
            fluctuation['atr_return'] = round(
                fluctuation['atr'] / fluctuation['entry_price'] * 100, 2)
            fluctuation['edge_ratio'] = fluctuation['g_mfe_return'] / \
                fluctuation['mae_return']
            return fluctuation

        # edge_ratio series
        edge_ratio_dataset = None
        if edge_ratio_series:
            edge_ratio_dataset = []
            if edge_ratio_time_range is None:
                edge_ratio_time_range = range(2, 40, 3)
            for t in edge_ratio_time_range:
                fluctuation = get_fluctuation(time_scale=t)
                normal_g_mfe_return = fluctuation['g_mfe_return'] / \
                    fluctuation['atr_return']
                normal_g_mfe_return = normal_g_mfe_return[normal_g_mfe_return != np.inf]
                normal_mae_return = fluctuation['mae_return'] / \
                    fluctuation['atr_return']
                normal_mae_return = normal_mae_return[normal_mae_return != np.inf]
                mean_atr = fluctuation['atr_return'].mean()
                mean_value = normal_g_mfe_return.sum() / normal_mae_return.sum()
                edge_ratio_dataset.append(
                    {'time_scale': t, 'mean_edge_ratio': mean_value, 'mean_atr': mean_atr})

        # get entry_date & exit_date
        date_map = pd.DataFrame(
            {'date_map': target_price.index}, index=target_price.index).shift(-1)
        result = get_fluctuation(time_scale=time_scale)
        result = result.reset_index().set_index(['entry_sig_date'])
        result['entry_date'] = date_map['date_map']
        result = result.reset_index().set_index(['exit_sig_date'])

        result['exit_date'] = date_map['date_map']
        result = result.reset_index()

        # get security_categories
        security_categories = data.get('security_categories')
        result = result.merge(security_categories, how='left', on='stock_id')
        result['stock_id'] = result['stock_id'] + ' ' + result['name']
        trade_record_df = result.drop(columns=['index', 'name'])
        trade_record_df = trade_record_df[['entry_sig_date', 'exit_sig_date', 'entry_date', 'exit_date', 'stock_id',
                                           'market', 'category', 'entry_price', 'exit_price', 'g_mfe_return',
                                           'mae_price', 'b_mfe_price', 'return', 'mae_return', 'b_mfe_return',
                                           'g_mfe_price', 'mdd', 'position', 'period', 'atr',
                                           'atr_return', 'edge_ratio']]
        return trade_record_df, edge_ratio_dataset

    @allow_asset_types(['tw_stock'])
    def display_mae_mfe_analysis(self, plot_data=None, stop_loss=0, take_profit=0, edge_ratio=False,
                                 edge_ratio_time_range=None, atr_freq=21):
        import plotly.express as px
        import plotly.figure_factory as ff
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        from plotly.io import to_html
        try:
            if plot_data is None:
                trade_record, edge_ratio_series = self.get_trade_record(edge_ratio_time_range=edge_ratio_time_range,
                                                                        edge_ratio_series=edge_ratio,
                                                                        atr_freq=atr_freq)
            else:
                trade_record, edge_ratio_series = plot_data
            trade_record = trade_record.dropna()
            edge_ratio_series = pd.DataFrame(edge_ratio_series)
            stop_loss = abs(stop_loss * 100)
            take_profit = abs(take_profit * 100)
            colors = ['#69b0ea', '#F66095']
            trade_record['profit_loss'] = trade_record['return'].apply(
                lambda s: 'profit' if s > 0 else 'loss')
            trade_record['size'] = abs(trade_record['return'])

            fig = make_subplots(rows=6, cols=6,
                                specs=[[{"colspan": 6}, None, None, None, None, None],
                                       [{"colspan": 2, "secondary_y": True}, None, {"colspan": 2}, None, {"colspan": 2},
                                        None],
                                       [{"colspan": 2}, None, {"colspan": 2},
                                           None, {"colspan": 2}, None],
                                       [{"colspan": 2}, None, {"colspan": 2},
                                           None, {"colspan": 2}, None],
                                       [{"colspan": 3}, None, None, {
                                           "colspan": 3}, None, None],
                                       [{"colspan": 6}, None, None, None, None, None]],
                                vertical_spacing=0.06,
                                horizontal_spacing=0.1,
                                subplot_titles=("Return Hist",
                                                "Edge Ratio", "B_MFE/MAE", "G_MFE/MAE",
                                                "MAE/Return", "B_MFE/Return", "G_MFE/Return",
                                                "MAE Distplot", "B_MFE Distplot", "G_MFE Distplot",
                                                "MDD Distplot", "MDD/G_MFE",
                                                "Ratio Violin"))

            def set_f_data_color(fig_data, color_set=None):
                if color_set is None:
                    color_set = colors
                if fig_data['legendgroup'] == 'profit':
                    fig_data['marker']['color'] = color_set[0]
                elif fig_data['legendgroup'] == 'loss':
                    fig_data['marker']['color'] = color_set[1]
                else:
                    fig_data['marker']['color'] = color_set[0]
                return fig_data

            # "Return Hist"
            fig_return_hist = px.histogram(
                trade_record, x="return", color="profit_loss")
            return_mean = round(trade_record['return'].mean(), 2)
            win_ratio = round(sum(
                trade_record['profit_loss'] == 'profit') / len(trade_record['profit_loss']) * 100, 2)

            for f_data in fig_return_hist.data:
                fig.add_trace(set_f_data_color(f_data), row=1, col=1)

            fig.add_vline(x=return_mean, line_width=3, line_dash="dash", line_color="green",
                          annotation_position="top left",
                          annotation_text=f'avg_return:{return_mean}', row=1, col=1)
            fig.add_vline(x=win_ratio, line_width=3, line_dash="dash", line_color="purple",
                          annotation_position="top right",
                          annotation_text=f'win_ratio:{win_ratio}', row=1, col=1)

            # "Edge Ratio"
            if edge_ratio_series.empty is False:
                fig_edge_ratio_hist = px.bar(
                    edge_ratio_series, x='time_scale', y='mean_edge_ratio')
                fig_atr_line = px.line(
                    edge_ratio_series, x='time_scale', y='mean_atr')

                for f_data in fig_edge_ratio_hist.data:
                    fig.add_trace(set_f_data_color(f_data), row=2, col=1)

                for f_data in fig_atr_line.data:
                    fig.add_trace(f_data, row=2, col=1, secondary_y=True)

                fig.add_hline(y=1, line_width=3, line_color="orange",
                              annotation_text='benchmark', row=2, col=1)

            # "B_MFE/MAE", "G_MFE/MAE"
            # add sl_tp rect
            for n in [3, 5]:
                fig.add_shape(type="rect",
                              x0=0, y0=0, x1=stop_loss, y1=take_profit,
                              line=dict(
                                  color="#55701c",
                                  width=2,
                              ),
                              fillcolor="PaleTurquoise",
                              opacity=0.5,
                              row=2, col=n
                              )
            fig_mae_b_mfe = px.scatter(trade_record, x="mae_return", y="b_mfe_return", color="profit_loss",
                                       size='size', hover_data=['stock_id', 'return', 'category'])

            for f_data in fig_mae_b_mfe.data:
                fig.add_trace(set_f_data_color(f_data), row=2, col=3)

            fig_mae_g_mfe = px.scatter(trade_record, x="mae_return", y="g_mfe_return", color="profit_loss",
                                       size='size', hover_data=['stock_id', 'return', 'category'])
            for f_data in fig_mae_g_mfe.data:
                fig.add_trace(set_f_data_color(f_data), row=2, col=5)

            # "MAE/Return","B_MFE/Return","G_MFE/Return",
            fig_mae_return = px.scatter(trade_record, x="return", y="mae_return", color="profit_loss",
                                        size='size', hover_data=['stock_id', 'category'])

            for f_data in fig_mae_return.data:
                fig.add_trace(set_f_data_color(f_data), row=3, col=1)

            fig_b_mfe_return = px.scatter(trade_record, x="return", y="b_mfe_return", color="profit_loss",
                                          size='size', hover_data=['stock_id', 'category'])
            for f_data in fig_b_mfe_return.data:
                fig.add_trace(set_f_data_color(f_data), row=3, col=3)

            fig_g_mfe_return = px.scatter(trade_record, x="return", y="g_mfe_return", color="profit_loss",
                                          size='size', hover_data=['stock_id', 'category'])
            for f_data in fig_g_mfe_return.data:
                fig.add_trace(set_f_data_color(f_data), row=3, col=5)

            # add sl_tp rect & auxiliary line
            for n in [1, 3, 5]:
                max_return = trade_record['return'].max()
                min_return = trade_record['return'].min()
                if n == 1:
                    x0 = -stop_loss
                    y0 = 0
                    x1 = max_return
                    y1 = stop_loss
                    aux_line_end_x = min_return
                    aux_line_end_y = abs(min_return)
                else:
                    x0 = min_return
                    y0 = 0
                    x1 = take_profit
                    y1 = take_profit
                    aux_line_end_x = max_return
                    aux_line_end_y = max_return

                fig.add_trace(go.Scatter(x=[0, aux_line_end_x * 1.1], y=[0, aux_line_end_y * 1.1],
                                         mode='lines', name='aux_line'), row=3, col=n)

                fig.add_shape(type="rect",
                              x0=x0, y0=y0, x1=x1, y1=y1,
                              line=dict(
                                  color="#55701c",
                                  width=2,
                              ),
                              fillcolor="PaleTurquoise",
                              opacity=0.5,
                              row=3, col=n
                              )

            # "MAE Distplot","B_MFE Distplot","G_MFE Distplot"
            win_df = trade_record[trade_record['profit_loss'] == 'profit']
            loss_df = trade_record[trade_record['profit_loss'] == 'loss']
            group_labels = ['profit', 'loss']

            fig_mae_distplot = ff.create_distplot([win_df['mae_return'].values, loss_df['mae_return'].values],
                                                  group_labels,
                                                  bin_size=2, colors=colors)
            for f_data in fig_mae_distplot.data:
                fig.add_trace(f_data, row=4, col=1)

            fig_b_mfe_distplot = ff.create_distplot([win_df['b_mfe_return'].values, loss_df['b_mfe_return'].values],
                                                    group_labels, bin_size=2, colors=colors)
            for f_data in fig_b_mfe_distplot.data:
                fig.add_trace(f_data, row=4, col=3)

            fig_g_mfe_distplot = ff.create_distplot([win_df['g_mfe_return'].values, loss_df['g_mfe_return'].values],
                                                    group_labels, bin_size=2, colors=colors)
            for f_data in fig_g_mfe_distplot.data:
                fig.add_trace(f_data, row=4, col=5)

            for i, n in zip([1, 3, 5], ['mae_return', 'b_mfe_return', 'g_mfe_return']):
                mean_value = round(trade_record[n].mean(), 2)
                fig.add_vline(x=mean_value, line_width=3, line_dash="dash", line_color="purple",
                              annotation_position="top right",
                              annotation_text=f'mean:{mean_value}', row=4, col=i)

            # mdd
            fig_g_mfe_distplot = ff.create_distplot([win_df['mdd'].values, loss_df['mdd'].values],
                                                    group_labels, bin_size=2, colors=colors)
            for f_data in fig_g_mfe_distplot.data:
                fig.add_trace(f_data, row=5, col=1)
            mdd_mean = round(trade_record['mdd'].mean(), 2)
            fig.add_vline(x=mdd_mean, line_width=3, line_dash="dash", line_color="purple",
                          annotation_position="top right",
                          annotation_text=f'mdd_mean:{mdd_mean}', row=5, col=1)

            fig_mdd_g_mfe = px.scatter(trade_record, x="g_mfe_return", y="mdd", color="profit_loss",
                                       size='size', hover_data=['stock_id', 'return', 'category'])
            for f_data in fig_mdd_g_mfe.data:
                fig.add_trace(set_f_data_color(f_data), row=5, col=4)
            aux_line_end = trade_record['g_mfe_return'].max()
            fig.add_trace(go.Scatter(x=[0, aux_line_end * 1.01], y=[0, aux_line_end * 1.01],
                                     mode='lines', name='aux_line'), row=5, col=4)

            # violin
            tr_melt_df = pd.melt(trade_record, id_vars=['entry_sig_date', 'exit_sig_date', 'stock_id', 'profit_loss'],
                                 value_vars=['return', 'mae_return', 'b_mfe_return', 'g_mfe_return', 'mdd'])

            for group, color in zip(['profit', 'loss'], colors):
                fig.add_trace(go.Violin(x=tr_melt_df['variable'][tr_melt_df['profit_loss'] == group],
                                        y=tr_melt_df['value'][tr_melt_df['profit_loss']
                                                              == group], line_color=color,
                                        legendgroup=group, scalegroup=group, name=group, box_visible=True,
                                        meanline_visible=True,
                                        fillcolor=color, opacity=0.6), row=6, col=1
                              )

            fig.update_layout(
                height=1750, width=1350,
                violinmode='group',
                title_text="MAE/MFE Analysis",
                yaxis=dict(
                    title='count',
                ),
                yaxis2=dict(
                    title='edge ratio',
                    showgrid=False,
                ),
                yaxis3=dict(
                    title='volatility',
                ),
                yaxis4=dict(
                    title='b_mfe(%)',
                ),
                yaxis5=dict(
                    title='g_mfe(%)',
                ),
                yaxis6=dict(
                    title='mae(%)',
                ),
                yaxis7=dict(
                    title='b_mfe(%)',
                ),
                yaxis8=dict(
                    title='g_mfe(%)',
                ),
                yaxis13=dict(
                    title='mdd(%)',
                ),
                yaxis14=dict(
                    title='return(%)',
                ),
                xaxis=dict(
                    title='return(%)',
                ),
                xaxis2=dict(
                    title='time_scale',
                ),
                xaxis3=dict(
                    title='mae(%)',
                ),
                xaxis4=dict(
                    title='mae(%)',
                ),
                xaxis5=dict(
                    title='return(%)',
                ),
                xaxis6=dict(
                    title='return(%)',
                ),
                xaxis7=dict(
                    title='return(%)',
                ),
                xaxis8=dict(
                    title='mae(%)',
                ),
                xaxis9=dict(
                    title='b_mfe(%)',
                ),
                xaxis10=dict(
                    title='g_mfe(%)',
                ),
                xaxis11=dict(
                    title='mdd(%)',
                ),
                xaxis12=dict(
                    title='g_mfe(%)',
                ),
            )
        except Exception as e:
            logger.error(e)
            fig = None
        return fig


def cal_atr(time_period=14):
    adj_close = data.get('etl:adj_close').ffill()
    adj_high = data.get('etl:adj_high').ffill()
    adj_low = data.get('etl:adj_low').ffill()
    tr_cond1 = (adj_high-adj_low).unstack()
    tr_cond2 = abs(adj_close.shift()-adj_high).unstack()
    tr_cond3 = abs(adj_close.shift()-adj_low).unstack()
    tr_df = pd.concat([tr_cond1, tr_cond2, tr_cond3],
                      axis=1).max(axis=1).unstack(level=0)
    atr_df = tr_df.rolling(time_period, min_periods=int(time_period/2)).mean()
    return atr_df
