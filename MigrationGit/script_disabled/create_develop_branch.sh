#!/bin/bash

cd /home/mbisch/repos/all_repos
rm -rf /home/mbisch/repos/all_repos/*

mkdir /home/mbisch/repos/all_repos/windekis
mkdir /home/mbisch/repos/all_repos/jdekis
mkdir /home/mbisch/repos/all_repos/windekis_add
mkdir /home/mbisch/repos/all_repos/BPGE_Tresor_sql
mkdir /home/mbisch/repos/all_repos/Berenberg_sql
mkdir /home/mbisch/repos/all_repos/Deltec_sql
mkdir /home/mbisch/repos/all_repos/JCE_Hottinger_sql
mkdir /home/mbisch/repos/all_repos/TBA_sql
mkdir /home/mbisch/repos/all_repos/PKB_sql
mkdir /home/mbisch/repos/all_repos/Credit-Suisse_sql
mkdir /home/mbisch/repos/all_repos/Finter_sql
mkdir /home/mbisch/repos/all_repos/BPNA_Tresor_sql
mkdir /home/mbisch/repos/all_repos/LBBW_sql
mkdir /home/mbisch/repos/all_repos/Piguet-Galland_sql
mkdir /home/mbisch/repos/all_repos/BPMO_Tresor_sql
mkdir /home/mbisch/repos/all_repos/Hiv_sql
mkdir /home/mbisch/repos/all_repos/InHouse_sql
mkdir /home/mbisch/repos/all_repos/Weg_Tresor_2013_sql
mkdir /home/mbisch/repos/all_repos/PKB_Fatca_Workshop_sql
mkdir /home/mbisch/repos/all_repos/Metropol_sql
mkdir /home/mbisch/repos/all_repos/BES_sql
mkdir /home/mbisch/repos/all_repos/GUT_DEMO_sql
mkdir /home/mbisch/repos/all_repos/Nomura_sql
mkdir /home/mbisch/repos/all_repos/Trafina_sql
mkdir /home/mbisch/repos/all_repos/BPGE_sql
mkdir /home/mbisch/repos/all_repos/Gonet_sql
mkdir /home/mbisch/repos/all_repos/MRV_sql
mkdir /home/mbisch/repos/all_repos/Weg_sql
mkdir /home/mbisch/repos/all_repos/ClaridenLeuSingapore_sql
mkdir /home/mbisch/repos/all_repos/BPNA_sql
mkdir /home/mbisch/repos/all_repos/NHB_sql
mkdir /home/mbisch/repos/all_repos/Dexia_sql
mkdir /home/mbisch/repos/all_repos/Scobag_sql
mkdir /home/mbisch/repos/all_repos/Vbv_sql
mkdir /home/mbisch/repos/all_repos/Arab_Bank_sql
mkdir /home/mbisch/repos/all_repos/LGT_BOSS_CH_sql
mkdir /home/mbisch/repos/all_repos/MediBank_sql
mkdir /home/mbisch/repos/all_repos/BBVA_sql
mkdir /home/mbisch/repos/all_repos/Sfb_Wdk_sql
mkdir /home/mbisch/repos/all_repos/Sfb_MultiLanguage_sql
mkdir /home/mbisch/repos/all_repos/Genix_sql
mkdir /home/mbisch/repos/all_repos/BBB_sql
mkdir /home/mbisch/repos/all_repos/Gutzwiller_sql
mkdir /home/mbisch/repos/all_repos/BIL_sql
mkdir /home/mbisch/repos/all_repos/AMBIT_CIM_sql
mkdir /home/mbisch/repos/all_repos/RBL_sql
mkdir /home/mbisch/repos/all_repos/BPMO_sql
mkdir /home/mbisch/repos/all_repos/Ansbacher_Nassau_sql
mkdir /home/mbisch/repos/all_repos/Bwl_sql
mkdir /home/mbisch/repos/all_repos/GUT_sql
mkdir /home/mbisch/repos/all_repos/BOV_PKB_Demo_sql
mkdir /home/mbisch/repos/all_repos/Vbv_Tresor_sql
mkdir /home/mbisch/repos/all_repos/Bvv_sql
mkdir /home/mbisch/repos/all_repos/BAB_sql
mkdir /home/mbisch/repos/all_repos/LBLux_Phase_III_sql
mkdir /home/mbisch/repos/all_repos/BOV_sql
mkdir /home/mbisch/repos/all_repos/BHF98_2_sql
mkdir /home/mbisch/repos/all_repos/Gonet_GON_CIM_sql
mkdir /home/mbisch/repos/all_repos/Bank_von_Roll_sql
mkdir /home/mbisch/repos/all_repos/PB_Ihag_sql
mkdir /home/mbisch/repos/all_repos/InCore_sql

for i in $( ls /home/mbisch/repos/all_repos/ ); do
   echo create develop branch for: $i
   cd  /home/mbisch/repos/all_repos/$i
   git clone git@localhost:$i /home/mbisch/repos/all_repos/$i/.

   git tag -a CVS2GIT-CutOver -m 'CVS to GIT cutover'
   git push origin CVS2GIT-CutOver


   git push -f origin HEAD:refs/heads/develop
done

rm -rf /home/mbisch/repos/all_repos/*



