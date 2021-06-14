import psycopg2
import psycopg2.extras
from dateutil.relativedelta import relativedelta
import datetime
import pandas as pd
import numpy as np
from qry_fltexprev import QryClass

# Connection parameters
host = 'localhost'
port = 5432
database = 'test'
user = "postgres"
password = "postgres"

# Execution date
exedat = datetime.datetime.now()
delta_4W = relativedelta(days=-28)
delta_1Y = relativedelta(years=-1)

# Specify Execution date
# exedat = datetime.date(2021,6,10)

# Create and Load FRP queries
qryObj = QryClass(exedat)


def get_Connection(host, port, database, user, password):
    conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
    return conn


def pop_Segrto(con, bkgdta):
    tbl_col_lst = ['cmpcod', 'exedat', 'fltnum', 'segorg', 'segdst', 'sumchgwgtseg', 'sumchgwgtflt', 'rto', 'datper',
                   'crmlstupdtim', 'fltrou']
    try:
        cur_date = exedat.strftime('%Y-%m-%d')
        print(cur_date)
        # Get Segment list
        his_dat_4W = exedat + delta_4W
        qry_segrto_seglst = qryObj.query_FRP["qry_segrto_seglst"]
        # print(qry_segrto_4w)
        df_segrto_seglst = pd.read_sql_query(qry_segrto_seglst, con, parse_dates=['fltdat']).convert_dtypes()
        bkg_ind_1 = bkgdta.set_index(["cmpcod", "fltnum", "segorg", "segdst", "fltrou"]).index
        segrto_ind_1 = df_segrto_seglst.set_index(["cmpcod", "fltnum", "segorg", "segdst", "fltrou"]).index
        # Booking data required for segrto calculation
        bkgdta_segrto = bkgdta[bkg_ind_1.isin(segrto_ind_1)]
        # print('Segment count =',len(bkgdta_segrto))

        # 4 weeks check
        seg_collst = ["cmpcod", "fltnum", "segorg", "segdst", "fltrou"]
        bkgdta_segrto_4W = bkgdta_segrto[bkgdta_segrto["fltdat"] >= np.datetime64(his_dat_4W)]
        bkgdta_segrto_4W = bkgdta_segrto_4W[["cmpcod", "fltnum", "segorg", "segdst", "fltrou", "fltdat", "chgwgt"]]
        tmp_4W = df_segrto_seglst[seg_collst]

        bkgdta_4W_sumseg = bkgdta_segrto_4W.groupby(["cmpcod", "fltnum", "segorg", "segdst"])[
            'chgwgt'].sum().reset_index()
        bkgdta_4W_sumflt = bkgdta_segrto_4W.groupby(["cmpcod", "fltnum"])['chgwgt'].sum().reset_index()
        tmp_4W = tmp_4W.join(bkgdta_4W_sumseg.set_index(['cmpcod', 'fltnum', 'segorg', 'segdst']),
                             on=['cmpcod', 'fltnum', 'segorg', 'segdst'],
                             lsuffix='', rsuffix='_sumseg')
        tmp_4W = tmp_4W.join(bkgdta_4W_sumflt.set_index(["cmpcod", "fltnum"]), on=["cmpcod", "fltnum"],
                             lsuffix='', rsuffix='_sumflt')
        tmp_4W.loc[:, 'rto'] = tmp_4W['chgwgt'] / tmp_4W['chgwgt_sumflt']

        tmp_4W.loc[:, 'sumchgwgtflt'] = tmp_4W['chgwgt_sumflt']
        tmp_4W.loc[:, 'sumchgwgtseg'] = tmp_4W['chgwgt']
        tmp_4W.loc[:, 'datper'] = '4W'
        values = {'sumchgwgtflt': 0, 'sumchgwgtseg': 0, 'rto': 0}
        tmp_4W = tmp_4W.fillna(value=values)

        seglst_ind = df_segrto_seglst.set_index(["cmpcod", "fltnum", "fltrou"]).index

        # List of flights for which atleast 1 segment value was identified by 4W check
        segrto_ind_4W = tmp_4W[tmp_4W['rto'] > 0].set_index(["cmpcod", "fltnum", "fltrou"]).index
        '''Remove flights for which segrto could not be identified in 4W check'''
        tmp_4W_ind = tmp_4W.set_index(["cmpcod", "fltnum", "fltrou"]).index
        tmp_4W = tmp_4W[tmp_4W_ind.isin(segrto_ind_4W)]

        # 1 year check
        his_dat_1Y = exedat + delta_1Y
        bkgdta_segrto_1Y = bkgdta_segrto[bkgdta_segrto["fltdat"] >= np.datetime64(his_dat_1Y)]
        bkgdta_segrto_1Y = bkgdta_segrto_1Y[["cmpcod", "fltnum", "segorg", "segdst", "fltrou", "fltdat", "chgwgt"]]
        bkg_ind_2 = bkgdta_segrto_1Y.set_index(["cmpcod", "fltnum", "fltrou"]).index
        '''Consider only flights for which value of not even 1 segment could be found in 4 weeks check'''
        bkgdta_segrto_1Y = bkgdta_segrto_1Y[~bkg_ind_2.isin(segrto_ind_4W)]

        tmp_1Y = df_segrto_seglst[~seglst_ind.isin(segrto_ind_4W)]
        tmp_1Y = tmp_1Y[seg_collst]
        bkgdta_1Y_sumseg = bkgdta_segrto_1Y.groupby(["cmpcod", "fltnum", "segorg", "segdst"])[
            'chgwgt'].sum().reset_index()
        bkgdta_1Y_sumflt = bkgdta_segrto_1Y.groupby(["cmpcod", "fltnum"])['chgwgt'].sum().reset_index()
        tmp_1Y = tmp_1Y.join(bkgdta_1Y_sumseg.set_index(['cmpcod', 'fltnum', 'segorg', 'segdst']),
                             on=['cmpcod', 'fltnum', 'segorg', 'segdst'],
                             lsuffix='', rsuffix='_sumseg')
        tmp_1Y = tmp_1Y.join(bkgdta_1Y_sumflt.set_index(["cmpcod", "fltnum"]), on=["cmpcod", "fltnum"],
                             lsuffix='', rsuffix='_sumflt')
        tmp_1Y.loc[:, 'rto'] = tmp_1Y['chgwgt'] / tmp_1Y['chgwgt_sumflt']

        tmp_1Y.loc[:, 'sumchgwgtflt'] = tmp_1Y['chgwgt_sumflt']
        tmp_1Y.loc[:, 'sumchgwgtseg'] = tmp_1Y['chgwgt']
        tmp_1Y.loc[:, 'datper'] = '1Y'
        values = {'sumchgwgtflt': 0, 'sumchgwgtseg': 0, 'rto': 0}
        tmp_1Y = tmp_1Y.fillna(value=values)
        # List of flights for which atleast 1 segment value was identified by 1Y check
        segrto_ind_1Y = tmp_1Y[tmp_1Y['rto'] > 0].set_index(["cmpcod", "fltnum", "fltrou"]).index
        '''Remove flights for which segrto could not be identified in 4W check'''
        tmp_1Y_ind = tmp_1Y.set_index(["cmpcod", "fltnum", "fltrou"]).index
        tmp_Eql = tmp_1Y[~tmp_1Y_ind.isin(segrto_ind_1Y)]
        tmp_1Y = tmp_1Y[tmp_1Y_ind.isin(segrto_ind_1Y)]
        tmp_Eql = tmp_Eql[seg_collst]
        tmp_Eql.loc[:, 'segcnt'] = 0
        tmp_Eql['segcnt'] = tmp_Eql.groupby(["cmpcod", "fltnum", "fltrou"]).transform('count')
        tmp_Eql['rto'] = 1 / tmp_Eql['segcnt']

        tmp_Eql.loc[:, 'sumchgwgtflt'] = 0
        tmp_Eql.loc[:, 'sumchgwgtseg'] = 0
        tmp_Eql.loc[:, 'datper'] = 'EQL'

        tmp_Eql = tmp_Eql.fillna(value=values)

        segrto_out = tmp_4W.append([tmp_1Y, tmp_Eql])
        segrto_out.loc[:, 'exedat'] = cur_date
        segrto_out.loc[:, 'crmlstupdtim'] = datetime.datetime.now().strftime('%d-%b-%Y %H:%M:%S')
        segrto_out = segrto_out[tbl_col_lst]

        print('Output:\nsegrto_out.head=\n', segrto_out.head())
        print('segrto_out.columns=\n', segrto_out.columns)
        print('segrto_out.count=\n', len(segrto_out))

    except Exception as e:
        print("Exception in pop_Segrto() : " + str(e))
    finally:
        print("Exiting pop_Segrto()")


print("Outside main")

try:
    print("Inside main")
    print(qryObj.query_FRP)
    # Load 1 year Booking data
    qry_bkg_1Y = qryObj.query_FRP["qry_bkg_1Y"]
    conn = get_Connection(host, port, database, user, password)
    df_bkg = pd.read_sql_query(qry_bkg_1Y, conn, parse_dates=['fltdat']).convert_dtypes()
    print("1Y Booking record count: ", len(df_bkg))

    pop_Segrto(conn, df_bkg)
except Exception as e:
    print("Error in main: " + str(e))
