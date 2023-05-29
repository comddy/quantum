"""
注意:由于先前尝试复现杨沫同学提到的那篇文章中的算法后 效果不佳 结果表意不明
因此 在此重开PlanB 此方法并没有论文参考 
是基于我自己做的QUBO结合SamplerVQE制作的 经过测试效果相较之前好许多
以下是PlanB的实现
保持以下注释不要删除 qiskit框架的版权申明

杨建飞 0528
"""

# This code is part of Qiskit.
#
# (C) Copyright IBM 2018, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.


from qiskit.algorithms.minimum_eigensolvers import NumPyMinimumEigensolver, QAOA, SamplingVQE
from qiskit.algorithms.optimizers import COBYLA
from qiskit.circuit.library import TwoLocal
from qiskit.result import QuasiDistribution
from qiskit_aer.primitives import Sampler
# from qiskit_finance.applications.optimization import PortfolioOptimization
from qiskit_optimization.algorithms import MinimumEigenOptimizer
import numpy as np
import matplotlib.pyplot as plt
import datetime


from typing import List, Tuple, Union, Optional

import numpy as np
from docplex.mp.advmodel import AdvModel

from qiskit_optimization.algorithms import OptimizationResult
from qiskit_optimization.applications import OptimizationApplication
from qiskit_optimization.problems import QuadraticProgram
from qiskit_optimization.translators import from_docplex_mp
from qiskit_finance.exceptions import QiskitFinanceError
from qiskit.utils import algorithm_globals




class QuantumFinance(object):
    def __init__(self,return_rate:List,risk_matrix:np.array,
                 num_assets:int=4,global_seed:int=123,risk_factor:float=0.5,
                 g:int=2) -> None:
        """
        变量说明:
        return_rate -> 资产的预期回报率 维度为1*N
        risk_matrix -> 资产的风险协方差矩阵 N*N
        num_assets  -> 资产数目N 务必保持一致
        global_seed -> 随机数种子
        risk_factor -> 对风险的重视度 取值[0,1]建议0.5拉倒
        g           -> 资产分片数 和之前命名相同
        """
        self._return_rate = return_rate
        self._risk_matrix = risk_matrix
        self._num_assets  = num_assets
        self._global_seed = global_seed
        self._risk_factor = risk_factor
        self._g = g
        self.check_all_input()
        
        self.portfolio = PortfolioOptimization(
            expected_returns=self._return_rate, covariances=self._risk_matrix,
            risk_factor=self._risk_factor, budget=self._g)
        self.quadratic_program = self.portfolio.to_quadratic_program()
        print('初始化成功!')
        
        # 传统: QUBO-> Ising Hamiltonian-> 量子绝热演化的Ansatz 参数分层训练->优化参数 ->测量:选出最多出现的那个态
        # 创新: QUBO-> Ising Hamiltonian-> 硬件高效型Ansatz + SamplerVQE ->优化参数 ->测量:选出最多出现的那个态
        
        
    def solve(self):
        algorithm_globals.random_seed = 1234
        self._optimizer = COBYLA()
        self._optimizer.set_options(maxiter=500)
        ry = TwoLocal(self._num_assets, "ry", "cz", reps=3, entanglement="full")
        vqe_mes = SamplingVQE(sampler=Sampler(), ansatz=ry, optimizer=self._optimizer)
        vqe = MinimumEigenOptimizer(vqe_mes)
        self.ansatz = vqe_mes.ansatz
        result = vqe.solve(self.quadratic_program)
        self.print_result(result)
        self.result = result
        
        
    def check_all_input(self):
        #此函数用来检验所有输入是否靠谱
        if len(self._return_rate) != self._num_assets or self._risk_matrix.shape != (self._num_assets,self._num_assets):
            raise ValueError('资产预期回报率 以及 风险协方差矩阵维度错误!')
        if self._num_assets<0:
            raise ValueError('资产个数不得设置为负数')
        elif self._num_assets>=9:
            raise ValueError('为了计算性能,请勿设置过大的资产个数!建议不大于8')
        if self._g<0 or self._g>=self._num_assets:
            raise ValueError(f'资产分片数错误!不得为负数或大于等于资产个数{self._num_assets}')
        if self._risk_factor>=1 or self._risk_factor<=0:
            raise ValueError(f'risk factor设定错误 应当处于(0,1)')
        
        
    def print_result(self,result):
        selection = result.x
        value = result.fval
        self.result_dict = {}
        print(f"最优投资选择:{selection}, value {value}")
        print(f'-----------结果解读-----------\n共有{self._num_assets}种理财产品,均衡地选择其中的{self._g}个')
        for index,i in enumerate(selection):
            if int(i)==1:
                self.result_dict[f'理财产品{index+1}'] = f'{1/self._g*100}%'
                print(f'第{index+1}个理财产品,投资比例{1/self._g*100}%')
            else:
                self.result_dict[f'理财产品{index+1}'] = '0%'
                print(f'第{index+1}个理财产品,不投资')
                
        

class PortfolioOptimization(OptimizationApplication):
    def __init__(
        self,
        expected_returns: np.ndarray,
        covariances: np.ndarray,
        risk_factor: float,
        budget: int,
        bounds: Optional[List[Tuple[int, int]]] = None,
    ) -> None:

        self._expected_returns = expected_returns
        self._covariances = covariances
        self._risk_factor = risk_factor
        self._budget = budget
        self._bounds = bounds
        self._check_compatibility(bounds)

    def to_quadratic_program(self) -> QuadraticProgram:
        self._check_compatibility(self._bounds)
        num_assets = len(self._expected_returns)
        mdl = AdvModel(name="Portfolio optimization")
        if self.bounds:
            x = [
                mdl.integer_var(lb=self.bounds[i][0], ub=self.bounds[i][1], name=f"x_{i}")
                for i in range(num_assets)
            ]
        else:
            x = [mdl.binary_var(name=f"x_{i}") for i in range(num_assets)]
        quad = mdl.quad_matrix_sum(self._covariances, x)
        linear = np.dot(self._expected_returns, x)
        mdl.minimize(self._risk_factor * quad - linear)
        mdl.add_constraint(mdl.sum(x[i] for i in range(num_assets)) == self._budget)
        op = from_docplex_mp(mdl)
        return op

    def portfolio_expected_value(self, result: Union[OptimizationResult, np.ndarray]) -> float:
        x = self._result_to_x(result)
        return np.dot(self._expected_returns, x)

    def portfolio_variance(self, result: Union[OptimizationResult, np.ndarray]) -> float:
        x = self._result_to_x(result)
        return np.dot(x, np.dot(self._covariances, x))

    def interpret(self, result: Union[OptimizationResult, np.ndarray]) -> List[int]:
        x = self._result_to_x(result)
        return [i for i, x_i in enumerate(x) if x_i]

    def _check_compatibility(self, bounds) -> None:
        if len(self._expected_returns) != len(self._covariances) or not all(
            len(self._expected_returns) == len(row) for row in self._covariances
        ):
            raise QiskitFinanceError(
                "The sizes of expected_returns and covariances do not match. ",
                f"expected_returns: {self._expected_returns}, covariances: {self._covariances}.",
            )
        if bounds is not None:
            if (
                not isinstance(bounds, list)
                or not all(isinstance(lb_, int) for lb_, _ in bounds)
                or not all(isinstance(ub_, int) for _, ub_ in bounds)
            ):
                raise QiskitFinanceError(
                    f"The bounds must be a list of tuples of integers. {bounds}",
                )
            if any(ub_ < lb_ for lb_, ub_ in bounds):
                raise QiskitFinanceError(
                    "The upper bound of each variable, in the list of bounds, must be greater ",
                    f"than or equal to the lower bound. {bounds}",
                )
            if len(bounds) != len(self._expected_returns):
                raise QiskitFinanceError(
                    f"The lengths of the bounds, {len(self._bounds)}, do not match to ",
                    f"the number of types of assets, {len(self._expected_returns)}.",
                )

    @property
    def expected_returns(self) -> np.ndarray:
        return self._expected_returns

    @expected_returns.setter
    def expected_returns(self, expected_returns: np.ndarray) -> None:
        self._expected_returns = expected_returns

    @property
    def covariances(self) -> np.ndarray:
        return self._covariances

    @covariances.setter
    def covariances(self, covariances: np.ndarray) -> None:
        self._covariances = covariances

    @property
    def risk_factor(self) -> float:
        return self._risk_factor

    @risk_factor.setter
    def risk_factor(self, risk_factor: float) -> None:
        self._risk_factor = risk_factor

    @property
    def budget(self) -> int:
        return self._budget

    @budget.setter
    def budget(self, budget: int) -> None:
        self._budget = budget

    @property
    def bounds(self) -> List[Tuple[int, int]]:
        return self._bounds

    @bounds.setter
    def bounds(self, bounds: List[Tuple[int, int]]) -> None:
        self._check_compatibility(bounds)  # check compatibility before setting bounds
        self._bounds = bounds
