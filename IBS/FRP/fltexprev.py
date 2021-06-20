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

# General Parameters
genPar = {
    "cmpcod": 'KE',
    "fltcaridr": 1180,
    "trf_grpcatcod": 'TARIFF',
    "min_dcp": 7,
    "sys_curcod": 'USD'
}
# PFM data
df_PFM = pd.DataFrame()

# Output table
output_tblnam = "crmfltexprevfct"
output_tbl_col = ['cmpcod', 'fltnum', 'fltdat', 'segorg', 'segdst', 'awborg', 'awbdst', 'awborgcty', 'awbdstcty',
                  'awborgcnt', 'awbdstcnt', 'awborgreg', 'awbdstreg', 'altidr', 'prdnam', 'gblcuscod', 'catcod',
                  'stncod', 'dow', 'chgwgtfrm', 'chgwgttoo', 'rectyp', 'ratusd', 'othchg', 'fltdmd', 'segprofct',
                  'prdprofct', 'segaltwgt', 'segprdclswgt', 'clswgtper', 'clswgt', 'revusd', 'contrbrto', 'flttyp',
                  'fltrou', 'fltorg', 'fltdst', 'exedat', 'tagidx', 'crmflg', 'crmlstupdtim', 'clsgrswgt', 'clsvolwgt']
output_tbl_pk = ['cmpcod', 'fltnum', 'fltdat', 'segorg', 'segdst', 'awborg', 'awbdst', 'altidr', 'prdnam', 'stncod']

# Execution date
exedat = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
delta_4W = relativedelta(days=-28)
delta_1Y = relativedelta(years=-1)

# Specify Custom Execution date
exedat = datetime.datetime(2021, 6, 10)

cur_date = exedat.strftime('%Y-%m-%d')
forcstfrmdat = exedat + relativedelta(days=1)  # Next day
forcsttoodat = datetime.datetime(int(exedat.strftime('%Y')), int(exedat.strftime('%m')), 1) + relativedelta(
    months=2) + relativedelta(days=-1)  # Last day of next month
print("Execution date=", exedat)
print("Forecast period Start date=", forcstfrmdat)
print("Forecast period End date=", forcsttoodat)

# Create and Load FRP queries
qryObj = QryClass(exedat, genPar)


def get_Connection(host, port, database, user, password):
    conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
    return conn


def clear_postgre_tbl(tblnam, conn):
    qry = "TRUNCATE TABLE " + str(tblnam)
    curr = conn.cursor()
    curr.execute(qry)
    conn.commit()
    print("Executed:" + qry)
    curr.close()


def clear_oldresult(rectyp, frmdat, toodat):
    conn = get_Connection(host, port, database, user, password)
    frmdat = pd.to_datetime(frmdat).strftime('%Y-%m-%d')
    toodat = pd.to_datetime(toodat).strftime('%Y-%m-%d')
    qry = "DELETE FROM " + output_tblnam + " WHERE RECTYP='" + rectyp + "' AND FLTDAT BETWEEN TO_DATE('" + frmdat + "','YYYY-MM-DD') AND TO_DATE('" + toodat + "','YYYY-MM-DD')"
    curr = conn.cursor()
    curr.execute(qry)
    conn.commit()
    print("Executed:" + qry)
    curr.close()
    conn.close()


def write_to_postgre(df, index, tblnam):
    conn = get_Connection(host, port, database, user, password)
    if len(df) > 0:
        df = df.set_index(index)
        pk = ','.join(list(df.index.names))
        col1 = ','.join(list(df.columns))
        col2 = ','.join(list(['EXCLUDED.' + str(col) for col in df.columns]))
        df = df.reset_index()
        tuples = [tuple(x) for x in df.to_numpy()]
        cols = ','.join(list(df.columns))
        vals = ','.join(list(['%s' for i in range(len(df.columns))]))
        qry = "INSERT INTO %s(%s) VALUES(%s) ON CONFLICT(%s) DO UPDATE SET (%s) = (%s)" % (
            tblnam, cols, vals, pk, col1, col2)
        print("qry=", qry)
    cursor = conn.cursor()
    try:
        psycopg2.extras.execute_batch(cursor, qry, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as e:
        result_exception = str(e)
        print("Error: ", result_exception)
        conn.rollback()
    finally:
        cursor.close()


def get_gen_paramters():
    conn = get_Connection(host, port, database, user, password)
    qry_AWM = qryObj.query_FRP["qry_awm"]
    qry_density_factor = qryObj.query_FRP["qry_density_factor"]
    qry_dow_start = qryObj.query_FRP["qry_dow_start"]

    awm = float(pd.read_sql_query(qry_AWM, conn)['awm'])
    density_factor = float(pd.read_sql_query(qry_density_factor, conn)['densityfactor'])
    dow_start = int(pd.read_sql_query(qry_dow_start, conn)['dowstr'])

    genPar['awm'] = awm
    genPar['density_factor'] = density_factor
    genPar['dow_start'] = dow_start
    print("General parameters : ", genPar)


def pop_Segrto(bkgdta):
    con = get_Connection(host, port, database, user, password)
    tbl_col_lst = ['cmpcod', 'exedat', 'fltnum', 'segorg', 'segdst', 'sumchgwgtseg', 'sumchgwgtflt', 'rto', 'datper',
                   'crmlstupdtim', 'fltrou']
    tblnam = "crmfltexprevfctsegrto"
    histblnam = "crmfltexprevfctsegrtohis"
    tbl_pk = ["cmpcod", "fltnum", "segorg", "segdst"]
    try:
        # Get Segment list
        his_dat_4W = exedat + delta_4W
        qry_segrto_seglst = qryObj.query_FRP["qry_segrto_seglst"]
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

        # print('Output:\nsegrto_out.head=\n', segrto_out[segrto_out['datper'] == 'EQL'].head())
        # print('segrto_out.columns=\n', segrto_out.columns)
        # print('segrto_out.count=\n', len(segrto_out))

        clear_postgre_tbl(tblnam, conn)
        write_to_postgre(segrto_out, tbl_pk, tblnam)

        # Insert into history table
        qry_segrto_hisvernum = qryObj.query_FRP['qry_segrto_hisvernum']
        vernum = int(pd.read_sql_query(qry_segrto_hisvernum, con).convert_dtypes()['vernum'])
        segrto_out.loc[:, 'vernum'] = vernum
        tbl_pk.append("vernum")
        write_to_postgre(segrto_out, tbl_pk, histblnam)


    except Exception as e:
        print("Exception in pop_Segrto() : " + str(e))
    finally:
        con.close()
        print("Exiting pop_Segrto()")


def get_PFM_OD(orgcod, dstcod):
    v_pfm = -1
    if len(df_PFM) <= 0:
        get_PFM()
    tmp_PFM = df_PFM[(df_PFM["orgcod"] == orgcod) & (df_PFM["dstcod"] == dstcod)]['profct']
    if len(tmp_PFM) > 0:
        v_pfm = float(tmp_PFM.iloc[0])
    return v_pfm


def get_PFM():
    con = get_Connection(host, port, database, user, password)
    qry_pfm = qryObj.getQry_PFM()
    tmp_pfm = pd.read_sql_query(qry_pfm, con).convert_dtypes()
    if len(tmp_pfm) >= 0:
        global df_PFM
        df_PFM = tmp_pfm
        df_PFM.set_index(["orgcod", "dstcod"])
    con.close()


def get_Contrbrto(segorg, segdst, traorg, tradst):
    if not segorg:
        segorg = "-"
    if not segdst:
        segdst = "-"
    if not traorg:
        traorg = "-"
    if not tradst:
        tradst = "-"
    v_pfm_s1 = 0
    v_pfm_s2 = 0
    v_pfm_s3 = 0
    awm = genPar['awm']
    v_pfm_s1 = 0 if traorg == segorg else get_PFM_OD(traorg, segorg)
    v_pfm_s2 = 0 if segorg == segdst else get_PFM_OD(segorg, segdst)
    v_pfm_s3 = 0 if segdst == tradst else get_PFM_OD(segdst, tradst)
    if v_pfm_s1 == -1 or v_pfm_s2 == -1 or v_pfm_s3 == -1:
        contrbrto = 0
    else:
        v_pfm_s1 = 0 if v_pfm_s1 == 0 else v_pfm_s1 + awm
        v_pfm_s2 = 0 if v_pfm_s2 == 0 else v_pfm_s2 + awm
        v_pfm_s3 = 0 if v_pfm_s3 == 0 else v_pfm_s3 + awm
        contrbrto = v_pfm_s2 / (v_pfm_s1 + v_pfm_s2 + v_pfm_s3)
    return contrbrto


def get_cgocap(fltnum, fltdat, conn):
    density_factor = genPar['density_factor']
    qry_cgocap = qryObj.getQry_Cgocap(fltnum, fltdat, density_factor)
    cgocap = float(pd.read_sql_query(qry_cgocap, conn).convert_dtypes()['cgocapwgt'])
    return cgocap


def get_dow(pi_dat):
    genPar['dow_start']
    inp_dow = int(pi_dat.strftime('%w')) + 1
    dow = 7 if np.mod(inp_dow - int(genPar['dow_start']), 7) + 1 == 0 else np.mod(inp_dow - int(genPar['dow_start']),
                                                                                  7) + 1
    return dow


def create_alt_gblcus(df_bkg):
    rectyp = 'ALTGBLCUS'
    try:
        conn = get_Connection(host, port, database, user, password)
        qry_ins_AltGblcus = qryObj.getQry_ins_AltGblcus(forcstfrmdat, forcsttoodat)
        df_altlst_gblcus = pd.read_sql_query(qry_ins_AltGblcus, conn, parse_dates=['fltdat']).convert_dtypes()

        df_altlst_gblcus['dow'] = df_altlst_gblcus['fltdat'].apply(get_dow)
        df_altlst_gblcus.loc[:, 'chgwgtfrm'] = 0
        df_altlst_gblcus.loc[:, 'rectyp'] = rectyp
        df_altlst_gblcus.loc[:, 'chgwgttoo'] = 0
        df_altlst_gblcus.loc[:, 'exedat'] = cur_date
        df_altlst_gblcus.loc[:, 'crmlstupdtim'] = datetime.datetime.now().strftime('%d-%b-%Y %H:%M:%S')

        # Default values for fillna
        def_values = {
            'cmpcod': genPar['cmpcod'], 'segorg': "-", 'segdst': "-", 'awborg': "-", 'awbdst': "-", 'awborgcty': "-",
            'awbdstcty': "-",
            'awborgcnt': "-", 'awbdstcnt': "-", 'awborgreg': "-", 'awbdstreg': "-", 'altidr': "-", 'chgwgtfrm': 0,
            'chgwgttoo': 0, 'ratusd': -1, 'othchg': -1, 'fltdmd': -1, 'segprofct': -1,
            'prdprofct': -1, 'segaltwgt': 0, 'segprdclswgt': 0, 'clswgtper': -1, 'clswgt': -1, 'revusd': -1,
            'contrbrto': 1, 'tagidx': 0, 'crmflg': "I", 'clsgrswgt': 0, 'clsvolwgt': 0
        }
        df_altlst_gblcus = df_altlst_gblcus.fillna(value=def_values)

        # print('Global customer allotment list:\ndf_altlst_gblcus.head=\n', df_altlst_gblcus.head())
        # print('df_altlst_gblcus.columns=\n', df_altlst_gblcus.columns)
        # print('df_altlst_gblcus.count=\n', len(df_altlst_gblcus))

        # Clear pervious execution overlap records from output table
        df_altlst_gblcus = df_altlst_gblcus[output_tbl_col]
        clear_oldresult(rectyp, forcstfrmdat, forcsttoodat)
        #Write GBLCUS allotment list to output table
        write_to_postgre(df_altlst_gblcus, output_tbl_pk, output_tblnam)

        # Find net rate and other charge

        qry_alt_gblcus_netrat = qryObj.query_FRP['qry_alt_gblcus_netrat']
        # print("qry_alt_gblcus_netrat=", qry_alt_gblcus_netrat)
        df_alt_gblcus_rat = pd.read_sql_query(qry_alt_gblcus_netrat, conn, parse_dates=['fltdat']).convert_dtypes()
        if len(df_alt_gblcus_rat) > 0:
            df_alt_gblcus_rat.loc[:, 'rectyp'] = rectyp
            df_alt_gblcus_rat.fillna(value={"ratusd": 0})
            ind = ["cmpcod", "fltnum", "fltdat", "altidr", "stncod", "exedat", "rectyp"]
            df_altlst_gblcus.drop(['ratusd'])
            df_altlst_gblcus = df_altlst_gblcus.merge(df_alt_gblcus_rat, on=ind, how='left')
            df_altlst_gblcus = df_altlst_gblcus[output_tbl_col]

            # print('Global customer allotment list:\ndf_altlst_gblcus.head=\n',
            #       df_altlst_gblcus[["fltnum", "fltdat", "segorg", "segdst", "awborg", "awbdst", "ratusd"]].head())
            # print('df_altlst_gblcus.columns=\n', df_altlst_gblcus.columns)
            # print('df_altlst_gblcus.count=\n', len(df_altlst_gblcus))

        else:
            print("Cannot find ALT - GBLCUS rate cards!!!")

        # Find rate from historical data for allotments with traorg and tradst as null

        tmp_altlst = df_altlst_gblcus[(df_altlst_gblcus["awborg"] == "-") & (df_altlst_gblcus["awbdst"] == "-")][
            'altidr'].unique()
        if len(tmp_altlst) > 0:
            last_month_start = datetime.datetime(int(exedat.strftime('%Y')), int(exedat.strftime('%m')),
                                                 1) + relativedelta(months=-2) + relativedelta(days=1)
            last_month_end = datetime.datetime(int(exedat.strftime('%Y')), int(exedat.strftime('%m')),
                                               1) + relativedelta(days=-1)
            df_bkg_1M = df_bkg.loc[(df_bkg['fltdat'] >= last_month_start) & (df_bkg['fltdat'] <= last_month_end)]
            df_bkg_1M = df_bkg_1M[df_bkg_1M['altidr'].isin(tmp_altlst)]
            df_bkg_1M['contrbrto'] = df_bkg_1M.apply(
                lambda x: get_Contrbrto(x['segorgcty'], x['segdstcty'], x['awborgcty'], x['awbdstcty']), axis=1)
            df_bkg_1M["grsrev"] = (df_bkg_1M["grsrevusdshp"] - (df_bkg_1M["fltratusd"] * df_bkg_1M["chgwgt"])) * \
                                  df_bkg_1M["contrbrto"]
            tmp_sumrev = df_bkg_1M.groupby(["cmpcod", "fltnum", "segorg", "segdst", "gblcuscod"])[
                'grsrev'].sum().reset_index()
            tmp_sumchgwgt = df_bkg_1M.groupby(["cmpcod", "fltnum", "segorg", "segdst", "gblcuscod"])[
                'chgwgt'].sum().reset_index()
            tmp_alt = df_altlst_gblcus[
                (df_altlst_gblcus["awborg"] == "-") & (df_altlst_gblcus["awbdst"] == "-")].set_index(
                ["cmpcod", "fltnum", "segorg", "segdst", "gblcuscod"])
            tmp_alt.loc[:, 'ratusd'] = tmp_sumrev["grsrev"] / tmp_sumchgwgt["chgwgt"]




    except Exception as e:
        print("Exception in create_alt_gblcus() : " + str(e))
    finally:
        conn.close()
        print("Exiting create_alt_gblcus()")


def create_alt_prd(df_bkg):
    pass


if __name__ == '__main__':
    try:
        print("Inside main")
        get_gen_paramters()
        # Load 1 year Booking data
        qry_bkg_1Y = qryObj.query_FRP["qry_bkg_1Y"]
        print(qry_bkg_1Y)
        conn = get_Connection(host, port, database, user, password)
        df_bkg = pd.read_sql_query(qry_bkg_1Y, conn, parse_dates=['fltdat']).convert_dtypes()
        df_bkg = df_bkg.fillna({"segorgcty": "-", "segdstcty": "-", "awborgcty": "-", "awbdstcty": "-"})
        print("1Y Booking record count: ", len(df_bkg))
        # Populate Segment ratio table
        pop_Segrto(df_bkg)
        # Populate Global customer allotment in output table
        create_alt_gblcus(df_bkg)
        # Populate Product allotment in output table
        create_alt_prd(df_bkg)

        conn.close()
    except Exception as e:
        print("Error in main: " + str(e))
    finally:
        pass
