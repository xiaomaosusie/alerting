select 
        advertiserid as buyerid,
        landingpagedomain,
        ppdrevenue,
        pdrevenue,
        round(difference,2) as difference,
        delta
from
(select
        spend.*,
        case when ppdrevenue > 0 then difference/ppdrevenue else 0 end as delta,
        sum(ppdrevenue) over (partition by advertiserid order by ppdrevenue desc) / sum(ppdrevenue) over (partition by advertiserid) as cum_pct
from
(select
        advertiserid,
        landingpagedomain,
        sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 2) then revenue else 0 end) as ppdrevenue,
        sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 1) then revenue else 0 end) as pdrevenue,
        ( sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 1) then revenue else 0 end) - 
        sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 2) then revenue else 0 end) ) as difference
from rpt.rptdaily
where day >= date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 2)
        and day < to_date(from_unixtime(iudf.det_unix_timestamp()))
      and advertiserid in (%s)
group by 1,2) spend
) res
where difference < 0