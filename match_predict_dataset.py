import logging
from typing import List, Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame
from pympler.asizeof import asizeof
from sqlalchemy.dialects.mssql.information_schema import columns

from src.match.db.models.match_record_final_step_start import MatchRecordFinalStepStart
from src.match.db.session import SessionLocal

db=SessionLocal()

class CustomDataLoader:
    """
    自定义数据加载器，用于从数据库加载MatchRecordFinalStepStart数据
    """

    def __init__(self, db:SessionLocal):
        """
        初始化数据加载器

        Args:
            database_url: 数据库连接URL
        """
        self.session = db;

    def load_data(self,limit:int=None) -> List[MatchRecordFinalStepStart]:
        """
        获取所有的MatchRecordFinalStepStart数据

        Returns:
            List[MatchRecordFinalStepStart]: 所有比赛记录数据
        """
        session = self.session
        try:
            # 查询所有MatchRecordFinalStepStart记录
            all_records = session.query(MatchRecordFinalStepStart);
            if limit:
                all_records = all_records.limit(limit)
            all_records=all_records.all()
            return all_records
        finally:
            session.close()

    def load_data_as_dataframe(self,limit:int=None) -> DataFrame:
        """
        获取所有数据并转换为pandas DataFrame格式

        Returns:
            pd.DataFrame: 包含所有比赛记录的DataFrame
        """
        data_list:List[MatchRecordFinalStepStart]=self.load_data(limit)
        df=pd.DataFrame([record.__dict__ for record in data_list])

        # 选择数值型特征列（这里仅示例部分特征）
        all_columns = [
            'match_id', 'proprity', 'is_home', 'start_pk', 'my_recent_count', 'my_avg_goals', 'my_avg_loose_goals',
            'my_win_rate', 'my_rq_rate',
            'my_bei_rq_rate', 'my_tech_avg_short_all', 'my_tech_avg_short_score', 'my_tech_avg_bei_short_all',
            'my_tech_avg_bei_short_score',
            'other_recent_count', 'other_avg_goals', 'other_win_rate', 'other_rq_rate', 'other_bei_rq_rate',
            'other_tech_avg_short_all',
            'other_tech_avg_short_score', 'other_tech_avg_bei_short_all', 'other_tech_avg_bei_short_score','final_result']

        # 移除空值并提取特征
        df_clean = df.dropna()
        df_clean=df_clean[all_columns]
        # match_id 相同的，随机取一条
        df_clean = df_clean.groupby('match_id', group_keys=False).sample(n=1)
        df_clean=df_clean.drop("match_id",axis=1)

        return df_clean
    def get_features_and_labels(self, limit:int=None) -> Tuple[np.ndarray, np.ndarray]:
        """
        提取特征和标签用于神经网络训练

        Returns:
            Tuple[np.ndarray, np.ndarray]: 特征矩阵和标签向量
        """
        df = self.load_data_as_dataframe(limit)

        # 标签向量（将结果转换为分类标签）
        y = df[['final_result']]
        X = df.drop(columns=['final_result'])

        return X, y

if __name__ == '__main__':
   """
   预测比赛结果
   1.加载比赛
   """
   logger = logging.getLogger(__name__)
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )
   loader = CustomDataLoader(db)
   # df=loader.load_data_as_dataframe(10000)
   # df.to_csv("所有step_start1.csv")
   X,y=loader.get_features_and_labels()
   print(X.shape,y.shape)
   train_size=int(0.83*X.shape[0])
   print(train_size)
   X_train=X[0:train_size]
   X_test=X[train_size:]
   y_train=y[:train_size]
   y_test=y[train_size:]




