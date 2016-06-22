# The class merges files with CA and Cyclomatic complexity metrics

import re
CKJM_ITEMS_SEPARATOR = " "
INDEX_CYVIS_CLASS_NAME = 1
INDEX_CYVIS_PACKAGE = 0
INDEX_CKJM_CA = 7
INDEX_CKJM_COB = 4
INDEX_CKJM_CLASS_NAME = 0
CYVIS_ITEM_SEPARATOR = ","


class CBMerger:
    def __init__(self, coupling_metric_file, complexity_metric_file, out_file_name):
        self.coupling_metric_file = coupling_metric_file
        self.complexity_metric_file = complexity_metric_file
        self.out_file_name = out_file_name

    # returns tuple containing class name  and corresponding COB and CA metric values
    # from file containing CA information
    @staticmethod
    def _couple_tuple(line):
        data = line.split(CKJM_ITEMS_SEPARATOR)
        return data[INDEX_CKJM_CLASS_NAME], [int(data[INDEX_CKJM_COB]), int(data[INDEX_CKJM_CA])]

    # returns class name from the file containing Cyclomatic complexity information
    @staticmethod
    def _get_class_name(parsed_line):
        return parsed_line[INDEX_CYVIS_PACKAGE] + "." + parsed_line[INDEX_CYVIS_CLASS_NAME]

    # returns Cyclomatic complexity from the file containing Cyclomatic complexity information
    @staticmethod
    def _get_complexity_metric(parsed_line):
        line_len = len(parsed_line)
        # if no complexity information (no methods)
        if line_len <= 2:
            return 0
        complexity = 0
        # iterate over all methods and sum up all complexities to get the complexity of the class
        for ind in range(3, line_len, 4):
            if parsed_line[ind] and re.match('\d+', parsed_line[ind]):
                complexity += int(parsed_line[ind])
        return complexity

    def merge_metrics(self):
        with open(self.coupling_metric_file, "r") as coupling_data_file:
            classes_info = dict([self._couple_tuple(line) for line in coupling_data_file])

        with open(self.complexity_metric_file, "r") as complexity_data_file:
            for line in complexity_data_file:
                parsed_line = line.split(CYVIS_ITEM_SEPARATOR)
                class_name = self._get_class_name(parsed_line)
                complexity_metric = self._get_complexity_metric(parsed_line)
                if class_name != "" and complexity_metric and class_name in classes_info:
                    classes_info[class_name].append(int(complexity_metric))

        with open(self.out_file_name, "w") as out:
            # ClassName,  COB, CA, Complexity
            out.write("ClassName,COB,CA,Complexity\n")
            for clazz, metrics in classes_info.items():
                if len(metrics) == 3:
                    out_line = clazz + "," + ",".join(str(it) for it in metrics) + "\n"
                    out.write(out_line)
