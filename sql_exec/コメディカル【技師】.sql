
/*
SMSバッチ：Ver.1.0 2024/03/15
author：s12100400
コメディカル【技師】
*/

with v_career as (
    select
        replace(replace(crBase.telhome,'-',''),' ','') telhomeNo
        ,replace(replace(crBase.telcellular,'-',''),' ','') telcellularNo
        ,*
    from
        "MNVM".trncareer crBase
    where
        crBase.delete_date is null
    /********* デフォルト値(変更不可) **********/
    and crBase.regstatus_id not in (5,6,8,9,3,4) --登録ステータス【活動休止・退会・決定】決定はアプローチステータス？
    /*

    1;"仮登録"
    2;"活動中"
    3;"自社決定"
    4;"他社決定"
    5;"活動休止"
    6;"退会"
    8;"重複のため停止"
    9;"個人情報削除"

    */

    and crBase.cnslstatus_id not in (35,36,15,16,33)  --アプローチステータス【リリース・NG・非有効・決定・NG対応済】

    /*
    15;"NG"
    16;"NG対応済"
    33;"決定"
    35;"リリース"
    36;"非有効"
    */

    /********* デフォルト値(変更不可) **********/
        -- SMS送信可否：可、空欄
    and (
        crBase.sms_console_snd_id = 1
        or crBase.sms_console_snd_id = 0
        or crBase.sms_console_snd_id is null
    )


        -- デリケートカスタマーフラグ：否
        and crBase.delicatecustomer_flg <> 1

        -- アプローチステータス:未対応、アプローチ中、MCR_アプローチ中、MCR_再アプローチ中、MCR_送客済、MCR_コンタクト済、
        -- 日程調整中、面談実施予定、面談済（電話）、面談済（来社）、面談済（WEB面談）、面談済（LINE、メール、SMS）、再求人待ち、進捗中、保留
        and crBase.cnslstatus_id in(
            1,4,6,30,31,32,34,37,38,39,40,41,42,43,44
        )
        /*
        1	未対応
        4	アプローチ中
        6	面談実施予定
        30	日程調整中
        31	面談済（電話）
        32	面談済（来社）
        34	保留
        37	MCR_アプローチ中
        38	MCR_再アプローチ中
        39	MCR_コンタクト済
        40	MCR_送客済
        41	進捗中
        42	再求人待ち
        43	面談済(WEB面談)
        44	面談済(LINE、メール、SMS)
        */

        -- 登録ステータス：活動中
        and crBase.regstatus_id = 2

        -- 登録ルート：マイナビマイナビコメディカル
        and crBase.media_id = 117
        /*
        mediaid	medianame
        117	マイナビコメディカル

        */

        -- 流入経路：コメディカル/紹介/空欄
        and (
            crBase.routeapply_id in(3,103,0)
            or crBase.routeapply_id is null
        )
        /*
        103	コメディカル
        3	紹介
        */

        -- サービス領域：コメディカル その他 空白
        and (
            crBase.active_service_field_id in(9,3,0)
            or crBase.active_service_field_id is null
        )
        /*
        稼働サービス領域
        9	その他
        1	看護師
        2	薬剤師
        3	コメディカル
        4	介護職
        5	保育士
        */

    and (
        (
            (
                crBase.telhome like '090%'
                or crBase.telhome like '080%'
                or crBase.telhome like '070%'
            )
            or
            (
                crBase.telcellular like '090%'
                or crBase.telcellular like '080%'
                or crBase.telcellular like '070%'
            )

        )
        and (
            crBase.telhome not like '%00000000%'
            or crBase.telhome not like '%11111111%'
            or crBase.telhome not like '%22222222%'
            or crBase.telhome not like '%33333333%'
            or crBase.telhome not like '%44444444%'
            or crBase.telhome not like '%55555555%'
            or crBase.telhome not like '%66666666%'
            or crBase.telhome not like '%77777777%'
            or crBase.telhome not like '%88888888%'
            or crBase.telhome not like '%99999999%'
        )

        and (
            crBase.telhome not like '%00000000%'
            or crBase.telhome not like '%11111111%'
            or crBase.telhome not like '%22222222%'
            or crBase.telhome not like '%33333333%'
            or crBase.telhome not like '%44444444%'
            or crBase.telhome not like '%55555555%'
            or crBase.telhome not like '%66666666%'
            or crBase.telhome not like '%77777777%'
            or crBase.telhome not like '%88888888%'
            or crBase.telhome not like '%99999999%'
            or crBase.telcellular is null
        )

        and (
            length(crBase.telhome) = 11
            or length(crBase.telcellular) = 11
        )

    )

)


SELECT
    case
        when length(crBase.telhomeNo) = 11 and crBase.telhomeNo is not null
            then enclosedoublequotation(concat(substring(crBase.telhomeNo,1,3),'-',substring(crBase.telhomeNo,4,4),'-',substring(crBase.telhomeNo,8,4)))
        when length(crBase.telhomeNo) <> 11 or crBase.telhomeNo is null and length(crBase.telcellularNo) = 11 and crBase.telcellularNo is not null
            then enclosedoublequotation(concat(substring(crBase.telcellularNo,1,3),'-',substring(crBase.telcellularNo,4,4),'-',substring(crBase.telcellularNo,8,4)))
        else null
    end                                                      "電話番号"
    ,crBase.career_id                                        "求職者番号"
    ,crFld.servicefieldname                                  "稼働サービス領域"
    ,Ca.username                                             "担当CA名"
    ,crMedia.medianame                                       "登録ルート"
    ,crPref.prefname                                         "在住地（都道府県）"
    ,crCity.cityname                                         "在住地（市区町村）"
    ,date_part('year',age(current_date,crBase.birth_date))   "年齢"
    ,crCnsl.cnslstatusname                                   "アプローチステータス"
    ,crReg.regstatusname                                     "登録ステータス"
    ,crQual.licensename                                      "資格情報"
    ,crDsrdWkng.dsrdwayofwkngname                            "希望する働き方"
    ,crMdClass.mediaclass1name                               "流入経路"
    ,crBase.prspct_for_hire_yr_mth                           "入社見込年月"
    ,actMain.nextaction_date                                 "NEXT実施日時"
    ,to_char(crBase.entry_date,'yyyy/mm/dd')                 "WEBエントリー日"
    ,to_char(crBase.latestcnsl_date,'yyyy/mm/dd')            "最新面談日"
    ,to_char(crBase.update_date,'yyyy/mm/dd')                "最終更新日"
    ,crSms.sms_console_snd_name                              "SMS送信可否"

FROM
    -- 求職者情報
    v_career crBase

    --稼働サービス領域
    left join "MNVM".mstservicefield crFld on crFld.servicefieldid = crBase.active_service_field_id

    -- 担当CA名
    left join "MNVM".mstuser Ca on Ca.userid = crBase.charge_id

    --登録ルート
	left join "MNVM".mstmedia crMedia on crMedia.mediaid = crBase.media_id

    -- 在住地（都道府県）
    left join "MNVM".mstpref crPref on crPref.prefid = crBase.pref_id

    -- 在住地（市区町村）
    left join "MNVM".mstcity crCity on crCity.cityid = crBase.city_id

    --登録ステータス（登録、アプローチ）
    left join "MNVM".mstregstatus crReg on crReg.regstatusid = crBase.regstatus_id

    --アプローチステータス
    left join "MNVM".mstcnslstatus crCnsl on crCnsl.cnslstatusid = crBase.cnslstatus_id

    --資格情報
	left join (
			select
				crQual.career_id as career_id,
				concat('/',string_agg(distinct crLicence.licenseid,'/'),'/') as licenseid,
				concat('/',string_agg(distinct crLicence.licensename,'/'),'/') as licensename
			from
				"MNVM".trnqual crQual
				left join "MNVM".mstlicense crLicence on crLicence.licenseid = crQual.license_id

			group by
				crQual.career_id
	) crQual on crQual.career_id = crBase.career_id

    --希望する働き方
    left join (
        select
            crWrkWy.career_id as career_id,
            concat('/',string_agg(cast(crDsrdWkng.dsrdwayofwkngid as varchar),'/'),'/') as dsrdwayofwkngid,
            concat('/',string_agg(crDsrdWkng.dsrdwayofwkngname,'/'),'/') as dsrdwayofwkngname
        from
            "MNVM".trncareer_workway crWrkWy
            left join "MNVM".mstdsrdwayofwkng crDsrdWkng on crDsrdWkng.dsrdwayofwkngid = crWrkWy.workway_id
        group by
            crWrkWy.career_id
    )crDsrdWkng on crDsrdWkng.career_id = crBase.career_id

     --流入経路
    left join "MNVM".mstmediaclass1 crMdClass on crMdClass.mediaclass1id = crBase.routeapply_id


    --ネクストアクション日
    left join (
        select
            actMain.career_id
            ,max(actMain.histseq) histseq
        from
            "MNVM".trncareer_action actMain
        where
            actMain.complete_date is null
            and actMain.nextaction_date is not null
        group by
            actMain.career_id
    ) tmpNext on tmpNext.career_id = crBase.career_id

    left join "MNVM".trncareer_action actMain on actMain.career_id = tmpNext.career_id and actMain.histseq = tmpNext.histseq

    -- SMS送信可否
    left join "MNVM".mstsms_console_snd crSms on crSms.sms_console_snd_id = crBase.sms_console_snd_id

WHERE
    --③資格：臨床検査技師、臨床工学技士、診療放射線技師、視能訓練士
     (
		strpos(crQual.licenseid,'/15003/') > 0
		or strpos(crQual.licenseid,'/15004/') > 0
		or strpos(crQual.licenseid,'/15007/') > 0
		or strpos(crQual.licenseid,'/15008/') > 0
	 )
    /*
    15003	臨床検査技師
    15004	臨床工学技士
    15007	診療放射線技師
    15008	視能訓練士
    */

limit 100