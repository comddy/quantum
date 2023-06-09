import matplotlib.pyplot as plt
import numpy as np

from qiskit import Aer, QuantumCircuit
from qiskit.utils import QuantumInstance
from qiskit.algorithms import IterativeAmplitudeEstimation, EstimationProblem
from qiskit.circuit.library import LinearAmplitudeFunction
from qiskit_finance.circuit.library import LogNormalDistribution
from qiskit_finance.applications.estimation import EuropeanCallPricing
from qiskit_finance.applications.estimation import EuropeanCallDelta
import random

class FutureAlgorithm:
    def __init__(self, S0, T, r, vol):
        # 设置存储标的资产到期日价格ST样本的量子比特数量为3，即，取2^3=8个样本
        self.num_uncertainty_qubits = 3

        # 基于BSM模型，计算ST需要的参数
        # S0 = 7.1271  # 标的资产期初价格
        # vol = 0.04893752407882 # 波动率
        # r = 0.020703023955912545  # 无风险收益率
        # T = 94 / 365  # 期权合约的期限，94天，以年为单位

        # 根据数学公式，计算ST的数学期望和标准差
        # 计算ST的对数正态分布的参数mu
        self.mu = (r - 0.5 * vol**2) * T + np.log(S0)
        # 计算ST的对数正态分布的参数sigma
        self.sigma = vol * np.sqrt(T)
        # 计算ST的数学期望
        mean = np.exp(self.mu + self.sigma**2 / 2)
        # 计算ST的方差
        variance = (np.exp(self.sigma**2) - 1) * np.exp(2 * self.mu + self.sigma**2)
        # 计算ST的标准差
        stddev = np.sqrt(variance)

        # 计算ST取样的区间的下限
        self.low = np.maximum(0, mean - 3 * stddev)
        # 计算ST取样的区间的上限
        self.high = mean + 3 * stddev
        

        # 绘制这个新的量子线路
        # european_call.draw()



    def run(self):
        # 设置期权的执行价格，因为它需要在ST的取样区间内对验证才有意义，所以到这里再设置，实际情况执行价格肯定是预先确定的
        strike_price = random.uniform(self.low, self.high)

        uncertainty_model = LogNormalDistribution(
            3, mu=self.mu, sigma=self.sigma**2, bounds=(self.low, self.high)
        )

        # LogNormalDistribution会构建一个量子线路（就是一堆矩阵运算），它作用于3个初始状态（初始状态为100%概率测量为0）的量子比特，使其存储8个在指定区间均匀取得的对数正态分布的变量的样本，及对应概率
        # 参数num_uncertainty_qubits为被施加运算的量子比特的数量
        # 参数mu为构建的对数正态分布的第一个参数，参数sigma^2为对数正态分布的第二个参数，这两个参数用于根据数学公式计算样本对应的概率
        # 参数(low, high)为样本取值的区间
        # 绘制用ST计算payoff的分段线性函数
        x = uncertainty_model.values
        y = np.maximum(0, x - strike_price)
        exact_value = np.dot(uncertainty_model.probabilities, y) # 计算payoff的数学期望，即将每个值与对应概率相乘后，求和
        exact_delta = sum(uncertainty_model.probabilities[x >= strike_price]) # 计算delta风险参数，按它就是标志资产到期日价格大于执行价格的概率之和计算
        # 设置计算payoff的分段线性函数对应的量子线路需要的估算精度
        c_approx = 0.25

        # 创建计算payoff的分段线性函数的量子线路
        breakpoints = [self.low, strike_price] # 分段函数自变量的第一段，标的资产到期日价格小于执行价格时，payoff永远为0
        # breakpoints = sorted(set([round(i, 4) for i in breakpoints]), reverse=False)
        # print(breakpoints, (self.low, self.high))
        slopes = [0, 1] # 分段线性函数的各段斜率，第一段是0，第二段是1，第二段是1跟量子线路的具体实现有关，在第二段自变量和因变量是一一对应的
        offsets = [0, 0] # 分段线性函数的各段位移，两段都是0，第二段是0跟量子线路的具体实现有关，在第二段自变量和因变量是一一对应的
        f_min = 0 # 分段线性函数的因变量的取值下限
        f_max = self.high - strike_price # 分段线性函数的因变量的取值上限，标的资产到期日价格大于执行价格时，payoff最大就是标的资产到期日价格与执行价格的差
        # LinearAmplitudeFunction会根据输入的参数构建出量子线路，这个量子线路需要的量子比特包括存储样本的量子比特，但还需要增加辅助的量子比特
        european_call_objective = LinearAmplitudeFunction(
            self.num_uncertainty_qubits,
            slopes,
            offsets,
            domain=(self.low, self.high),
            image=(f_min, f_max),
            breakpoints=breakpoints,
            rescaling_factor=c_approx,
        )

        # 结合初始化样本的量子线路和计算payoff的量子线路，构建一个量子线路，就是把着两堆矩阵运算放一起连续算，这个新的量子线路就是振幅估计算法的初始化线路
        # 新的量子线路的量子比特数跟payoff计算量子线路的比特数量相等，为7
        num_qubits = european_call_objective.num_qubits
        european_call = QuantumCircuit(num_qubits)
        european_call.append(uncertainty_model, range(self.num_uncertainty_qubits))
        european_call.append(european_call_objective, range(num_qubits))
        # 创建一个量子虚拟机实例（在传统计算机里模拟），用于基于运行上面构建的量子线路的振幅估计算法
        qi = QuantumInstance(Aer.get_backend("aer_simulator"), shots=100)
        # 创建一个振幅估计问题
        # 参数state_preparation为振幅估计的状态初始化量子线路，即前文构建的量子线路，包含ST采样和payoff计算
        # 参数objective_qubits标识振幅估计进行测量的目标比特列表，即上面7个量子比特里的q_3
        # 参数post_processing指定测出振幅后的操作，它使用的LinearAmplitudeFunction的post_processing，这个操作会将估计出的振幅映射回原来的payoff值
        problem = EstimationProblem(
            state_preparation=european_call,
            objective_qubits=[3],
            post_processing=european_call_objective.post_processing,
        )
        # 设置振幅估计需要的精度参数
        epsilon = 0.01
        alpha = 0.05
        # 构建一个振幅估计IterativeAmplitudeEstimation（还有其他种类的振幅估计器，不同种类的实现逻辑和算法复杂度不同）
        ae = IterativeAmplitudeEstimation(epsilon, alpha=alpha, quantum_instance=qi)
        # 启动振幅估计器，即重复执行量子线路并进行测量
        result = ae.estimate(problem)
        # 从结果中取出期权定价的在95%（1-alpha）概率下的置信区间
        old_conf_int = np.array(result.confidence_interval_processed)
        old_result = result.estimation_processed

        # 以上量子线路构建过程仅为展示算法逻辑，其实Qiskit中内置了无收益标的资产的欧式看涨期权的定价和风险参数的实现，直接调用如下即可：

        # 参数num_state_qubits是存储样本用的量子比特数
        # 参数strike_price是执行价格
        # 参数rescaling_factor是payoff计算分段线性函数线路的估算精度
        # 参数bounds是ST的取样区间
        # 参数uncertainty_model是ST的取样量子线路
        european_call_pricing = EuropeanCallPricing(
            num_state_qubits=self.num_uncertainty_qubits,
            strike_price=strike_price,
            rescaling_factor=c_approx,
            bounds=(self.low, self.high),
            uncertainty_model=uncertainty_model,
        )
        # 设置振幅估计需要的精度参数
        epsilon = 0.01
        alpha = 0.05
        # 创建一个量子虚拟机实例（在传统计算机里模拟）
        qi = QuantumInstance(Aer.get_backend("aer_simulator"), shots=100)
        # 从内置的欧式看涨期权的定价实现中取出需要振幅估计的问题
        problem = european_call_pricing.to_estimation_problem()
        # 构建一个振幅估计IterativeAmplitudeEstimation
        ae = IterativeAmplitudeEstimation(epsilon, alpha=alpha, quantum_instance=qi)
        # 启动振幅估计器，即重复执行量子线路并进行测量
        result = ae.estimate(problem)
        # 从结果中取出期权定价在95%（1-alpha）概率下的置信区间
        conf_int = np.array(result.confidence_interval_processed)






        # 对于delta风险参数，使用Qiskit内置的delta计算函数量子线路

        # 参数num_state_qubits是存储样本用的量子比特数
        # 参数strike_price是执行价格
        # 参数bounds是ST的取样区间
        # 参数uncertainty_model是ST的取样量子线路
        european_call_delta = EuropeanCallDelta(
            num_state_qubits=self.num_uncertainty_qubits,
            strike_price=strike_price,
            bounds=(self.low, self.high),
            uncertainty_model=uncertainty_model,
        )

        # 设置振幅估计需要的精度参数
        epsilon = 0.01
        alpha = 0.05

        # 创建一个量子虚拟机实例（在传统计算机里模拟）
        qi = QuantumInstance(Aer.get_backend("aer_simulator"), shots=100)
        # 从内置的欧式看涨期权的定价实现中取出需要振幅估计的问题
        problem = european_call_delta.to_estimation_problem()

        # 构建一个振幅估计IterativeAmplitudeEstimation
        ae_delta = IterativeAmplitudeEstimation(epsilon, alpha=alpha, quantum_instance=qi)
        # 启动振幅估计器，即重复执行量子线路并进行测量
        result_delta = ae_delta.estimate(problem)
        # 从结果中取出期权delta风险参数在95%（1-alpha）概率下的置信区间
        conf_int = np.array(result_delta.confidence_interval_processed)
        
        return [old_result, european_call_pricing.interpret(result), exact_delta, european_call_delta.interpret(result_delta)]



