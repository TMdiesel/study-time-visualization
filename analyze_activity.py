# default package
import logging
from datetime import datetime,date
from datetime import timedelta
import typing as t

# third party package
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import jpholiday

# logger
logger=logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# graph setting
matplotlib.use('Agg')
sns.set()


class analyze_activitiy:
    def __init__(self,filepath:str,task_dict:t.Dict,savepath:str):
        self.filepath=filepath
        self.task_dict=task_dict
        self.savepath=savepath
        self.graph_num=3
        self.max_task_num=len(self.task_dict)

    def generate_df(self):
        self.df=pd.read_csv(self.filepath,header=None)
        self.df.columns=["date","task_num","start_time","end_time","memo"]
        self._convert()

    def _convert(self):
        def convertover24Hdatetime(str_datetime:str)->datetime:
            """
            str型のY/M/D,H:Mをdatetime型に変換
            H>=24以上でも可能
            """            
            date,time=str_datetime.split(",")
            year,month,day=[int(element) for element in date.split("/")]
            hour,minute=[int(element) for element in time.split(":")]
            if hour>=24:
                hour-=24
                converted_datetime=datetime(year,month,day,hour,minute)+timedelta(days=1)
            else:
                converted_datetime=datetime(year,month,day,hour,minute)
            return converted_datetime

        self.df["task_num"]=self.df["task_num"].map(lambda x: int(x))
        self.df['start_time'] = self.df['date']+","+self.df['start_time']
        self.df['end_time'] = self.df['date']+","+self.df['end_time']
        self.df["start_time"]=self.df["start_time"].map(convertover24Hdatetime)
        self.df["end_time"]=self.df["end_time"].map(convertover24Hdatetime)
        self.df["date"]=self.df["date"].map(lambda x: datetime.strptime(x, "%Y/%m/%d"))

        self.df["hour"]=self.df["end_time"]-self.df["start_time"]
        self.df["hour"]=self.df["hour"].map(lambda x: x.total_seconds()/3600)

    def activity_plot(self)->None:
        """
        - 各タスク番号の合計時間
        - 各日の勉強時間の時系列変化
        - 各日のタスクごとの勉強時間の時系列変化
        """
        fig,axes=plt.subplots(self.graph_num,figsize=(10,5*self.graph_num))
        min_date=self.df["date"].min()
        max_date=self.df["date"].max()
        str_min_date=min_date.strftime('%Y-%m-%d')
        str_max_date=max_date.strftime('%Y-%m-%d')
        task_num_gdf=self.df.groupby("task_num").sum()["hour"]
        task_num_gdf.index=task_num_gdf.index.map(lambda i:f"{i}:{self.task_dict[i]}")
        date_gdf=self.df.groupby("date").sum()[['hour']]
        gdf=self.df.groupby(["task_num","date"]).sum()[['hour']]

        def ComplementDate(s:pd.Series)->pd.DataFrame:
            """
            日付がindexのSeriesを入力して、
            欠けている日付をmin_dateからmax_dateの範囲で埋める
            """
            dates_df = pd.DataFrame(index=pd.date_range(str_min_date,str_max_date, freq='D'))
            return pd.DataFrame(s).merge(dates_df, how="outer", left_index=True, right_index=True).fillna(0)
        
        def create_biz_hol_index(start_date:datetime.date, end_date:datetime.date) -> pd.date_range:
            """
            平日と休日のindexを返す
            """
            year=start_date.year
            holiday=[]
            holiday_dict=jpholiday.year_holidays(year) 
            for i in range(len(holiday_dict)):         
                holiday.append(holiday_dict[i][0])
            holiday=holiday+[date(year,1,1),date(year,1,2),date(year,1,3),date(year,12,31)] 
            holiday=sorted(list(set(holiday)))  
            holiday=pd.to_datetime(holiday)

            calendar_full=pd.date_range(start_date, end_date,freq="D")
            business_index=[]
            holiday_index=[]
            for idx,calendar in enumerate(calendar_full):
                if (not calendar in holiday) and (calendar.weekday()>=0) and (calendar.weekday()<=4):
                    business_index.append(idx)
                else:
                    holiday_index.append(idx)

            return business_index,holiday_index

        axes[0].text(0,1.5,f"Study time report (from {str_min_date} to {str_max_date})",transform=axes[0].transAxes)
        axes[0].text(0,1.4,f"Summation: {task_num_gdf.sum():.2f}h" ,transform=axes[0].transAxes)
        axes[0].text(0,1.3,f"Mean: {task_num_gdf.sum()/((max_date+timedelta(days=1)-min_date).total_seconds()/86400):.2f}h" ,transform=axes[0].transAxes)
        axes[0].text(0,1.2,f"Latest day: {date_gdf.hour.iloc[-1]:.2f}h" ,transform=axes[0].transAxes)

        # graph 0
        axes[0].set_title(f"Study time for each task ")
        task_num_gdf.plot.bar(ax=axes[0])

        # graph 1
        axes[1].set_title(f"Time variation of study time ")
        business_index,holiday_index=create_biz_hol_index(min_date,max_date)
        ComplementDate(date_gdf).plot(marker='o',ax=axes[1],
                                markevery=business_index,legend=None)
        ComplementDate(date_gdf).plot(marker='o',ax=axes[1],
                                markevery=holiday_index,linestyle="None",color="red",legend=None)
        axes[1].set_ylim([0,date_gdf["hour"].max()+1])

        # graph 2
        axes[2].set_title(f"Time variation of study time for each task ")
        legend_list=[]
        for i in range(1,self.max_task_num+1):
            try:
                ComplementDate(gdf.loc[i,"hour"]).plot(marker='o',ax=axes[2])
                legend_list.append(f"{i}:{self.task_dict[i]}")
            except:
                pass
        axes[2].legend(legend_list,bbox_to_anchor=(0, -0.15),loc='upper left')

        plt.subplots_adjust(wspace=0.4, hspace=0.6)
        plt.savefig(self.savepath)
        plt.close(fig)
   
