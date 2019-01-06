user_name = 'ALG'
server_ip = '10.42.10.202'
password = 'nPrhkBK*7'
db_name = 'alog-wms'

queryoccupy = "select BD.ProductCode,sum(BD.Qty) as Qty from V_t_OutOrder O "
queryoccupy += "left join V_t_Boxing B on O.OutOrderNo = B.OutOrderNo "
queryoccupy += "left join V_t_BoxingDetail BD on B.BoxingNo = BD.BoxingNo "
queryoccupy += "where O.PlanOutTime >= {} and O.PlanOutTime <= {} and B.StorageCode = 'ALOG-0003-03' group by BD.ProductCode"

