select 
        advertiserid as accountid,
        landingpagedomain as campaign,
        round(ppdrevenue, 0) as ppdrevenue_cur,
        round(pdrevenue, 0) as pdrevenue_cur,
        round(difference, 0) as difference_cur,
        case when ppdrevenue > 0 then 100*difference/ppdrevenue else 0 end as delta_pct
from
(select
        advertiserid,
        landingpagedomain,
        sum(case when day = to_date(date_sub(now(), 2)) then revenue else 0 end) as ppdrevenue,
        sum(case when day = to_date(date_sub(now(), 1))then revenue else 0 end) as pdrevenue,
        ( sum(case when day = to_date(date_sub(now(), 1)) then revenue else 0 end) - 
        sum(case when day = to_date(date_sub(now(), 2)) then revenue else 0 end) ) as difference
from rpt.rptdaily
where day >= to_date(date_sub(now(), 2))
        and day < to_date(from_unixtime(iudf.det_unix_timestamp()))
      and advertiserid in ({0})
group by 1,2) x 