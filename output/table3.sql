{{ 
         config( 
            alias = 'stg_2', 
            materialized = 'view' 
        ) 
    }} 
    
select
    col1 as column_1,
    col2 as column_2,
    col3 as column_3,
    col4 as column_4,
    col5 as column_5,
    col6 as column_6,
    col7 as column_7,
    col8 as column_8,
    col9 as column_9,
    col10 as column_10
from {{ ref('table2') }}