/**************************************************************************
 DbDesc.cpp / DbDesc.h
 **************************************************************************
 Projekt      : Apsys WinDekis Developement System
 Copyright    : FIS Ambit CIM
 Compiler     : Borland C++
 Beschreibung : Enthält Datenbankbeschreibungstabelle
 **************************************************************************

 Datum        Vers   Vis   Beschreibung
 -----        ----   ---   ------------

 09.08.2005   3.69   Mb    Nach DBDescCommon ausgelagert
 26.09.2005   3.70   Mb    GxMisList hinzugefügt
 28.09.2005   3.71   Ae    Schliessfach integriert
 14.10.2005   3.72   Mb    DbDescSQLStr hinzugefügt
 27.10.2005   3.73   Ae    Akte ausgelagert
 08.11.2005   3.74   Mb    GxAdminFieldList hinzugefügt
 18.04.2006   3.75   Ae    Kreditkarte eingebaut
 26.07.2006   3.76   Mb    __GXDID__ hinzugefügt
 21.12.2006   3.77   AH    Für Partnerdokumente Auswahl DB_DOKU_PARTNER hinzugefügt
 30.01.2009   3.78   Bs    Apsys Finance Daten eingefügt

 **************************************************************************/


/**************************************************************************
 Include-Dateien
 **************************************************************************/

 #include <main.h>
 #pragma hdrstop

 #ifdef __DBDESC_VALIDIERUNG_OFF__
    #undef __VALIDIERUNG__
 #endif

/*************************************************************************
 Konstanten
 *************************************************************************/

   #ifdef __PARTNERDOKUMENTE_X__
      #define DB_DOKU_TABLE DB_DOKU_PARTNER
      #define DB_DOKU_VIEW  DB_DOKU

      #define DB_KORDOK_TABLE 0
      #define DB_KORDOK_VIEW DB_KORDOK
   #else
      #define DB_DOKU_TABLE DB_DOKU_PARTNER|DB_DOKU
      #define DB_DOKU_VIEW  0

      #define DB_KORDOK_TABLE DB_KORDOK
      #define DB_KORDOK_VIEW 0
   #endif

   #if defined (__NOMURA_STYLE__)
      #define DB_GELDVONKONTOINHABER DB_KUNDE|DB_OW_KUNDE|DB_DOKU|DB_KORDOK
   #else
      #define DB_GELDVONKONTOINHABER 0
   #endif

   #ifdef __FILIALE__
      #define KUNDE_FILIALE_FK  FILIALE_FILIALE_CD
   #else
      #define KUNDE_FILIALE_FK  NONE
   #endif

   #ifndef __PROCESS_MANAGER__
   #warning ############################################## or maybe this?
   /*************************************************************************
    DbCon WinDekis
   *************************************************************************/
   const DBCON far DBCon[MAX_DBCON]=
      {

      /*************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
      {    Nr,              Interface,   Database,   szSchema,      szRole,   szRolePassword,   szIniTitle,   bExtendedLogon,   bCharConvert,   dynamischeDaten   },
      **************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/

      {    WINDEKIS,        IF_OCI,      DB_ORACLE,  TABLE_OWNER,   DBROLE,   DBROLE_PASSWORD,  _T("Oracle"),     TRUE,             FALSE,          0,                 _T(""),  _T(""), _T("")   },
      {    WINDEKIS_ENC1,   IF_OCI,      DB_ORACLE,  TABLE_OWNER,   DBROLE,   DBROLE_PASSWORD,  _T("Enc1"),       TRUE,             FALSE,          0,                 _T(""),  _T(""), _T("")   },
      {    WINDEKIS_ENC2,   IF_OCI,      DB_ORACLE,  TABLE_OWNER,   DBROLE,   DBROLE_PASSWORD,  _T("Enc2"),       TRUE,             FALSE,          0,                 _T(""),  _T(""), _T("")   },
      #ifdef __ENFORCED_2WAY_AUTHORIZATION__
      {    WINDEKIS_ENCUSER,IF_OCI,      DB_ORACLE,  ENC_OWNER,     DBENCROLE,DBROLE_PASSWORD,  _T("EncUser"),    TRUE,             FALSE,          0,                 _T(""),  _T(""), _T("")   },
      #endif
      };
   #else //  __PROCESS_MANAGER__
   /*************************************************************************
    DbCon Process Manager
   *************************************************************************/
   #warning ##############################################maybe this?
   const DBCON far DBCon[MAX_DBCON]=
      {
      //************************************************************************************************************************************************
      //Nr                                          Interface                  Database                                               szSchema                         szRole                      szRolePassword              szIniTitle                                      bExtendedLogon                                    bCharConvert                            dynamischeDaten
      //************************************************************************************************************************************************
      {    WINDEKIS,                                IF_OCI,                    DB_ORACLE,                                             TABLE_OWNER,                     DBROLE,                     DBROLE_PASSWORD,            _T("Oracle"),                                   TRUE,                                             FALSE,                                  0,                                 _T(""),                 _T(""),   _T("")   },
      {    APSYS,                                   IF_OCI,                    DB_ORACLE,                                             NULL,                            NULL,                       NULL,                       _T("Apsys"),                                    TRUE,                                             FALSE,                                  0,                                 _T(""),                 _T(""),   _T("")   },
      #ifdef WAI_OWNER
      {    WAI,                                     IF_OCI,                    DB_OTHERS,                                             WAI_OWNER,                       NULL,                       NULL,                       _T("Datawarehouse"),                            TRUE,                                             FALSE,                                  0,                                 _T(""),                 _T(""),   _T("")   },
      #else
      {    WAI,                                     IF_OCI,                    DB_OTHERS,                                             NULL,                            NULL,                       NULL,                       _T("Datawarehouse"),                            TRUE,                                             FALSE,                                  0,                                 _T(""),                 _T(""),   _T("")   },
      #endif
      {    DWH,                                     IF_OCI,                    DB_OTHERS,                                             NULL,                            NULL,                       NULL,                       _T("DWH"),                                      TRUE,                                             FALSE,                                  0,                                 _T(""),                 _T(""),   _T("")   },
      {    ACCESS_DB,                               IF_ODBC,                   DB_OTHERS,                                             NULL,                            NULL,                       NULL,                       _T("MS-Access"),                                TRUE,                                             FALSE,                                  0,                                 _T(""),                 _T(""),   _T("")   }
      };
   #endif //  __PROCESS_MANAGER__

// DBDesc
// ******

const DBDESC far DBDesc[MAX_DBDESC]=
   {

 // Allgemeine Tabellen
 // *******************

    #include <..\..\windekis\source\DbDescCommon.cpp>

 // Administrative Tabellen
 // ***********************

    #include <..\..\windekis\source\DbDescAdmin.cpp>

 // Datenaustausch
 // **************

    #include <..\..\windekis\source\DbDescDataExchange.cpp>

 // Akte
 // ****

    #include <..\..\windekis\source\DbDescAkte.cpp>

 // Temp Tables
 // ***********

    #include <..\..\windekis\source\DbDescTempTables.cpp>

 // World-Check
 // ***********

    #if defined  __WORLDCHECK__ || defined __WORLDCHECK_DBDESC__ || defined __WORLDCHECK_AUTOLOAD__
       #include <..\..\windekis\source\DbDescWorldCheck.cpp>
    #endif

 // Externe Quellen
 // ***************

    #ifdef __EXTERNE_QUELLEN__
       #include <..\..\windekis\source\DbDescExterneQuellen.cpp>
    #endif

 // Cubis
 // *****

    #ifdef __CUBIS__
       #include <..\..\windekis\source\DbDescCubis.cpp>
    #endif

 // Name Split
 // **********

    #ifdef __NAME_SPLIT__
       #include <..\..\windekis\source\DbDescNameSplit.cpp>
    #endif

 // EUTaxReporting
 // **************

    #ifdef __EUTAXREPORTING__
       #include <..\..\windekis\source\DbDescEUTaxReporting.cpp>
    #endif

 // Reporting Prudentiel
 // ********************

    #ifdef __REPORTING_PRUDENTIEL__
       #include <..\..\windekis\source\DbDescReportingPrudentiel.cpp>
    #endif

 // GxDbDesc
 // ********

    #include <..\source\GxDbDesc.cpp>

 // Schliessfach
 // ************

    #ifdef __SCHLIESSFACH__
       #include <..\..\windekis\source\DbDescSchliessfach.cpp>
    #endif

 // Kreditkarte
 // ***********

    #ifdef __KREDITKARTE__
       #include <..\..\windekis\source\DbDescKreditkarte.cpp>
    #endif

 // Fatca
 // *****

    #ifdef __FATCA_HITS__
       #include <..\..\windekis\source\DbDescFatca.cpp>
    #endif

 // AEoI
 // ****

    #ifdef __AEOI_HITS__
       #include <..\..\windekis\source\DbDescAEOI.cpp>
    #endif

 // Apsys Interface Tabellen
 // ************************

    #ifdef __WMA_APSYS_INTERFACE_TABLES__
       #include <..\..\windekis\source\DbDescApsysInterface.cpp>
    #endif

 // Apsys Tabellen
 // **************

    #ifdef __PROCESS_MANAGER__
       #include <..\..\windekis\source\DbDescApsys.cpp>
    #endif

 // E-Services
 // **********

    #ifdef __E_SERVICES__
       #include <..\..\windekis\source\DbDescEServices.cpp>
    #endif

 // E-Banking
 // *********

    #ifdef __E_BANKING_USER_MANAGEMENT__
       #include <..\..\windekis\source\DbDescEBanking.cpp>
    #endif

 // Marketing Tabellen
 // ******************

    #ifdef __MARKETING__
       #include <..\..\MxWare32\Rms\source\DbDescMarketing.cpp>
    #endif

 // DBDescJava Parameter
 // ********************

    #ifdef __JAVA__
       #include <..\..\windekis\source\DbDescJava.cpp>
    #endif

    #ifdef __JAVA_JOBS__
       #include <..\..\windekis\source\DbDescJob.cpp>
    #endif

 // History Tabellen
 // ****************

    #ifdef __HISTORY__
       #include <..\..\windekis\source\DbDescHistory.cpp>
    #endif

 // Administrative History Tabellen
 // *******************************

    #ifdef __ADMIN_TAB_HISTORY__
       #include <..\..\windekis\source\DbDescAdminHistory.cpp>
    #endif

 // ArchivInstanz
 // *************

    #if defined (__ARCHIVINSTANZ__) || defined (__WEBARCHIV__) || defined (__SICFILES__) || defined (__EMAILVERSAND__) || defined (__DBARCHIV__) || defined (__SWIFTFILES__)
       #include <..\..\windekis\source\DbDescArchivInstanz.cpp>
    #endif

 // Migrationstabellen
 // ******************

    #ifdef __MIG_TABELLEN__
    #include <..\..\windekis\source\DbMigTabellen.cpp>
    #endif

    #ifdef __MIG_ADRESSPLUS_LBBW__
    #include <..\..\windekis\source\DbDescMigAdressPlus.cpp>
    #endif

    #ifdef __MIG_AVALOQ_LBBW__
    #include <..\..\windekis\source\DbDescMigAvaloq.cpp>
    #endif

    #ifdef __MIG_ARCHIV__
    #include <..\..\windekis\source\DbDescMigArchiv.cpp>
    #endif

    #if defined (__MIG_APSYS__) && !defined(__PROCESS_MANAGER__)
    #include <..\..\windekis\source\DbDescMigApsys.cpp>
    #endif

 // VV Monitor Tabellen
 // *******************

    #ifdef __VV_MONITOR__
    #include <..\..\windekis\source\DbDescVvMonitor.cpp>
    #endif

 // Apsys Finance Data
 // ******************

    #ifdef __APSYS_FINANCE_DATA__
    #include <..\..\windekis\source\DbDescApsysFinanceData.cpp>
    #endif

// Partner Dubletten
// *****************

    #ifdef __PARTNER_DUBLETTEN__
    #include <..\..\windekis\source\DbDescPartnerDubletten.cpp>
    #endif

 // FinFox Import
 // *************

    #ifdef __FINFOX_IMPORT__
    #include <..\..\windekis\source\DbDescFinFoxImport.cpp>
    #endif

 // Erträgnisaufstellung
 // ********************

    #ifdef __ERTRAEGNISAUFSTELLUNG__
    #include <..\..\windekis\source\DbDescErtraegnis.cpp>
    #endif

 // Voice over IP
 // *************

    #ifdef __ASC_EVOIP__
       #include <..\..\windekis\source\DbDescVoIp.cpp>
    #endif

 // Projektspezifische DBDesc
 // *************************

    #ifdef __PROZESSMGR_DB_DESC_PROJECT_LINK__
    #include <..\..\windekis\windekis\source\DbDescProject.cpp>
    #else
    #include <..\..\windekis\source\DbDescProject.cpp>
    #endif
    };

 // QFlagInclude
 // ************

    #include <..\..\windekis\source\DbDescQFlagInclude.cpp>

 // GxDBDescSQLStr Funktionen
 // *************************

    #include <..\source\GxDbDescSQLStr.cpp>

 // DBDescSQLStr Funktionen
 // ***********************

    #include <..\..\windekis\source\DbDescSQLStr.cpp>

    #ifdef __DBDESC_VALIDIERUNG_OFF__
       #define __VALIDIERUNG__
    #endif


