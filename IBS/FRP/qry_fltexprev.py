import datetime
from dateutil.relativedelta import relativedelta


class QryClass:
    def __init__(self, dat, cmpcod, fltcaridr):
        self.v_cmpcod = '' if not cmpcod else cmpcod  # Company code
        self.v_fltcaridr = '' if not fltcaridr else str(fltcaridr)  # Flight Carrier ID

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
            "qry_segrto_hisvernum": "SELECT COALESCE(MAX(vernum),0)+1 vernum FROM CRMFLTEXPREVFCTSEGRTOHIS",
            "qry_bkg_1Y": "select bkgdcp.cmpcod,bkgdcp.fltnum,bkgdcp.fltdat,bkgdcp.segorg,bkgdcp.segdst,awborg,awbdst," + "chgwgt,scccod,prdnam,altidr,bkgdcp.flttyp,grsrevusdshp,grsrevusd,acrtypcod,fltawbwgt," + "fltratusd,fltopr.fltrou fltrou FROM crmcapbkgfltdcp bkgdcp,crmfltoprmst fltopr WHERE bkgdcp.fltdat BETWEEN to_date('" + self.his_dat_1Y + "','YYYY-MM-DD') AND to_date('" + self.cur_date + "','YYYY-MM-DD') AND bkgdcp.dcp=-1 AND bkgdcp.flttyp <> 'T' AND bkgdcp.bkgsta <> 'X' AND bkgdcp.cmpcod=fltopr.cmpcod AND bkgdcp.fltnum  =fltopr.fltnum AND bkgdcp.fltdat  =fltopr.fltdat",
            "qry_awm": "SELECT parval awm FROM shrsyspar WHERE parcod = 'cra.proration.awmfactorvalue' AND cmpcod='" + self.v_cmpcod + "'",
            "qry_density_factor": "SELECT cast(parval as double precision) as densityfactor FROM shrsyspar WHERE parcod = 'capacity.allotment.weightFor1CBMVolume' AND cmpcod='" + self.v_cmpcod + "'",
            "qry_dow_start": " select case when A.parval='SUN' then 1 when A.parval='MON' then 2 when A.parval='TUE' then 3 when A.parval='WED' then 4 when A.parval='THU' then 5 when A.parval='FRI' then 6 when A.parval='SAT' then 7 else 1 end dowstr from (SELECT parval FROM shrsyspar WHERE parcod LIKE 'system.defaults.startday' and cmpcod='" + self.v_cmpcod + "') A"
        }

    def getPFMQry(self, orgarpcod, dstarpcod):
        qrypfm = "SELECT profct FROM CRAPROFCT pfm WHERE orgdstlvl='C' AND cmpcod='" + self.v_cmpcod + "' AND seqnum=(SELECT MAX(seqnum) FROM CRAPROFCT WHERE ORGCOD=pfm.orgcod AND DSTCOD=pfm.dstcod AND ORGDSTLVL=pfm.orgdstlvl AND CMPCOD=pfm.cmpcod) AND pfm.orgcod=COALESCE((SELECT ctycod FROM shrarpmst WHERE arpcod='" + orgarpcod + "' and cmpcod='" + self.v_cmpcod + "'),'" + orgarpcod + "') AND pfm.dstcod=COALESCE((SELECT ctycod  FROM shrarpmst WHERE arpcod='" + dstarpcod + "' and cmpcod='" + self.v_cmpcod + "'),'" + dstarpcod + "')"
        return qrypfm

    def getCgocapQry(self, fltnum, fltdat, density_factor):
        qrycgocap = ""
        if fltnum and fltdat and density_factor:
            qrycgocap = "select least(totcarcap,(totcarcapvol*" + density_factor + ")) cgocapwgt  FROM shracrtypmst where cmpcod='" + self.v_cmpcod + "' AND acrtypcod=(select min(acrtyp) from crmfltoprleg where cmpcod=" + self.v_cmpcod + " AND fltnum='" + fltnum + "' AND fltdat=to_date('" + fltdat
            "+','YYYY-MM-DD')) AND acrver=1"
        return qrycgocap

    def get_insQry_AltGblcus(self, frmdat, toodat):
        frmdat = frmdat.strftime('%Y-%m-%d')
        toodat = toodat.strftime('%Y-%m-%d')

        qry_ins_gblcus = "SELECT CMPCOD, FLTNUM, FLTDAT, orgcod SEGORG, dstcod SEGDST, COALESCE(traorg,'-') AWBORG, COALESCE(tradst,'-') AWBDST, traorgcty AWBORGCTY, tradstcty AWBDSTCTY, traorgcnt AWBORGCNT, tradstcnt AWBDSTCNT, traorgreg AWBORGREG, tradstreg AWBDSTREG, ALTIDR, '-' PRDNAM, GBLCUSCOD, CATCOD, STNCOD, NULL DOW, NULL CHGWGTFRM, NULL CHGWGTTOO, 'ALTGBLCUS' RECTYP, 0 RATUSD, 0 OTHCHG, -1 FLTDMD, -1 SEGPROFCT, -1 PRDPROFCT, -1 SEGALTWGT, -1 SEGPRDCLSWGT, -1 CLSWGTPER, CASE WHEN altwgt>0 THEN altwgt ELSE 0 END CLSWGT, 0 REVUSD, 1 CONTRBRTO, (SELECT CASE WHEN flttyp='CO' THEN 'P' WHEN flttyp ='C' THEN 'F' ELSE flttyp END flttyp FROM crmfltoprmst WHERE cmpcod=alt.cmpcod AND fltnum =alt.fltnum AND fltdat =alt.fltdat ) FLTTYP, (SELECT fltrou FROM crmfltoprmst WHERE cmpcod=alt.cmpcod AND fltnum =alt.fltnum AND fltdat =alt.fltdat ) FLTROU, (SELECT fltorg FROM crmfltoprmst WHERE cmpcod=alt.cmpcod AND fltnum =alt.fltnum AND fltdat =alt.fltdat ) FLTORG, (SELECT fltdst FROM crmfltoprmst WHERE cmpcod=alt.cmpcod AND fltnum =alt.fltnum AND fltdat =alt.fltdat )FLTDST, NULL EXEDAT, 0 TAGIDX, 'I' CRMFLG, CURRENT_TIMESTAMP CRMLSTUPDTIM, clsgrswgt, clsvolwgt FROM (SELECT cmpcod, fltnum, fltdat, orgcod, dstcod, traorg, tradst, fltaltidr altidr, gblcuscod, catcod, stncod, alttyp, COALESCE( CASE WHEN wgt < vol*COALESCE( (SELECT cast(parval AS DOUBLE precision) FROM shrsyspar syspar WHERE syspar.parcod = 'capacity.allotment.weightFor1CBMVolume' AND syspar.cmpcod =fltalt.cmpcod ),0) THEN vol *COALESCE( (SELECT cast(parval AS DOUBLE precision) FROM shrsyspar syspar WHERE syspar.parcod = 'capacity.allotment.weightFor1CBMVolume' AND syspar.cmpcod =fltalt.cmpcod ),0) ELSE wgt END ,0) altwgt, COALESCE( (SELECT ctycod FROM shrarpmst WHERE arpcod=fltalt.traorg ),fltalt.traorg) TRAORGCTY, COALESCE( (SELECT ctycod FROM shrarpmst WHERE arpcod=fltalt.tradst ),fltalt.tradst) TRADSTCTY, (SELECT cntcod FROM shrctymst WHERE ctycod= COALESCE( (SELECT ctycod FROM shrarpmst WHERE arpcod=fltalt.traorg ),fltalt.traorg) ) TRAORGCNT, (SELECT cntcod FROM shrctymst WHERE ctycod= COALESCE( (SELECT ctycod FROM shrarpmst WHERE arpcod=fltalt.tradst ),fltalt.tradst) ) TRADSTCNT, (SELECT regcod FROM shrcntmst WHERE cntcod= (SELECT cntcod FROM shrctymst WHERE ctycod= COALESCE( (SELECT ctycod FROM shrarpmst WHERE arpcod=fltalt.traorg ),fltalt.tradst) ) ) TRAORGREG, (SELECT regcod FROM shrcntmst WHERE cntcod= (SELECT cntcod FROM shrctymst WHERE ctycod= COALESCE( (SELECT ctycod FROM shrarpmst WHERE arpcod=fltalt.tradst ),fltalt.tradst) ) ) TRADSTREG, COALESCE( wgt,0) clsgrswgt , COALESCE(vol* (SELECT cast(parval AS DOUBLE precision) FROM shrsyspar syspar WHERE syspar.parcod = 'capacity.allotment.weightFor1CBMVolume' AND syspar.cmpcod =fltalt.cmpcod ),0) clsvolwgt FROM crmcapfltalt fltalt WHERE alttyp='G' AND altsta <>'D' AND fltdat BETWEEN to_date('" + frmdat + "','YYYY-MM-DD') AND to_date('" + toodat + "','YYYY-MM-DD') AND fltcaridr=" + self.v_fltcaridr + " AND cmpcod ='" + self.v_cmpcod + "' AND fltseqnum= (SELECT MAX(fltseqnum) FROM crmcapfltalt WHERE CMPCOD =fltalt.CMPCOD AND FLTCARIDR=fltalt.FLTCARIDR AND FLTNUM =fltalt.FLTNUM AND FLTDAT =fltalt.FLTDAT AND FLTALTIDR=fltalt.FLTALTIDR AND STNCOD =fltalt.STNCOD ) AND NOT EXISTS (SELECT 1 FROM crmfltoprmst WHERE domfltflg='Y' AND cmpcod =fltalt.cmpcod AND fltnum =fltalt.fltnum AND fltdat =fltalt.fltdat ) ) alt"
        return qry_ins_gblcus
