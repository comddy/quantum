from typing import List
import pickle

class FinancialData(object):
    def __init__(self,Number:int=4,ProjectName:List[str]=['股票A','债券B','期货C','信托D'],
                 profit_rate:List[float]=[0.08,0.05,0.10,0.06],risk_matrix:List[List[float]]=None,FileName=None) -> None:
        self.number = Number
        self.profit_rate =profit_rate
        self.filename = FileName
        self.project_name = ProjectName
        if risk_matrix is None:
            self.risk_matrix = [[0.04,0.01,0.06,0.025],[0.01,0.02,0.03,0.005],
                                [0.06,0.03,0.09,0.04],[0.025,0.005,0.04,0.09]]
        elif len(risk_matrix)!=self.number:
                raise ValueError(f'输入的风险协方差矩阵尺寸错误!')
        else:
            self.risk_matrix = risk_matrix
        self.restore()
        
    def restore(self):
        if self.filename is None:        
            with open('./data/PlanA.spear','wb') as f:
                pickle.dump(obj={'Number':self.number,'Project_Name':self.project_name,
                                 'Profit_rates':self.profit_rate,
                                'Risk_Matrix':self.risk_matrix},file=f)
        else:
            with open(f'./data/{self.filename}.spear','wb') as f:
                pickle.dump(obj={'Number':self.number,'Project_Name':self.project_name,
                                 'Profit_rates':self.profit_rate,
                                'Risk_Matrix':self.risk_matrix},file=f)
        print('成功保存数据!')