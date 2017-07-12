SELECT
    dspbdev.accountname AS Advertiser,
    dspbdev.am     AS AM,
    dspbdev.email,
    PD.*,
    PPD.*,
    4D.*,
    7D.*,
    --revenue delta
    Revenue_cur-pdrevenue as rev_diff_agst_pd_cur,
    CASE WHEN pdrevenue > 0 THEN ROUND((Revenue_cur-pdrevenue)/pdrevenue*100,1) ELSE 0.0 END as revenue_change_agst_pd_pct,
    CASE WHEN 4davgrevenue > 0 THEN ROUND((Revenue_cur-4davgRevenue)/4davgRevenue*100,1) ELSE 0.0 END as revenue_change_agst_4davg_pct,
    CASE WHEN 7davgrevenue > 0 THEN ROUND((Revenue_cur-7davgRevenue)/7davgRevenue*100,1) ELSE 0.0 END as revenue_change_agst_7davg_pct,
    --offer delta
    CASE WHEN pdbidsofferedtotal > 0 THEN ROUND((offer_mm-pdbidsofferedtotal)/pdbidsofferedtotal*100,1) ELSE 0.0 END as offer_change_agst_pd_pct,
    CASE WHEN 4davgbidsofferedtotal > 0 THEN ROUND((offer_mm-4davgbidsofferedtotal)/4davgbidsofferedtotal*100,1) ELSE 0.0 END as offer_change_agst_4davg_pct,
    CASE WHEN 7davgbidsofferedtotal > 0 THEN ROUND((offer_mm-7davgbidsofferedtotal)/7davgbidsofferedtotal*100,1) ELSE 0.0 END as offer_change_agst_7davg_pct,
    --offerrate delta
    CASE WHEN pdofferrate > 0 THEN ROUND((offerrate_pct-pdofferrate)/pdofferrate*100,1) ELSE 0.0 END as offerrate_change_agst_pd_pct,
    CASE WHEN 4dofferrate > 0 THEN ROUND((offerrate_pct-4dofferrate)/4dofferrate*100,1) ELSE 0.0 END as offerrate_change_agst_4davg_pct,
    CASE WHEN 7dofferrate > 0 THEN ROUND((offerrate_pct-7dofferrate)/7dofferrate*100,1) ELSE 0.0 END as offerrate_change_agst_7davg_pct,
    --offermatch rate delta
    CASE WHEN pdoffermatchrate > 0 THEN ROUND((offermatchrate_pct-pdoffermatchrate)/pdoffermatchrate*100,1) ELSE 0.0 END as offermatchrate_change_agst_pd_pct,
    CASE WHEN 4doffermatchrate > 0 THEN ROUND((offermatchrate_pct-4doffermatchrate)/4doffermatchrate*100,1) ELSE 0.0 END as offermatchrate_change_agst_4davg_pct,
    CASE WHEN 7doffermatchrate > 0 THEN ROUND((offermatchrate_pct-7doffermatchrate)/7doffermatchrate*100,1) ELSE 0.0 END as offermatchrate_change_agst_7davg_pct,
    --bidrate delta
    CASE WHEN pdbidrate > 0 THEN ROUND((bidrate_pct-pdbidrate)/pdbidrate*100,1) ELSE 0.0 END as bidrate_change_agst_pd_pct,
    CASE WHEN 4dbidrate > 0 THEN ROUND((bidrate_pct-4dbidrate)/4dbidrate*100,1) ELSE 0.0 END as bidrate_change_agst_4davg_pct,
    CASE WHEN 7dbidrate > 0 THEN ROUND((bidrate_pct-7dbidrate)/7dbidrate*100,1) ELSE 0.0 END as bidrate_change_agst_7davg_pct,
    --block delta
    CASE WHEN pdblockrate > 0 THEN ROUND((blockrate_pct-pdblockrate)/pdblockrate*100,1) ELSE 0.0 END as blockrate_change_agst_pd_pct,
    CASE WHEN 4dblockrate > 0 THEN ROUND((blockrate_pct-4dblockrate)/4dblockrate*100,1) ELSE 0.0 END as blockrate_change_agst_4davg_pct,
    CASE WHEN 7dblockrate > 0 THEN ROUND((blockrate_pct-7dblockrate)/7dblockrate*100,1) ELSE 0.0 END as blockrate_change_agst_7davg_pct,
    --winrate delta
    CASE WHEN pdwinrate > 0 THEN ROUND((winrate_pct-pdwinrate)/pdwinrate*100,1) ELSE 0.0 END as winrate_change_agst_pd_pct,
    CASE WHEN 4dwinrate > 0 THEN ROUND((winrate_pct-4dwinrate)/4dwinrate*100,1) ELSE 0.0 END as winrate_change_agst_4davg_pct,
    CASE WHEN 7dwinrate > 0 THEN ROUND((winrate_pct-7dwinrate)/7dwinrate*100,1) ELSE 0.0 END as winrate_change_agst_7davg_pct,
    --revcpm delta
    CASE WHEN pdrevcpm > 0 THEN ROUND((revcpm_cur-pdrevcpm)/pdrevcpm*100,1) ELSE 0.0 END as revcpm_change_agst_pd_pct,
    CASE WHEN 4drevcpm > 0 THEN ROUND((revcpm_cur-4drevcpm)/4drevcpm*100,1) ELSE 0.0 END as revcpm_change_agst_4davg_pct,
    CASE WHEN 7drevcpm > 0 THEN ROUND((revcpm_cur-7drevcpm)/7drevcpm*100,1) ELSE 0.0 END as revcpm_change_agst_7davg_pct,
    --costcpm delta
    CASE WHEN pdcostcpm > 0 THEN ROUND((costcpm_cur-pdcostcpm)/pdcostcpm*100,1) ELSE 0.0 END as costcpm_change_agst_pd_pct,
    CASE WHEN 4dcostcpm > 0 THEN ROUND((costcpm_cur-4dcostcpm)/4dcostcpm*100,1) ELSE 0.0 END as costcpm_change_agst_4davg_pct,
    CASE WHEN 7dcostcpm > 0 THEN ROUND((costcpm_cur-7dcostcpm)/7dcostcpm*100,1) ELSE 0.0 END as costcpm_change_agst_7davg_pct,
    --margin delta
    CASE WHEN pdmargin > 0 THEN ROUND((margin_pct-pdmargin)/pdmargin*100,1) ELSE 0.0 END as margin_change_agst_pd_pct,
    CASE WHEN 4dmargin > 0 THEN ROUND((margin_pct-4dmargin)/4dmargin*100,1) ELSE 0.0 END as margin_change_agst_4davg_pct,
    CASE WHEN 7dmargin > 0 THEN ROUND((margin_pct-7dmargin)/7dmargin*100,1) ELSE 0.0 END as margin_change_agst_7davg_pct,
    --timeout delta
    CASE WHEN pdtimeoutrate > 0 THEN ROUND((timeoutrate_pct-pdtimeoutrate)/pdtimeoutrate*100,1) ELSE 0.0 END as timeoutrate_change_agst_pd_pct,
    CASE WHEN 4dtimeoutrate > 0 THEN ROUND((timeoutrate_pct-4dtimeoutrate)/4dtimeoutrate*100,1) ELSE 0.0 END as timeoutrate_change_agst_4davg_pct,
    CASE WHEN 7dtimeoutrate > 0 THEN ROUND((timeoutrate_pct-7dtimeoutrate)/7dtimeoutrate*100,1) ELSE 0.0 END as timeoutrate_change_agst_7davg_pct
FROM
    (
        SELECT
            a.day,
            a.accountid,
            bidsofferedtotal as offer_mm,
            CASE WHEN BidsOfferedTotal > 0 THEN ROUND(MatchedBidsOfferedTotal/BidsOfferedTotal*100) ELSE 0 END AS offermatchrate_pct,
            CASE WHEN BidsOfferedTotal > 0 THEN ROUND(BidsMadeTotal/BidsOfferedTotal*100,1) ELSE 0.0 END AS bidrate_pct,
            CASE WHEN BidsOfferedTotal > 0 THEN ROUND(TimeOuts/BidsOfferedTotal*100,1) ELSE 0.0 END AS timeoutrate_pct,
            CASE WHEN BidsMadeTotal > 0 THEN ROUND(Blocks/BidsMadeTotal*100,1) ELSE 0.0 END AS blockrate_pct,
            CASE WHEN BidsMadeTotal > 0 THEN ROUND(COALESCE(PaidImpressions, 0)/BidsMadeTotal*100,1) ELSE 0.0 END AS winrate_pct,
            ROUND(COALESCE(Revenue, 0)) AS Revenue_cur,
            CASE WHEN PaidImpressions > 0 THEN ROUND(COALESCE(Revenue, 0.0)/PaidImpressions*1000, 2) ELSE 0.0 END AS revcpm_cur,
            CASE WHEN PaidImpressions > 0 THEN ROUND(COALESCE(Cost, 0.0)/PaidImpressions*1000, 2) ELSE 0.0 END AS costcpm_cur,
            CASE WHEN Revenue > 0 THEN ROUND((1-COALESCE(Cost, 0)/Revenue)*100,1) ELSE 0.0 END AS margin_pct,
            CASE WHEN passedimps > 0 THEN ROUND(BidsOfferedTotal/passedimps*100,1) ELSE 0.0 END AS offerrate_pct
        FROM
            (
                SELECT
                    DAY,
                    buyerid as accountid,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN BidsOffered
                            ELSE 0
                        END)         AS MatchedBidsOfferedTotal,
                    SUM(BidsOffered) AS BidsOfferedTotal,
                    SUM(BidsMade)    AS BidsMadeTotal,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN BidsMade
                            ELSE 0
                        END)                  AS MatchedBidsMadeTotal,
                    SUM(TimeOuts)             AS TimeOuts,
                    SUM(ConnectionErrors)     AS ConnectionErrors,
                    SUM(BadResponses)         AS BadResponses,
                    SUM(PublisherblockedBids) AS Blocks
                FROM
                    rtb.RTBKpiDaily
                WHERE
                    DAY = to_date(date_sub(now(), 1))
                GROUP BY
                    1,2) a
        LEFT JOIN
            (
                SELECT
                    DAY,
                    BuyerId as accountid,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN PaidImpressions
                            ELSE 0
                        END)             AS MatchedPaidImpressions,
                    SUM(PaidImpressions) AS PaidImpressions,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN Cost
                            ELSE 0
                        END)  AS MatchedCost,
                    SUM(Cost) AS Cost,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN Revenue
                            ELSE 0
                        END)     AS MatchedRevenue,
                    SUM(Revenue) AS Revenue
                FROM
                    rtb.RTBSpendDaily
                WHERE
                    DAY = to_date(date_sub(now(), 1))
                GROUP BY
                    1,2) b
        ON
            a.accountid=b.accountid
        AND a.day=b.day
        LEFT JOIN
            (
                SELECT
                    DAY,
                    SUM(total_passed_impressions) AS passedimps
                FROM
                    rpt.kpidaily
                WHERE
                    DAY = to_date(date_sub(now(), 1))
                GROUP BY
                    1) pass
        ON
            a.day = pass.day ) PD
LEFT JOIN
    (
        SELECT
            a.accountid,
            bidsOfferedtotal                                    AS pdbidsofferedtotal,
            CASE WHEN BidsOfferedTotal > 0 THEN ROUND(MatchedBidsOfferedTotal/BidsOfferedTotal*100) ELSE 0 END AS pdoffermatchrate,
            CASE WHEN BidsOfferedTotal > 0 THEN ROUND(BidsMadeTotal/BidsOfferedTotal*100,1) ELSE 0.0 END AS pdbidrate,
            CASE WHEN BidsOfferedTotal > 0 THEN ROUND(TimeOuts/BidsOfferedTotal*100,1) ELSE 0.0 END AS pdtimeoutrate,
            CASE WHEN BidsMadeTotal > 0 THEN ROUND(Blocks/BidsMadeTotal*100,1) ELSE 0.0 END AS pdblockrate,
            CASE WHEN BidsMadeTotal > 0 THEN ROUND(COALESCE(PaidImpressions, 0)/BidsMadeTotal*100,1) ELSE 0.0 END AS pdwinrate,
            ROUND(COALESCE(Revenue, 0)) AS pdrevenue,
            CASE WHEN PaidImpressions > 0 THEN ROUND(COALESCE(Revenue, 0.0)/PaidImpressions*1000, 2) ELSE 0.0 END AS pdrevcpm,
            CASE WHEN PaidImpressions > 0 THEN ROUND(COALESCE(Cost, 0.0)/PaidImpressions*1000, 2) ELSE 0.0 END AS pdcostcpm,
            CASE WHEN Revenue > 0 THEN ROUND((1-COALESCE(Cost, 0)/Revenue)*100,1) ELSE 0.0 END AS pdmargin,
            CASE WHEN passedimps > 0 THEN ROUND(BidsOfferedTotal/passedimps*100,1) ELSE 0.0 END AS pdofferrate
        FROM
            (
                SELECT
                    DAY,
                    buyerid as accountid,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN BidsOffered
                            ELSE 0
                        END)         AS MatchedBidsOfferedTotal,
                    SUM(BidsOffered) AS BidsOfferedTotal,
                    SUM(BidsMade)    AS BidsMadeTotal,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN BidsMade
                            ELSE 0
                        END)                  AS MatchedBidsMadeTotal,
                    SUM(TimeOuts)             AS TimeOuts,
                    SUM(ConnectionErrors)     AS ConnectionErrors,
                    SUM(BadResponses)         AS BadResponses,
                    SUM(PublisherblockedBids) AS Blocks
                FROM
                    rtb.RTBKpiDaily
                WHERE
                    DAY = to_date(date_sub(now(), 2))
                GROUP BY
                    1,2) a
        LEFT JOIN
            (
                SELECT
                    DAY,
                    buyerid as accountid,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN PaidImpressions
                            ELSE 0
                        END)             AS MatchedPaidImpressions,
                    SUM(PaidImpressions) AS PaidImpressions,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN Cost
                            ELSE 0
                        END)  AS MatchedCost,
                    SUM(Cost) AS Cost,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN Revenue
                            ELSE 0
                        END)     AS MatchedRevenue,
                    SUM(Revenue) AS Revenue
                FROM
                    rtb.RTBSpendDaily
                WHERE
                    DAY = to_date(date_sub(now(), 2))
                GROUP BY
                    1,2) b
        ON
            a.accountid=b.accountid
        AND a.day=b.day
        LEFT JOIN
            (
                SELECT
                    DAY,
                    SUM(total_passed_impressions) AS passedimps
                FROM
                    rpt.kpidaily
                WHERE
                    DAY = to_date(date_sub(now(), 2))
                GROUP BY
                    1) pass
        ON
            a.day = pass.day ) PPD
ON
    pd.accountid = ppd.accountid
LEFT JOIN
    (
        SELECT
            a.accountid,
            ROUND(SUM(BidsOfferedTotal)/COUNT(DISTINCT a.day))            AS 4davgbidsofferedtotal,
            CASE WHEN SUM(BidsOfferedTotal) > 0 THEN ROUND(SUM(MatchedBidsOfferedTotal)/SUM(BidsOfferedTotal)*100) ELSE 0 END AS 4doffermatchrate,
            CASE WHEN SUM(BidsOfferedTotal) > 0 THEN ROUND(SUM(BidsMadeTotal)/SUM(BidsOfferedTotal)*100,1) ELSE 0.0 END AS 4dbidrate,
            CASE WHEN SUM(BidsOfferedTotal) > 0 THEN ROUND(SUM(TimeOuts)/SUM(BidsOfferedTotal)*100,1) ELSE 0.0 END AS 4dtimeoutrate,
            CASE WHEN SUM(BidsMadeTotal) > 0 THEN ROUND(SUM(Blocks)/SUM(BidsMadeTotal)*100,1) ELSE 0.0 END AS 4dblockrate,
            CASE WHEN SUM(BidsMadeTotal) > 0 THEN ROUND(SUM(COALESCE(PaidImpressions, 0))/SUM(BidsMadeTotal)*100,1) ELSE 0.0 END AS 4dwinrate,
            ROUND(SUM(COALESCE(Revenue, 0))/COUNT(DISTINCT a.day))       AS 4davgRevenue,
            CASE WHEN SUM(PaidImpressions) > 0 THEN ROUND(SUM(COALESCE(Revenue, 0))/SUM(PaidImpressions)*1000, 2) ELSE 0.0 END AS 4drevcpm,
            CASE WHEN SUM(PaidImpressions) > 0 THEN ROUND(SUM(COALESCE(Cost, 0))/SUM(PaidImpressions)*1000, 2) ELSE 0.0 END AS 4dcostcpm,
            CASE WHEN SUM(Revenue) > 0 THEN ROUND((1-SUM(COALESCE(Cost, 0))/SUM(Revenue))*100,1) ELSE 0.0 END  AS 4dmargin,
            CASE WHEN SUM(passedimps) > 0 THEN ROUND(SUM(BidsOfferedTotal)/SUM(passedimps)*100,1) ELSE 0.0 END  AS 4dofferrate
        FROM
            (
                SELECT
                    DAY,
                    BuyerId as accountid,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN BidsOffered
                            ELSE 0
                        END)         AS MatchedBidsOfferedTotal,
                    SUM(BidsOffered) AS BidsOfferedTotal,
                    SUM(BidsMade)    AS BidsMadeTotal,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN BidsMade
                            ELSE 0
                        END)                  AS MatchedBidsMadeTotal,
                    SUM(TimeOuts)             AS TimeOuts,
                    SUM(ConnectionErrors)     AS ConnectionErrors,
                    SUM(BadResponses)         AS BadResponses,
                    SUM(PublisherblockedBids) AS Blocks
                FROM
                    rtb.RTBKpiDaily
                WHERE
                    DAY >= to_date(date_sub(now(), 5))
                AND DAY < to_date(date_sub(now(), 1))
                GROUP BY
                    1,2) a
        LEFT JOIN
            (
                SELECT
                    DAY,
                    BuyerId as accountid,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN PaidImpressions
                            ELSE 0
                        END)             AS MatchedPaidImpressions,
                    SUM(PaidImpressions) AS PaidImpressions,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN Cost
                            ELSE 0
                        END)  AS MatchedCost,
                    SUM(Cost) AS Cost,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN Revenue
                            ELSE 0
                        END)     AS MatchedRevenue,
                    SUM(Revenue) AS Revenue
                FROM
                    rtb.RTBSpendDaily
                WHERE
                    DAY >= to_date(date_sub(now(), 5))
                AND DAY < to_date(date_sub(now(), 1))
                GROUP BY
                    1,2) b
        ON
            a.accountid=b.accountid
        AND a.day=b.day
        LEFT JOIN
            (
                SELECT
                    DAY,
                    SUM(total_passed_impressions) AS passedimps
                FROM
                    rpt.kpidaily
                WHERE
                    DAY >= to_date(date_sub(now(), 5))
                AND DAY < to_date(date_sub(now(), 1))
                GROUP BY
                    1) pass
        ON
            a.day = pass.day
        GROUP BY
            a.accountid ) 4D
ON
    pd.accountid = 4D.accountid
LEFT JOIN
    (
        SELECT
            a.accountid,
            ROUND(SUM(BidsOfferedTotal)/COUNT(DISTINCT a.day))            AS 7davgbidsofferedtotal,
            CASE WHEN SUM(BidsOfferedTotal) > 0 THEN ROUND(SUM(MatchedBidsOfferedTotal)/SUM(BidsOfferedTotal)*100) ELSE 0 END AS 7doffermatchrate,
            CASE WHEN SUM(BidsOfferedTotal) > 0 THEN ROUND(SUM(BidsMadeTotal)/SUM(BidsOfferedTotal)*100,1) ELSE 0.0 END AS 7dbidrate,
            CASE WHEN SUM(BidsOfferedTotal) > 0 THEN ROUND(SUM(TimeOuts)/SUM(BidsOfferedTotal)*100,1) ELSE 0.0 END AS 7dtimeoutrate,
            CASE WHEN SUM(BidsMadeTotal) > 0 THEN ROUND(SUM(Blocks)/SUM(BidsMadeTotal)*100,1) ELSE 0.0 END AS 7dblockrate,
            CASE WHEN SUM(BidsMadeTotal) > 0 THEN ROUND(SUM(COALESCE(PaidImpressions, 0))/SUM(BidsMadeTotal)*100,1) ELSE 0.0 END AS 7dwinrate,
            ROUND(SUM(COALESCE(Revenue, 0))/COUNT(DISTINCT a.day))       AS 7davgRevenue,
            CASE WHEN SUM(PaidImpressions) > 0 THEN ROUND(SUM(COALESCE(Revenue, 0))/SUM(PaidImpressions)*1000, 2) ELSE 0.0 END AS 7drevcpm,
            CASE WHEN SUM(PaidImpressions) > 0 THEN ROUND(SUM(COALESCE(Cost, 0))/SUM(PaidImpressions)*1000, 2) ELSE 0.0 END AS 7dcostcpm,
            CASE WHEN SUM(Revenue) > 0 THEN ROUND((1-SUM(COALESCE(Cost, 0))/SUM(Revenue))*100,1) ELSE 0.0 END  AS 7dmargin,
            CASE WHEN SUM(passedimps) > 0 THEN ROUND(SUM(BidsOfferedTotal)/SUM(passedimps)*100,1) ELSE 0.0 END  AS 7dofferrate
        FROM
            (
                SELECT
                    DAY,
                    BuyerId as accountid,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN BidsOffered
                            ELSE 0
                        END)         AS MatchedBidsOfferedTotal,
                    SUM(BidsOffered) AS BidsOfferedTotal,
                    SUM(BidsMade)    AS BidsMadeTotal,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN BidsMade
                            ELSE 0
                        END)                  AS MatchedBidsMadeTotal,
                    SUM(TimeOuts)             AS TimeOuts,
                    SUM(ConnectionErrors)     AS ConnectionErrors,
                    SUM(BadResponses)         AS BadResponses,
                    SUM(PublisherblockedBids) AS Blocks
                FROM
                    rtb.RTBKpiDaily
                WHERE
                    DAY >= to_date(date_sub(now(), 8))
                AND DAY < to_date(date_sub(now(), 1))
                GROUP BY
                    1,2) a
        LEFT JOIN
            (
                SELECT
                    DAY,
                    BuyerId as accountid,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN PaidImpressions
                            ELSE 0
                        END)             AS MatchedPaidImpressions,
                    SUM(PaidImpressions) AS PaidImpressions,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN Cost
                            ELSE 0
                        END)  AS MatchedCost,
                    SUM(Cost) AS Cost,
                    SUM(
                        CASE
                            WHEN CookieMatch = 1
                            THEN Revenue
                            ELSE 0
                        END)     AS MatchedRevenue,
                    SUM(Revenue) AS Revenue
                FROM
                    rtb.RTBSpendDaily
                WHERE
                    DAY >= to_date(date_sub(now(), 8))
                AND DAY < to_date(date_sub(now(), 1))
                GROUP BY
                    1,2) b
        ON
            a.accountid=b.accountid
        AND a.day=b.day
        LEFT JOIN
            (
                SELECT
                    DAY,
                    SUM(total_passed_impressions) AS passedimps
                FROM
                    rpt.kpidaily
                WHERE
                    DAY >= to_date(date_sub(now(), 8))
                AND DAY < to_date(date_sub(now(), 1))
                GROUP BY
                    1) pass
        ON
            a.day = pass.day
        GROUP BY
            a.accountid ) 7D
ON
    pd.accountid = 7D.accountid
LEFT JOIN
    (
        SELECT
            ma.accountid,
            ma.accountname,
            am.firstname AS AM,
            am.email
        FROM
            reference.masteraccount ma
        LEFT JOIN
            reference.accountcontact ac
        ON
            ac.accountid = ma.accountid
        LEFT JOIN
            reference.accountowner am
        ON
            am.id = ac.AccountManagerId
        WHERE
            (
                ma.accountname NOT LIKE '%test%')
        AND (
                ma.accountname NOT LIKE '%Test%')
        AND (
                ma.accountname NOT LIKE '%TEST%')
        AND (
                ma.accountname NOT LIKE '%Nikolay%')
        ) dspbdev
ON
    dspbdev.accountid = pd.accountid

order by pd.Revenue_cur desc 
