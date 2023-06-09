import random
import numpy as np
import matplotlib.pyplot as plt

# class CRAMCAlgorithm:

# 计算随机一年内发生违约的概率
def calculate_default_probability(p_0, rho, z):
    return p_0 * (1 + rho * z)


# 计算信用产品的违约损失
def calculate_loss_given_default(notional, p_0):
    return (1 - p_0) * notional


# 计算单个资产组合的VaR和CVaR
def calculate_var_cvar(num_simulations, p_0, rho, z_max, recovery_rate, notional):
    """
    计算单个资产组合的VaR和CVaR
    """
    losses = []
    defaults = 0
    for i in range(num_simulations):
        # 生成从区间[-z_max, z_max]中等概率采样的一个z值
        z = random.uniform(-z_max, z_max)
        # 如果债券违约，则增加defaults计数器
        if calculate_default_probability(p_0, rho, z) > random.uniform(0, 1):
            defaults += 1
            # 计算损失
            loss = calculate_loss_given_default(notional, p_0)
            losses.append(loss)
    # 计算违约风险
    default_risk = defaults / num_simulations
    # 计算VaR和CVaR
    expected_loss = sum(losses) / len(losses)
    var = np.percentile(losses, 95)
    cvar = np.mean([loss for loss in losses if loss >= var])
    
    return var, cvar, default_risk

# 计算所有资产组合的VaR和CVaR，并输出结果。
# 计算所有资产组合的VaR和CVaR，并输出结果。
def calculate_portfolio_var_cvar(portfolios, num_simulations, z_max):
    print("========== VaR and CVaR Calculation Results ==========")
    losses = []
    defaults = 0
    probabilities = []
    for i in range(len(portfolios)):
        # 计算该资产组合的VaR和CVaR
#         print(portfolio)
        portfolio = portfolios['assets'][i]
        p_0, rho, recovery_rate, notional = portfolio['p_0'], portfolio['rho'], portfolio['recovery_rate'], portfolio['notional']
        z = random.uniform(-z_max, z_max)
        for i in range(num_simulations):
            # 生成从区间[-z_max, z_max]中等概率采样的一个z值
            z = random.uniform(-z_max, z_max)
            # 如果债券违约，则增加defaults计数器
            if calculate_default_probability(p_0, rho, z) > random.uniform(0, 1):
                defaults += 1
                # 计算损失
                loss = calculate_loss_given_default(notional, p_0)
                losses.append(loss)
                probabilities += [prob]
        # 计算违约风险
        default_risk = defaults / num_simulations
        # 计算VaR和CVaR
        expected_loss = sum(losses) / len(losses)
        
        probabilities = np.array(probabilities)

        var, cvar, default_risk = calculate_var_cvar(num_simulations, p_0, rho, z_max, recovery_rate, notional)
        
        # 计算该资产组合的总价值
        total_value = sum([w * a['Value'] for w, a in zip(portfolios["allocations"], portfolios["assets"])])
        
        # 输出结果
        print(len(losses))
        pdf = np.zeros(len(losses))
        for i, v in enumerate(losses):
            pdf[i] += sum(probabilities[values == v])
        print('loss:', loss)
        print('default_risk:', default_risk)
        #expected_loss = sum(losses) / len(losses)
        #default_risk = defaults / num_simulations
    print('losses:', losses)
    print('pdf:', pdf)
    # print(f"Portfolio: {portfolios['name']}")
    # print(f"Total Value: {total_value:.2f}")
    # print(f"Default Risk: {default_risk:.2%}")
    # print(f"VaR(95%): {var:.2f}")
    # print(f"CVaR(95%): {cvar:.2f}")
    # print("====================================================")
    # # plot loss PDF, expected loss, var, and cvar
    # plt.bar(loss, default_risk)
    # plt.axvline(expected_loss, color="green", linestyle="--", label="E[L]")
    # plt.axvline(var, color="orange", linestyle="--", label="VaR(L)")
    # plt.axvline(cvar, color="red", linestyle="--", label="CVaR(L)")
    # plt.legend(fontsize=15)
    # plt.xlabel("Loss L ($)", size=15)
    # plt.ylabel("probability (%)", size=15)
    # plt.title("Loss Distribution", size=20)
    # plt.xticks(size=15)
    # plt.yticks(size=15)
    # plt.show()

if __name__ == '__main__':
    import random

    # 定义示例资产对象
    assets = []
    for index, row in risk_data.iterrows():
        assets.append({'Value':row['Value'],
                       'vol':random.uniform(0, 0.1),
                       'p_0':row['Pr(default)'],
                       'rho':row['Beta (Sensitivity to Credit Driver)'],
                       'recovery_rate':row['Expected Recovery Rate'],
                       'notional': row['Value']})
    print(len(assets))
    choosen = assets[:3]
    sum_value = 0
    for c in choosen:
        sum_value += c['Value']
    portfolios = {
        'name': 'A',
        'allocations': [round(i['Value']/sum_value, 6) for i in choosen],
        'assets': choosen
    }
    
    print(portfolios)
#         print(row['value'])
    # 定义多个资产组合
#     portfolios = [
#         {"name": "Portfolio A", "allocations": [0.3, 0.4, 0.3], "assets": [asset1, asset2, asset3]},
#         {"name": "Portfolio B", "allocations": [0.5, 0.2, 0.3], "assets": [asset1, asset4, asset5]},
#         # ... 添加更多资产组合
#     ]

    # 设置模型参数
    p_0 = risk_data['Pr(default)']
    rho = risk_data['Beta (Sensitivity to Credit Driver)']
    z_max = 10
    recovery_rate = risk_data['Expected Recovery Rate']
    notional = risk_data['Value']
    num_simulations = 10000

    # 计算所有资产组合的VaR和CVaR，并输出结果
    calculate_portfolio_var_cvar(portfolios, num_simulations, z_max)
