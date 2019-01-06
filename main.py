import dbquery
import InterfaceSale
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

def Task():
    CurTime = datetime.datetime.now()
    CurTimeFormat = CurTime.strftime("%Y-%m-%d")
    TorTimeFormat = (CurTime + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    UpdateData = dbquery.Get_SaleForecast(CurTimeFormat + ' 12:00:00', TorTimeFormat + ' 1:00:00')
    PredictUpdate = dict()

    for i in UpdateData:
        PredictUpdate[i[0]] = i[1]

    InterfaceSale.Post_Wms(PredictUpdate,CurTimeFormat + ' 23:59:59.000')        #推送接口

if __name__ == '__main__':
    # 初始化调度器
    Scheduler = BlockingScheduler()

    # 添加任务作业，args()中最后一个参数后面要有一个逗号，本任务设置在每天凌晨1:00:00执行
    Scheduler.add_job(Task, 'cron', hour='8', minute='0', second='0', )

    # 启动调度器，到点task就会被执行啦
    Scheduler.start()
