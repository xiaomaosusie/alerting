select 
        buyerid as accountid, 
        ma.accountname, 
        rtb.blockedcreativereason, 
        bcr.blockedcreativereasonname,
        sum(impressions) as impressions
from rtb.rtbsummarydaily rtb
left join reference.MasterAccount ma on ma.AccountId = rtb.buyerId
left join reference.BlockedCreativeReasons bcr on bcr.BlockedCreativeReasonId = rtb.BlockedCreativeReason
where day = to_date(date_sub(now(), 1))
        and buyererrorcode = 'BLOCKED_CREATIVE_URL'
        and rtbeventid = 'BUYER_BID' 
        and buyerid in ({0})
group by 1,2,3,4