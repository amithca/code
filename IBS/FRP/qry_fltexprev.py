import datetime
from dateutil.relativedelta import relativedelta


class QryClass:
    v_fltcaridr = str(1180)  # Flight Carrier ID

    def __init__(self, dat):
        if not dat:
            dat = datetime.datetime.now()
        self.currentDate = dat
        self.delta_4W = relativedelta(days=-28)
        self.delta_1Y = relativedelta(years=-1)
        self.cur_date = self.currentDate.strftime('%Y-%m-%d')
        self.his_dat_4W = self.currentDate + self.delta_4W
        self.his_dat_4W = self.his_dat_4W.strftime('%Y-%m-%d')
        self.his_dat_1Y = self.currentDate + self.delta_1Y
        self.his_dat_1Y = self.his_dat_1Y.strftime('%Y-%m-%d')
        self.createQryDict()  # Create queries based on dat

    def createQryDict(self):
        # print("set_exec_date.cur_dat:" + self.cur_date)
        # print("set_exec_date.his_dat_4W:" + self.his_dat_4W)
        self.query_FRP = {
            "qry_segrto_seglst": "SELECT DISTINCT CMPCOD,to_date('" + self.cur_date + "','YYYY-MM-DD') EXEDAT,FLTNUM, SEGORG,SEGDST" +
                                 ",0 SUMCHGWGTSEG,0 SUMCHGWGTFLT,0 RTO,NULL DATPER,CURRENT_TIMESTAMP CRMLSTUPDTIM,MAX(fltrou) FLTROU " +
                                 "FROM (SELECT CMPCOD,fltcarcod||fltnum fltnum,fltdat,SEGORG,SEGDST,(SELECT fltrou FROM crmfltoprmst WHERE fltnum=a.fltcarcod" +
                                 "||a.fltnum AND fltdat=a.fltdat AND cmpcod=a.cmpcod ) fltrou FROM crmfltcapclsrul a WHERE fltcaridr=" + self.v_fltcaridr + " AND a.SEGORG<>a.SEGDST AND fltdat BETWEEN to_date('" + self.his_dat_4W + "','YYYY-MM-DD') and to_date('" + self.cur_date + "','YYYY-MM-DD') UNION ALL SELECT CMPCOD,fltnum,fltdat,SEGORG,SEGDST,(SELECT fltrou FROM crmfltoprmst WHERE fltnum=b.fltnum AND fltdat  =b.fltdat AND cmpcod=b.cmpcod) fltrou FROM crmfltcapsegdcprul_prdcls b WHERE rultyp='BID' AND b.segorg<>b.segdst AND fltdat BETWEEN to_date('" + self.his_dat_4W + "','YYYY-MM-DD') AND to_date('" + self.cur_date + "','YYYY-MM-DD') UNION ALL  SELECT CMPCOD,fltnum,fltdat,ORGCOD SEGORG,ORGCOD SEGDST,(SELECT fltrou  FROM crmfltoprmst WHERE fltnum=c.fltnum AND fltdat=c.fltdat AND cmpcod=c.cmpcod) fltrou FROM crmcapfltalt c WHERE altsta<>'D' AND c.ORGCOD<>c.DSTCOD AND fltdat BETWEEN to_date('" + self.his_dat_4W + "','YYYY-MM-DD') AND to_date('" + self.cur_date + "','YYYY-MM-DD')) A where segorg<>segdst GROUP BY cmpcod,FLTNUM,SEGORG,SEGDST",
            "qry_bkg_1Y": "select bkgdcp.cmpcod,bkgdcp.fltnum,bkgdcp.fltdat,bkgdcp.segorg,bkgdcp.segdst,awborg,awbdst," + "chgwgt,scccod,prdnam,altidr,bkgdcp.flttyp,grsrevusdshp,grsrevusd,acrtypcod,fltawbwgt," + "fltratusd,fltopr.fltrou fltrou FROM crmcapbkgfltdcp bkgdcp,crmfltoprmst fltopr WHERE bkgdcp.fltdat BETWEEN to_date('" + self.his_dat_1Y + "','YYYY-MM-DD') AND to_date('" + self.cur_date + "','YYYY-MM-DD') AND bkgdcp.dcp=-1 AND bkgdcp.flttyp <> 'T' AND bkgdcp.bkgsta <> 'X' AND bkgdcp.cmpcod=fltopr.cmpcod AND bkgdcp.fltnum  =fltopr.fltnum AND bkgdcp.fltdat  =fltopr.fltdat"
        }
