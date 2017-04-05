select 
        buyerid,
        channel,
        ppdrevenue,
        pdrevenue,
        round(difference,2) as difference,
        case when ppdrevenue > 0 then difference/ppdrevenue else 0 end as delta
from
(select
        buyerid,
        case when channel = 1 then 'vieo' when channel = 0 then 'display' else 'N/A' end as channel,
        sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 2) then revenue else 0 end) as ppdrevenue,
        sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 1) then revenue else 0 end) as pdrevenue,
        ( sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 1) then revenue else 0 end) - 
        sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 2) then revenue else 0 end) ) as difference
from rtb.rtbspenddaily
where day >= date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 2)
        and day < to_date(from_unixtime(iudf.det_unix_timestamp()))
      and buyerid in (%s)
group by 1,2) spend
