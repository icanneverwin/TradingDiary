
create_table_sql = {
  "oi_reports": """ CREATE TABLE IF NOT EXISTS oi_reports (
                        SYMBOL text NOT NULL,
                        DESC text NOT NULL,
                        OI_DATE text NOT NULL,
                        GLOBEX_VOLUME int NOT NULL,
                        VOLUME int NOT NULL,
                        OPEN_INTEREST int NOT NULL,
                        CHANGE int NOT NULL,
                        PRELIMINARY_IND TEXT NOT NULL,
                        PRIMARY KEY (SYMBOL, OI_DATE)
                      );
                  """,
  "cot_reports": """ CREATE TABLE IF NOT EXISTS cot_reports (
                          SYMBOL text NOT NULL,
                          COT_DATE text NOT NULL,
                          OI_ALL int NOT NULL,
                          NONCOMM_POS_LONG int NOT NULL,
                          NONCOMM_POS_SHORT int NOT NULL,
                          COMM_POS_LONG int NOT NULL,
                          COMM_POS_SHORT int NOT NULL,
                          CHANGE_OI int NOT NULL,
                          CHANGE_NONCOMM_LONG int NOT NULL,
                          CHANGE_NONCOMM_SHORT int NOT NULL,
                          CHANGE_COMM_LONG int NOT NULL,
                          CHANGE_COMM_SHORT int NOT NULL,
                          PCT_OI_NONCOMM_LONG real NOT NULL,
                          PCT_OI_NONCOMM_SHORT real NOT NULL,
                          PCT_OI_COMM_LONG real NOT NULL,
                          PCT_OI_COMM_SHORT real NOT NULL,
                          
                          PRIMARY KEY (SYMBOL, COT_DATE)
                        );
                    """
}

db_check = {
  "oi_reports": "select count(name) from sqlite_master where type = 'table' and name = 'oi_reports'",
  "cot_reports": "select count(name) from sqlite_master where type = 'table' and name = 'cot_reports'"
}