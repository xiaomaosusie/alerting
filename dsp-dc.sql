select 
        buyerid,
        dc,
        ppdrevenue,
        pdrevenue,
        round(difference,2) as difference,
        case when ppdrevenue > 0 then difference/ppdrevenue else 0 end as delta
from
(select
        buyerid,
        case when datacenter = 1 then 'LGA' when datacenter = 3 then 'AMS' when datacenter = 4 then 'SJC'else 'N/A' end as dc,
        sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 2) then revenue else 0 end) as ppdrevenue,
        sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 1) then revenue else 0 end) as pdrevenue,
        ( sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 1) then revenue else 0 end) - 
        sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 2) then revenue else 0 end) ) as difference
from rtb.rtbspenddaily
where day >= to_date(date_sub(now(), 2))
        and day < to_date(from_unixtime(iudf.det_unix_timestamp()))
      and buyerid in (%s)
group by 1,2) spend