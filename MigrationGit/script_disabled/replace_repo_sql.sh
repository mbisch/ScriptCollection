#!/bin/bash

echo start replace repo Sql
date


rm -rf /home/git/repositories/AMBIT_CIM_sql.git
rm -rf /home/git/repositories/Ansbacher_Nassau_sql.git
rm -rf /home/git/repositories/Arab_Bank_sql.git
rm -rf /home/git/repositories/BAB_sql.git
rm -rf /home/git/repositories/Bank_von_Roll_sql.git
rm -rf /home/git/repositories/BBB_sql.git
rm -rf /home/git/repositories/BBVA_sql.git
rm -rf /home/git/repositories/Berenberg_sql.git
rm -rf /home/git/repositories/BES_sql.git
rm -rf /home/git/repositories/BHF98_2_sql.git
rm -rf /home/git/repositories/BIL_sql.git
rm -rf /home/git/repositories/BOV_PKB_Demo_sql.git
rm -rf /home/git/repositories/BOV_sql.git
rm -rf /home/git/repositories/BPGE_sql.git
rm -rf /home/git/repositories/BPGE_Tresor_sql.git
rm -rf /home/git/repositories/BPMO_sql.git
rm -rf /home/git/repositories/BPMO_Tresor_sql.git
rm -rf /home/git/repositories/BPNA_sql.git
rm -rf /home/git/repositories/BPNA_Tresor_sql.git
rm -rf /home/git/repositories/Bvv_sql.git
rm -rf /home/git/repositories/Bwl_sql.git
rm -rf /home/git/repositories/ClaridenLeuSingapore_sql.git
rm -rf /home/git/repositories/Credit-Suisse_sql.git
rm -rf /home/git/repositories/Deltec_sql.git
rm -rf /home/git/repositories/Dexia_sql.git
rm -rf /home/git/repositories/Finter_sql.git
rm -rf /home/git/repositories/Genix_sql.git
rm -rf /home/git/repositories/Gonet_GON_CIM_sql.git
rm -rf /home/git/repositories/Gonet_sql.git
rm -rf /home/git/repositories/GUT_DEMO_sql.git
rm -rf /home/git/repositories/GUT_sql.git
rm -rf /home/git/repositories/Gutzwiller_sql.git
rm -rf /home/git/repositories/Hiv_sql.git
rm -rf /home/git/repositories/InCore_sql.git
rm -rf /home/git/repositories/InHouse_sql.git
rm -rf /home/git/repositories/JCE_Hottinger_sql.git
rm -rf /home/git/repositories/LBBW_sql.git
rm -rf /home/git/repositories/LBLux_Phase_III_sql.git
rm -rf /home/git/repositories/LGT_BOSS_CH_sql.git
rm -rf /home/git/repositories/MediBank_sql.git
rm -rf /home/git/repositories/Metropol_sql.git
rm -rf /home/git/repositories/MRV_sql.git
rm -rf /home/git/repositories/NHB_sql.git
rm -rf /home/git/repositories/Nomura_sql.git
rm -rf /home/git/repositories/PB_Ihag_sql.git
rm -rf /home/git/repositories/Piguet-Galland_sql.git
rm -rf /home/git/repositories/PKB_Fatca_Workshop_sql.git
rm -rf /home/git/repositories/PKB_sql.git
rm -rf /home/git/repositories/RBL_sql.git
rm -rf /home/git/repositories/Scobag_sql.git
rm -rf /home/git/repositories/Sfb_MultiLanguage_sql.git
rm -rf /home/git/repositories/Sfb_Wdk_sql.git
rm -rf /home/git/repositories/TBA_sql.git
rm -rf /home/git/repositories/Trafina_sql.git
rm -rf /home/git/repositories/Vbv_sql.git
rm -rf /home/git/repositories/Vbv_Tresor_sql.git
rm -rf /home/git/repositories/Weg_sql.git
rm -rf /home/git/repositories/Weg_Tresor_2013_sql.git 


# Sql repo
cd /home/git/repositories/windekis_sql.git 
rm -rf /home/git/repositories/windekis_sql.git/*
git init --bare  
cat /home/mbisch/mig_cvs2git/Sql/blob/git-blob.dat /home/mbisch/mig_cvs2git/Sql/tmp/git-dump.dat | git fast-import

#exit
echo done


