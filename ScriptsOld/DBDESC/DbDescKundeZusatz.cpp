/**************************************************************************
 DBDESCKUNDEZUSATZ.CPP
 **************************************************************************
 Projekt      : ApWare - WinDekis
 Copyright    : SunGard Ambit CRM
 Compiler     : Borland C++
 Beschreibung : Enthält Datenbankbeschreibungslinien des Projekts
                Von ApWare in den Project Ordner kopieren und
                projektspezifisch erweitern
 **************************************************************************

 Datum        Vers   Vis   Beschreibung
 -----        ----   ---   ------------

 27.12.2004   1.00   Ak    1. Ausgabe

 **************************************************************************/


/*****************************************************************************************************************************
 {     Tabelle:Nr   ,TabNr   ,szDBName   ,OrderBy   ,DefaultDesc   ,nFields   ,szName   ,szNameLanguage2   ,PrimaryKey   ,Flags   ,QueryFlags   },
 {     Feld:Nr      ,TabNr   ,szDBName   ,DBType    ,CType         ,Len       ,szName   ,szNameLanguage2   ,ForeignKey   ,Flags   ,QueryFlags   },
 ****************************************************************************************************************************/

   {    KUNDE_KUNDENID_ACCNAMELONG,                           _T("Kunden Id/Bezeichnungvertrag"),         _T("Client Id/Account name long")        },
   #ifdef __OPENING_APPROVAL__
   {    KUNDE_APPROVAL_STATUS_CD,                             _T("Approval Status"),                      _T("Approval Status"),                   },
   {    KUNDE_CLIENT_STATUS_CD,                               _T("Client Status"),                        _T("Client Status"),                     },
   {    KUNDE_APPROVAL_STEP1_CD,                              _T("Step 1 Approval Decision"),             _T("Step 1 Approval Decision"),          },
   {    KUNDE_APPROVAL_STEP1_ASSESSMENT_CD,                   _T("Step 1 Approval Assessment"),           _T("Step 1 Approval Assessment"),        },
   {    KUNDE_APPROVAL_STEP1_USER,                            _T("Step 1 Approval User"),                 _T("Step 1 Approval User"),              },
   {    KUNDE_APPROVAL_STEP1_DATE,                            _T("Step 1 Approval Date"),                 _T("Step 1 Approval Date"),              },
   {    KUNDE_APPROVAL_STEP1_BEM,                             _T("Step 1 Approval Comment"),              _T("Step 1 Approval Comment"),           },
   {    KUNDE_APPROVAL_STEP2_CD,                              _T("Step 2 Approval Decision"),             _T("Step 2 Approval Decision"),          },
   {    KUNDE_APPROVAL_STEP2_ASSESSMENT_CD,                   _T("Step 2 Approval Assessment"),           _T("Step 2 Approval Assessment"),        },
   {    KUNDE_APPROVAL_STEP2_USER,                            _T("Step 2 Approval User"),                 _T("Step 2 Approval User"),              },
   {    KUNDE_APPROVAL_STEP2_DATE,                            _T("Step 2 Approval Date"),                 _T("Step 2 Approval Date"),              },
   {    KUNDE_APPROVAL_STEP2_BEM,                             _T("Step 2 Approval Comment"),              _T("Step 2 Approval Comment"),           },
   {    KUNDE_APPROVAL_STEP3_CD,                              _T("Step 3 Approval Decision"),             _T("Step 3 Approval Decision"),          },
   {    KUNDE_APPROVAL_STEP3_ASSESSMENT_CD,                   _T("Step 3 Approval Assessment"),           _T("Step 3 Approval Assessment"),        },
   {    KUNDE_APPROVAL_STEP3_USER,                            _T("Step 3 Approval User"),                 _T("Step 3 Approval User"),              },
   {    KUNDE_APPROVAL_STEP3_DATE,                            _T("Step 3 Approval Date"),                 _T("Step 3 Approval Date"),              },
   {    KUNDE_APPROVAL_STEP3_BEM,                             _T("Step 3 Approval Comment"),              _T("Step 3 Approval Comment"),           },
   {    KUNDE_APPROVAL_STEP4_CD,                              _T("Step 4 Approval Decision"),             _T("Step 4 Approval Decision"),          },
   {    KUNDE_APPROVAL_STEP4_ASSESSMENT_CD,                   _T("Step 4 Approval Assessment"),           _T("Step 4 Approval Assessment"),        },
   {    KUNDE_APPROVAL_STEP4_USER,                            _T("Step 4 Approval User"),                 _T("Step 4 Approval User"),              },
   {    KUNDE_APPROVAL_STEP4_DATE,                            _T("Step 4 Approval Date"),                 _T("Step 4 Approval Date"),              },
   {    KUNDE_APPROVAL_STEP4_BEM,                             _T("Step 4 Approval Comment"),              _T("Step 4 Approval Comment"),           },
   {    KUNDE_APPROVAL_STEP5_CD,                              _T("Step 5 Approval Decision"),             _T("Step 5 Approval Decision"),          },
   {    KUNDE_APPROVAL_STEP5_ASSESSMENT_CD,                   _T("Step 5 Approval Assessment"),           _T("Step 5 Approval Assessment"),        },
   {    KUNDE_APPROVAL_STEP5_USER,                            _T("Step 5 Approval User"),                 _T("Step 5 Approval User"),              },
   {    KUNDE_APPROVAL_STEP5_DATE,                            _T("Step 5 Approval Date"),                 _T("Step 5 Approval Date"),              },
   {    KUNDE_APPROVAL_STEP5_BEM,                             _T("Step 5 Approval Comment"),              _T("Step 5 Approval Comment"),           },
   #endif

