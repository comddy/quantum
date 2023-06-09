import matplotlib.pyplot as plt
import numpy as np

from qiskit import Aer, QuantumCircuit
from qiskit.utils import QuantumInstance
from qiskit.algorithms import IterativeAmplitudeEstimation, EstimationProblem
from qiskit.circuit.library import LinearAmplitudeFunction
from qiskit_finance.circuit.library import LogNormalDistribution


# 设置存储标的资产到期日价格ST样本的量子比特数量为3，即，取2^3=8个样本
num_uncertainty_qubits = 3

# 基于BSM模型，计算ST需要的参数
S0 = 7.1271  # 标的资产期初价格
vol = 0.04893752407882 # 波动率
r = 0.020703023955912545  # 无风险收益率
T = 94 / 365  # 期权合约的期限，94天，以年为单位

# 根据数学公式，计算ST的数学期望和标准差
# 计算ST的对数正态分布的参数mu
mu = (r - 0.5 * vol**2) * T + np.log(S0)
# 计算ST的对数正态分布的参数sigma
sigma = vol * np.sqrt(T)
# 计算ST的数学期望
mean = np.exp(mu + sigma**2 / 2)
# 计算ST的方差
variance = (np.exp(sigma**2) - 1) * np.exp(2 * mu + sigma**2)
# 计算ST的标准差
stddev = np.sqrt(variance)

# 计算ST取样的区间的下限
low = np.maximum(0, mean - 3 * stddev)
# 计算ST取样的区间的上限
high = mean + 3 * stddev

# LogNormalDistribution会构建一个量子线路（就是一堆矩阵运算），它作用于3个初始状态（初始状态为100%概率测量为0）的量子比特，使其存储8个在指定区间均匀取得的对数正态分布的变量的样本，及对应概率
# 参数num_uncertainty_qubits为被施加运算的量子比特的数量
# 参数mu为构建的对数正态分布的第一个参数，参数sigma^2为对数正态分布的第二个参数，这两个参数用于根据数学公式计算样本对应的概率
# 参数(low, high)为样本取值的区间
uncertainty_model = LogNormalDistribution(
    num_uncertainty_qubits, mu=mu, sigma=sigma**2, bounds=(low, high)
)

# 绘制ST的分布情况
x = uncertainty_model.values
y = uncertainty_model.probabilities
plt.bar(x, y, width=0.1)
plt.xticks(x, size=15, rotation=90)
plt.yticks(size=15)
plt.grid()
plt.xlabel("ST", size=15)
plt.ylabel("Probability", size=15)
plt.show()

# 设置期权的执行价格，因为它需要在ST的取样区间内对验证才有意义，所以到这里再设置，实际情况执行价格肯定是预先确定的
strike_price = 6.8
# 绘制用ST计算payoff的分段线性函数
x = uncertainty_model.values
y = np.maximum(0, x - strike_price)
plt.plot(x, y, "ro-")
plt.grid()
plt.title("Payoff Function", size=15)
plt.xlabel("ST", size=15)
plt.ylabel("Payoff", size=15)
plt.xticks(x, size=15, rotation=90)
plt.yticks(size=15)
plt.show()

