from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class PieChartDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)

        series = QPieSeries()
        for label, value in data.items():
            series.append(str(label), float(value.strip('%')))


        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Pie Chart")


        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # self.setLayout(chart_view)


class ResultGraph(QWidget):
    def __init__(self, data):
        super().__init__()

        self.setWindowTitle("计算结果")
        self.data = data
        # 显示位置
        self.setGeometry(100, 100, 800, 600)
        self.create_piechart()

    def create_piechart(self):
        # 创建QPieSeries对象，它用来存放饼图的数据
        series = QPieSeries()

        # append方法中的数字，代表的是权重，完成可以改成其它，如80,70,60等等
        x_values = []
        y = []
        y_values = []

        for k,v in self.data.items():
            x_values.append(k)
            y.append(v.strip("%"))        # 将%加进去会影响计算结果，所以要转换成整数形式
        for n in y:
            y_values.append(float(n))
        for value in range(0, len(x_values)):
            series.append(str(x_values[value])+f"-{y_values[value]}%", y_values[value])

        slice = QPieSlice()

        # 单独处理某个扇区
        slice = QPieSlice()
        for i in range(0, len(x_values)):
            # 这里要处理的是python项，是依据前面append的顺序，如果是处理C++项的话，那索引就是3
            slice = series.slices()[i]

            # 突出显示，设置颜色
            # slice.setExploded(True) #如果需要各扇区分开可取消该行注释
            slice.setLabelVisible(True)
            #slice.setPen(QPen(Qt.red, 2)) #指定扇区边缘的颜色,注释则自动生成
            # slice.setBrush(Qt.red) #指定扇区的颜色,注释则自动生成

        # 创建QChart实例，它是PyQt5中的类
        chart = QChart()
        # QLegend类是显示图表的图例，先隐藏掉
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()

        # 设置动画效果
        chart.setAnimationOptions(QChart.SeriesAnimations)

        # 设置标题
        chart.setTitle("投资比例")

        chart.legend().setVisible(True)

        # 对齐方式
        chart.legend().setAlignment(Qt.AlignBottom)

        # 创建ChartView，它是显示图表的控件
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)


class Example(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        

        series = QPieSeries()


        for label, value in data.items():
            slice = QPieSlice()
            slice.setValue(float(value.strip('%')))
            slice.setLabel(f"{label}: {value}")
            slice.setLabelVisible(True)
            series.append(slice)




        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("饼图")


        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        layout = QVBoxLayout()
        layout.addWidget(chart_view)

        self.setLayout(layout)
        self.resize(900,700)
    def resizeEvent(self, event) -> None:
        self.layout().setGeometry(self.rect())