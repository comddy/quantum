import torch
from torch import nn
from torch.optim import Adam
import numpy as np
import csv

class Discriminator(nn.Module):
    def __init__(self, input_size):
        super(Discriminator, self).__init__()

        self.linear_input = nn.Linear(input_size, 20)  # 输入层到隐藏层的线性变换
        self.leaky_relu = nn.LeakyReLU(0.2)  # 使用LeakyReLU激活函数
        self.linear20 = nn.Linear(20, 1)  # 隐藏层到输出层的线性变换
        self.sigmoid = nn.Sigmoid()  # 使用Sigmoid激活函数

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        x = self.linear_input(input)  # 输入层到隐藏层的线性变换
        x = self.leaky_relu(x)  # 使用LeakyReLU激活函数
        x = self.linear20(x)  # 隐藏层到输出层的线性变换
        x = self.sigmoid(x)  # 使用Sigmoid激活函数
        return x

def anomaly_detection(threshold=0.3):
    base_path = 'core/AbnomalDetcationCode/'
    # 创建判别器实例
    input_size = 2  # 或者根据实际输入数据的大小设置
    discriminator = Discriminator(input_size)

    # 加载保存的参数
    discriminator.load_state_dict(torch.load(base_path+'discriminator.pth'))

    # 设置模型为评估模式
    discriminator.eval()

    # 生成随机数据
    n = 2  # 根据需要调整
    normal_data = np.random.normal(size=(10000, n))
    uniform_data = np.random.uniform(size=(2000, n))

    # 转换数据为PyTorch张量
    normal_data_torch = torch.from_numpy(normal_data).float()
    uniform_data_torch = torch.from_numpy(uniform_data).float()

    # 使用判别器进行预测
    normal_predictions = discriminator(normal_data_torch)
    uniform_predictions = discriminator(uniform_data_torch)

    # 将预测转换为NumPy数组
    normal_predictions_np = normal_predictions.detach().numpy()
    uniform_predictions_np = uniform_predictions.detach().numpy()

    # 创建索引
    normal_indices = np.arange(normal_data.shape[0])
    uniform_indices = np.arange(uniform_data.shape[0]) + normal_data.shape[0]

    # 合并索引和数据
    normal_data_with_indices = np.hstack([normal_indices.reshape(-1, 1).astype(int), normal_data, normal_predictions_np.reshape(-1, 1)])
    uniform_data_with_indices = np.hstack([uniform_indices.reshape(-1, 1).astype(int), uniform_data, uniform_predictions_np.reshape(-1, 1)])

    # 合并正态数据和均匀数据
    total_data = np.vstack([normal_data_with_indices, uniform_data_with_indices])
   
    # 写入所有的数据到CSV文件 
    with open(base_path+'classified_data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['序号'] + ['特征' + str(i+1) for i in range(n)] + ['判别器预测'])
        for row in total_data:
            # 将索引转换为整数后写入
            writer.writerow(row)
        
        
    # 将不符合阈值的数据写入新的CSV文件
    with open(base_path+'out_of_threshold_data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['序号'] + ['特征' + str(i+1) for i in range(n)] + ['判别器预测'])
        
        # 打印并写入不符合阈值的数据
        for row in total_data:
            index = int(row[0])
            features = row[1:-1]
            prediction = row[-1]
            
            if prediction < threshold:
                # print(f"序号: {index}, 特征: {features}, 判别器预测: {prediction}")
                writer.writerow([index] + list(features) + [prediction])
