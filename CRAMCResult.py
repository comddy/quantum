from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet
from PyQt5.QtGui import QPainter


class Draw(QDialog):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        series = QBarSeries()
        for i in range(3):
            slice = QBarSet(str(i))
            slice << 1 << 2 << 3
            series.append(slice)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Loss Distribution")
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)


        layout = QVBoxLayout()
        layout.addWidget(chart_view)

        self.setLayout(layout)
        self.resize(900,700)
    def resizeEvent(self, event) -> None:
        self.layout().setGeometry(self.rect())