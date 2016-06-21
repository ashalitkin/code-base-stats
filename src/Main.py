from org.ashalitkin.cbstat.cbData import CBMerger
from org.ashalitkin.cbstat.cbAnalyzer import CBAnalyzer

metricsFile = "..\out\\metrics.csv"
merger = CBMerger("..\data\\coupling.txt", "..\data\\ComplexityReport.txt", metricsFile)
merger.merge_metrics()

analyzer = CBAnalyzer(metricsFile)
analyzer.ca_hist()
analyzer.complexity_hist()
analyzer.orig_scatter_plot()
analyzer.inverted_scatter_plot()
analyzer.save_res_to_csv("..\\out\\res1.csv")

