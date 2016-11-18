/**************************************************************************
 DbDescProzessMgrStandalone.cpp / DbDescProzessMgrStandalone.h
**************************************************************************
   Projekt      : ApWare32 - ProzessMgr
   Copyright    : GenixInformatik
   Compiler     : BorlandC++
   Beschreibung : Old standalone DBDESC for ProzessManager
                  which should be replaced by common DBDESC for WinDekis
                  and ProzessManager
**************************************************************************

/********************************************************************************
 IMPORTTANT: New entries must also be added to the corresponding WinDekis DBDESC!
 ********************************************************************************/

   /*************************************************************************
   Konstanten
   *************************************************************************/

   #ifdef __KD_BEMERKUNG_MULTILINE__
      #define KD_BEMERKUNG_LEN                  501
   #else
      #ifdef __LBLUX_WDK__
         #define KD_BEMERKUNG_LEN                61
      #else
         #define KD_BEMERKUNG_LEN                51
      #endif
   #endif

   //DBCon
   //*****

   const DBCON far DBCon[MAX_DBCON]=
   {

/******************************************************************************************************************************************************************************************************************************
   {Nr                                          ,Interface                  ,Database                                               ,szSchema                         ,szRole                      ,szRolePassword              ,szIniTitle                                      ,bExtendedLogon                                    ,bCharConvert                            ,dynamischeDaten}
  ****************************************************************************************************************************************************************************************************************************/

   {   WINDEKIS     ,IF_OCI    ,DB_ORACLE   ,TABLE_OWNER     ,DBROLE            ,DBROLE_PASSWORD   ,"Oracle"          ,TRUE              ,FALSE        ,0              ,""           ,""        ,""                         },
   #ifdef __APSYS_ORACLE__
   {   APSYS        ,IF_OCI    ,DB_INGRES   ,NULL            ,NULL              ,NULL              ,"Apsys"           ,TRUE              ,FALSE        ,0              ,""           ,""        ,""                         },
   #else
   {   APSYS        ,IF_ODBC   ,DB_INGRES   ,NULL            ,NULL              ,NULL              ,"Apsys"           ,TRUE              ,FALSE        ,0              ,""           ,""        ,""                         },
   #endif
   #ifdef WAI_OWNER
   {   WAI          ,IF_OCI    ,DB_OTHERS   ,WAI_OWNER       ,NULL              ,NULL              ,"Datawarehouse"   ,TRUE              ,FALSE        ,0              ,""           ,""        ,""                         },
   #else
   {   WAI          ,IF_OCI    ,DB_OTHERS   ,NULL            ,NULL              ,NULL              ,"Datawarehouse"   ,TRUE              ,FALSE        ,0              ,""           ,""        ,""                         },
   #endif
   {   DWH          ,IF_OCI    ,DB_OTHERS   ,NULL            ,NULL              ,NULL              ,"DWH"             ,TRUE              ,FALSE        ,0              ,""           ,""        ,""                         },
   {   ACCESS_DB    ,IF_ODBC   ,DB_OTHERS   ,NULL            ,NULL              ,NULL              ,"MS-Access"       ,TRUE              ,FALSE        ,0              ,""           ,""        ,""                         },
   };


   //DBDesc
   //******

   const DBDESC far DBDesc[MAX_DBDESC]=
   {

  /****************************************************************************************************************************************************************************************************************************
   {   Tabelle:Nr   ,TabNr   ,szDBName    ,OrderBy         ,DefaultDesc       ,nFields   ,szName   ,szNameLanguage2   ,PrimaryKey   ,Flags          ,QueryFlags   ,FlagsEx   ,HistoryFieldNr   ,Object   },
   {   Feld:Nr      ,TabNr   ,szDBName    ,DBType          ,CType             ,Len       ,szName   ,szNameLanguage2   ,ForeignKey   ,Flags          ,QueryFlags   ,FlagsEx   ,HistoryFieldNr   ,Object   },
   ***************************************************************************************************************************************************************************************************************************/

   //obligatorischeEinträge
   //***********************

   {   DUAL         ,DUAL    ,"DUAL"      ,TAB             ,TAB               ,18        ,""       ,_T("")            ,NONE         ,DB_SYSTEM      ,0                                                   },
   {   USER         ,DUAL    ,"USER"      ,SQL_VARCHAR     ,SQL_C_CHAR        ,31        ,""       ,_T("")            ,NONE         ,0              ,0                                                   },
   {   SYSDATE      ,DUAL    ,"SYSDATE"   ,SQL_TIMESTAMP   ,SQL_C_TIMESTAMP   ,16        ,""       ,_T("")            ,NONE         ,0              ,0                                                   },
   {   ROWID        ,DUAL    ,"ROWID"     ,SQL_VARCHAR     ,SQL_C_CHAR        ,20        ,""       ,_T("")            ,NONE         ,DB_UNIQUEKEY   ,0                                                   },

