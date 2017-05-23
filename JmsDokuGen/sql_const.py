sql_stmt = """with CONF_TAB
              as (SELECT mtc.tab_name,
                    mfc.cd,
                    mfc.fld_name,
                    mtc.msg_name,
                    mfc.msg_fld_name,
                    mf.description,
                    mf.type_cd,
                    mft.description type,
                    mf.length,
                    mf.tot_digits,
                    mf.decimal_digits,
                    mf.is_key,
                    nvl(rf.msg_name,mf.ref_tab_name) ref_msg_name,
                    nvl(rf.msg_fld_name,mf.ref_fld_name) ref_msg_fld_name,
                    mf.ref_tab_type,
                    mf.remark
              from msg_out_fld mf
                 ,msg_out_tab_config mtc
                 ,msg_out_fld_config mfc
                 ,msg_out_fld_type mft
                 ,(select *
                  from   msg_out_tab_config rmtc
                        ,msg_out_fld_config rmfc
                  where  rmfc.tab_config_cd = rmtc.cd
                     and nvl (rmtc.loesch_cd, 'N') != 'J'
                     and nvl (rmfc.loesch_cd, 'N') != 'J'
                     and rmtc.dest_cd = :1) rf
              where     mf.tab_name = mtc.tab_name
                    and mfc.fld_name = mf.fld_name
                    and mfc.tab_config_cd = mtc.cd
                    and mtc.dest_cd = :2
                    and mf.type_cd = mft.cd
                    and mf.ref_tab_name = rf.tab_name(+)
                    and mf.ref_fld_name = rf.fld_name(+)
                    and nvl (mf.loesch_cd, 'N') != 'J'
                    and nvl (mtc.loesch_cd, 'N') != 'J'
                    and nvl (mfc.loesch_cd, 'N') != 'J'
                    and (   nvl (mfc.send_cd, 'J') = 'J'
                         or mf.info_source_cd = 'DBDESC')
                    )
           select ct1.cd,
                    ct1.tab_name,
                    ct1.fld_name,
                    ct1.msg_name,
                    ct1.msg_fld_name,
                    ct1.description,
                    ct2.tab_name hist_tab_name,
                    ct2.fld_name hist_fld_name,
                    ct2.msg_name hist_msg_name,
                    ct2.msg_fld_name hist_msg_fld_name,
                    ct2.description hist_description,
                    ct1.type_cd,
                    ct1.type,
                    ct1.length,
                    ct1.tot_digits,
                    ct1.decimal_digits,
                    ct1.is_key,
                    ct1.ref_msg_name,
                    ct1.ref_msg_fld_name,
                    ct1.ref_tab_type,
                    ct1.remark
           from conf_tab ct1
           full outer join conf_tab ct2
           on ct1.tab_name || '_HIST'= ct2.tab_name and ct1.fld_name  = ct2.fld_name
           where  ct1.tab_name  not like '%_HIST'
           order by ct1.msg_name, case when is_key = 'J' then '_' else msg_fld_name end"""

