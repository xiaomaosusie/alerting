select 
        buyerid,
        publisherid,
        ma.accountname as publisher,
        ppdrevenue,
        pdrevenue,
        rev_difference,
        rev_delta,
        offer_difference,
        offer_delta
from
(select
        spend.*,
        rev_difference/ppdrevenue as rev_delta,
        offer_difference,
        offer_delta,
        sum(ppdrevenue) over (partition by spend.buyerid order by ppdrevenue desc) / sum(ppdrevenue) over (partition by spend.buyerid) as cum_pct
from
(select
        buyerid,
        publisherid,
        sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 2) then revenue else 0 end) as ppdrevenue,
        sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 1) then revenue else 0 end) as pdrevenue,
        ( sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 1) then revenue else 0 end) - 
        sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 2) then revenue else 0 end) ) as rev_difference
from rtb.rtbspenddaily
where day >= date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 2)
        and day < to_date(from_unixtime(iudf.det_unix_timestamp()))
      and buyerid in (%s)
group by 1,2) spend
left join
        (select
        buyerid,
        publisherid,
        sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 2) then bidsoffered else 0 end) as ppdoffer,
        sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 1) then bidsoffered else 0 end) as pdoffer,
        ( sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 1) then bidsoffered else 0 end) - 
        sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 2) then bidsoffered else 0 end) ) as offer_difference,
        ( sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 1) then bidsoffered else 0 end) - 
        sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 2) then bidsoffered else 0 end) )/
        sum(case when day = date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 2) then bidsoffered else 0 end) as offer_delta
from rtb.rtbkpidaily
where day >= date_sub(from_unixtime(iudf.det_unix_timestamp(), 'yyyy-MM-dd'), 2)
        and day < to_date(from_unixtime(iudf.det_unix_timestamp()))
      and buyerid in (%s)
group by 1,2) offer
on spend.buyerid = offer.buyerid and spend.publisherid = offer.publisherid
) res
left join reference.masteraccount ma
on res.publisherid = ma.accountid
where cum_pct <= 0.8