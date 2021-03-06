select 
        accountid,
        dc,
        ppdrevenue,
        pdrevenue,
        round(difference,2) as difference,
        case when ppdrevenue > 0 then 100*difference/ppdrevenue else 0 end as delta
from
(select
        buyerid as accountid,
        case when datacenter = 1 then 'LGA' when datacenter = 3 then 'AMS' when datacenter = 4 then 'SJC'else 'N/A' end as dc,
        sum(case when day = to_date(date_sub(now(), 2)) then revenue else 0 end) as ppdrevenue,
        sum(case when day = to_date(date_sub(now(), 1)) then revenue else 0 end) as pdrevenue,
        ( sum(case when day = to_date(date_sub(now(), 1)) then revenue else 0 end) - 
        sum(case when day = to_date(date_sub(now(), 2)) then revenue else 0 end) ) as difference
from rtb.rtbspenddaily
where day >= to_date(date_sub(now(), 2))
        and day < to_date(from_unixtime(iudf.det_unix_timestamp()))
      and buyerid in ({0})
group by 1,2) spend