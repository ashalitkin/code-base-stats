class CBMerger:
    def __init__(self, coupling_metric_file, complexity_metric_file, out_file_name):
        self.coupling_metric_file = coupling_metric_file
        self.complexity_metric_file = complexity_metric_file
        self.out_file_name = out_file_name

    @staticmethod
    def _couple_tuple(line):
        data = line.split(" ")
        return data[0], [int(data[4]), int(data[7])]

    @staticmethod
    def _get_class_name(parsed_line):
        return parsed_line[0] + "." + parsed_line[1]

    @staticmethod
    def _get_complexity_metric(parsed_line):
        line_len = len(parsed_line)
        if line_len <= 2:
            return 0
        complexity = 0
        for ind in range(3, line_len, 4):
            complexity += int(parsed_line[ind])
        return complexity

    def merge_metrics(self):
        with open(self.coupling_metric_file, "r") as coupling_data_file:
            classes_info = dict([self._couple_tuple(line) for line in coupling_data_file])

        with open(self.complexity_metric_file, "r") as complexity_data_file:
            for line in complexity_data_file:
                parsed_line = line.split(",")
                class_name = self._get_class_name(parsed_line)
                complexity_metric = self._get_complexity_metric(parsed_line)
                if class_name != "" and complexity_metric and class_name in classes_info:
                    classes_info[class_name].append(int(complexity_metric))

        with open(self.out_file_name, "w") as out:
            # COB, CA, Complexity
            out.write("ClassName,COB,CA,Complexity\n")
            for clazz, metrics in classes_info.items():
                if len(metrics) == 3:
                    out_line = clazz + "," + ",".join(str(it) for it in metrics) + "\n"
                    out.write(out_line)
