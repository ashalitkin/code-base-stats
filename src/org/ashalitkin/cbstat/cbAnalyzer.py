import pandas
import math
import seaborn as sns
import matplotlib.pyplot as plt


class CBAnalyzer:
    def __init__(self, input_file_name):
        # read, init min and max
        self.input_file_name = input_file_name
        self.metrics = pandas.read_csv(input_file_name)
        self.max_complexity = self.metrics["Complexity"].max()
        self.max_CA = self.metrics["CA"].max()
        self.min_complexity = self.metrics["Complexity"].min()
        self.min_CA = self.metrics["CA"].min()

        # add new metrics
        self._add_new_metrics()

        self.p_metrics = self.metrics.sort_values(["CP_Criteria"], ascending=False)

    def _add_new_metrics(self):
        self.metrics["NormComplexity"] = (self.min_complexity + 1) / (self.metrics["Complexity"] + 1) * 100
        self.metrics["NormCA"] = (self.min_CA + 1) / (self.metrics["CA"] + 1) * 100
        self.metrics["CP_Criteria"] = 100 - ((self.metrics["NormComplexity"] * self.metrics["NormComplexity"] + \
                                 self.metrics["NormCA"] * self.metrics["NormCA"]).map(math.sqrt) / math.sqrt(2))

    def orig_scatter_plot(self):
        plt.scatter(self.metrics["CA"], self.metrics["Complexity"])
        plt.xlabel("Coupling")
        plt.xticks(range(0, self.max_CA, self.max_CA // 30))
        plt.ylabel("Complexity")
        plt.show()

    def ca_hist(self):
        plt.hist(self.p_metrics["CA"], bins=range(0, 100))
        plt.title("CA Histogram")
        plt.xticks(range(0, 100, 2))
        plt.show()

    def complexity_hist(self):
        plt.hist(self.metrics["Complexity"], bins=range(0, 200), label="CA")
        plt.title("Cyclomatic Complexity Histogram")
        plt.xticks(range(0, 200, 4))
        plt.show()

    def save_res_to_csv(self, file_name):
        self.p_metrics[(self.metrics["CA"] > 1) & (self.p_metrics["Complexity"] > 10)].to_csv(file_name, index=False, \
                                                                         columns=["ClassName", "COB", "CA",
                                                                                  "Complexity", "NormCA",
                                                                                  "NormComplexity", "CP_Criteria"], \
                                                                         header=["Class name", "COB", "CA",
                                                                                 "Complexity",
                                                                                 "CA (Normalized and inverted)", \
                                                                                 "Complexity (Normalized and inverted)",
                                                                                 "Unit Test rating"])

    def inverted_scatter_plot(self):
        plt.scatter(self.metrics["NormCA"], self.metrics["NormComplexity"])
        plt.xlabel("Coupling (normalized and inverted)")
        plt.ylabel("Complexity (normalized and inverted)")
        plt.xticks(range(0, 100, 2))
        plt.show()


class CBAnalyzerWithoutInvert(CBAnalyzer):
    def _add_new_metrics(self):
        self.metrics["NormComplexity"] = self.metrics["Complexity"] + 1
        self.metrics["NormCA"] = self.metrics["CA"] + 1
        self.metrics["CP_Criteria"] = 100 - (((self.min_CA + 1)**2 + (self.min_complexity +1)**2)**0.5 \
                                       / (self.metrics["NormComplexity"]**2 + self.metrics["NormCA"]**2)**0.5) * 100
