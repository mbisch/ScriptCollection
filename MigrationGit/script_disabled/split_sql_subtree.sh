#!/bin/bash

echo start replace repo Sql
date

# Sql repo
cd /home/mbisch/repos

rm -rf  /home/mbisch/repos/windekis_sql
git clone git@localhost:windekis_sql

cd /home/mbisch/repos/windekis_sql
git subtree split -P "BPGE_Tresor"          -b BPGE_Tresor_sql
git subtree split -P "Berenberg"            -b Berenberg_sql
git subtree split -P "Deltec"               -b Deltec_sql
git subtree split -P "JCE Hottinger"        -b JCE_Hottinger_sql
git subtree split -P "TBA"                  -b TBA_sql
git subtree split -P "PKB"                  -b PKB_sql
git subtree split -P "Credit-Suisse"        -b Credit-Suisse_sql
git subtree split -P "Finter"               -b Finter_sql
git subtree split -P "BPNA_Tresor"          -b BPNA_Tresor_sql
git subtree split -P "LBBW"                 -b LBBW_sql
git subtree split -P "Piguet-Galland"       -b Piguet-Galland_sql
git subtree split -P "BPMO_Tresor"          -b BPMO_Tresor_sql
git subtree split -P "Hiv"                  -b Hiv_sql
git subtree split -P "InHouse"              -b InHouse_sql
git subtree split -P "Weg_Tresor_2013"      -b Weg_Tresor_2013_sql
git subtree split -P "PKB Fatca Workshop"   -b PKB_Fatca_Workshop_sql
git subtree split -P "Metropol"             -b Metropol_sql
git subtree split -P "BES"                  -b BES_sql
git subtree split -P "GUT DEMO"             -b GUT_DEMO_sql
git subtree split -P "Nomura"               -b Nomura_sql
git subtree split -P "Trafina"              -b Trafina_sql
git subtree split -P "BPGE"                 -b BPGE_sql
git subtree split -P "Gonet"                -b Gonet_sql
git subtree split -P "MRV"                  -b MRV_sql
git subtree split -P "Weg"                  -b Weg_sql
git subtree split -P "ClaridenLeuSingapore" -b ClaridenLeuSingapore_sql
git subtree split -P "BPNA"                 -b BPNA_sql
git subtree split -P "NHB"                  -b NHB_sql
git subtree split -P "Dexia"                -b Dexia_sql
git subtree split -P "Scobag"               -b Scobag_sql
git subtree split -P "Vbv"                  -b Vbv_sql
git subtree split -P "Arab_Bank"            -b Arab_Bank_sql
git subtree split -P "LGT_BOSS_CH"          -b LGT_BOSS_CH_sql
git subtree split -P "MediBank"             -b MediBank_sql
git subtree split -P "BBVA"                 -b BBVA_sql
git subtree split -P "Sfb_Wdk"              -b Sfb_Wdk_sql
git subtree split -P "Sfb_MultiLanguage"    -b Sfb_MultiLanguage_sql
git subtree split -P "Genix"                -b Genix_sql
git subtree split -P "BBB"                  -b BBB_sql
git subtree split -P "Gutzwiller"           -b Gutzwiller_sql
git subtree split -P "BIL"                  -b BIL_sql
git subtree split -P "AMBIT_CIM"            -b AMBIT_CIM_sql
git subtree split -P "RBL"                  -b RBL_sql
git subtree split -P "BPMO"                 -b BPMO_sql
git subtree split -P "Ansbacher_Nassau"     -b Ansbacher_Nassau_sql
git subtree split -P "Bwl"                  -b Bwl_sql
git subtree split -P "GUT"                  -b GUT_sql
git subtree split -P "BOV_PKB_Demo"         -b BOV_PKB_Demo_sql
git subtree split -P "Vbv_Tresor"           -b Vbv_Tresor_sql
git subtree split -P "Bvv"                  -b Bvv_sql
git subtree split -P "BAB"                  -b BAB_sql
git subtree split -P "LBLux_Phase_III"      -b LBLux_Phase_III_sql
git subtree split -P "BOV"                  -b BOV_sql
git subtree split -P "BHF98_2"              -b BHF98_2_sql
git subtree split -P "Gonet_GON_CIM"        -b Gonet_GON_CIM_sql
git subtree split -P "Bank von Roll"        -b Bank_von_Roll_sql
git subtree split -P "PB_Ihag"              -b PB_Ihag_sql
git subtree split -P "InCore"               -b InCore_sql

git push --all -u

cd /home/mbisch/repos/
rm -rf windekis_sql

cd /home/mbisch/repos/sql_repos
rm -rf /home/mbisch/repos/sql_repos/*

mkdir /home/mbisch/repos/sql_repos/BPGE_Tresor_sql
mkdir /home/mbisch/repos/sql_repos/Berenberg_sql
mkdir /home/mbisch/repos/sql_repos/Deltec_sql
mkdir /home/mbisch/repos/sql_repos/JCE_Hottinger_sql
mkdir /home/mbisch/repos/sql_repos/TBA_sql
mkdir /home/mbisch/repos/sql_repos/PKB_sql
mkdir /home/mbisch/repos/sql_repos/Credit-Suisse_sql
mkdir /home/mbisch/repos/sql_repos/Finter_sql
mkdir /home/mbisch/repos/sql_repos/BPNA_Tresor_sql
mkdir /home/mbisch/repos/sql_repos/LBBW_sql
mkdir /home/mbisch/repos/sql_repos/Piguet-Galland_sql
mkdir /home/mbisch/repos/sql_repos/BPMO_Tresor_sql
mkdir /home/mbisch/repos/sql_repos/Hiv_sql
mkdir /home/mbisch/repos/sql_repos/InHouse_sql
mkdir /home/mbisch/repos/sql_repos/Weg_Tresor_2013_sql
mkdir /home/mbisch/repos/sql_repos/PKB_Fatca_Workshop_sql
mkdir /home/mbisch/repos/sql_repos/Metropol_sql
mkdir /home/mbisch/repos/sql_repos/BES_sql
mkdir /home/mbisch/repos/sql_repos/GUT_DEMO_sql
mkdir /home/mbisch/repos/sql_repos/Nomura_sql
mkdir /home/mbisch/repos/sql_repos/Trafina_sql
mkdir /home/mbisch/repos/sql_repos/BPGE_sql
mkdir /home/mbisch/repos/sql_repos/Gonet_sql
mkdir /home/mbisch/repos/sql_repos/MRV_sql
mkdir /home/mbisch/repos/sql_repos/Weg_sql
mkdir /home/mbisch/repos/sql_repos/ClaridenLeuSingapore_sql
mkdir /home/mbisch/repos/sql_repos/BPNA_sql
mkdir /home/mbisch/repos/sql_repos/NHB_sql
mkdir /home/mbisch/repos/sql_repos/Dexia_sql
mkdir /home/mbisch/repos/sql_repos/Scobag_sql
mkdir /home/mbisch/repos/sql_repos/Vbv_sql
mkdir /home/mbisch/repos/sql_repos/Arab_Bank_sql
mkdir /home/mbisch/repos/sql_repos/LGT_BOSS_CH_sql
mkdir /home/mbisch/repos/sql_repos/MediBank_sql
mkdir /home/mbisch/repos/sql_repos/BBVA_sql
mkdir /home/mbisch/repos/sql_repos/Sfb_Wdk_sql
mkdir /home/mbisch/repos/sql_repos/Sfb_MultiLanguage_sql
mkdir /home/mbisch/repos/sql_repos/Genix_sql
mkdir /home/mbisch/repos/sql_repos/BBB_sql
mkdir /home/mbisch/repos/sql_repos/Gutzwiller_sql
mkdir /home/mbisch/repos/sql_repos/BIL_sql
mkdir /home/mbisch/repos/sql_repos/AMBIT_CIM_sql
mkdir /home/mbisch/repos/sql_repos/RBL_sql
mkdir /home/mbisch/repos/sql_repos/BPMO_sql
mkdir /home/mbisch/repos/sql_repos/Ansbacher_Nassau_sql
mkdir /home/mbisch/repos/sql_repos/Bwl_sql
mkdir /home/mbisch/repos/sql_repos/GUT_sql
mkdir /home/mbisch/repos/sql_repos/BOV_PKB_Demo_sql
mkdir /home/mbisch/repos/sql_repos/Vbv_Tresor_sql
mkdir /home/mbisch/repos/sql_repos/Bvv_sql
mkdir /home/mbisch/repos/sql_repos/BAB_sql
mkdir /home/mbisch/repos/sql_repos/LBLux_Phase_III_sql
mkdir /home/mbisch/repos/sql_repos/BOV_sql
mkdir /home/mbisch/repos/sql_repos/BHF98_2_sql
mkdir /home/mbisch/repos/sql_repos/Gonet_GON_CIM_sql
mkdir /home/mbisch/repos/sql_repos/Bank_von_Roll_sql
mkdir /home/mbisch/repos/sql_repos/PB_Ihag_sql
mkdir /home/mbisch/repos/sql_repos/InCore_sql

for i in $( ls /home/mbisch/repos/sql_repos/ ); do
   echo create repo: $i
   
   cd    /home/mbisch/repos/sql_repos/$i
   git init
   git pull git@localhost:windekis_sql $i
   
   cp  /home/mbisch/script/.gitignore  /home/mbisch/repos/sql_repos/$i/
   git add .gitignore
   git commit -a -m 'add .gitignore to repository'

   git remote add origin git@localhost:$i
   git push origin -u master   
done

rm -rf /home/mbisch/repos/sql_repos/*

#exit
echo done

