import csv

class CommonTools:
    # default support and confidence level
    def __init__(self, all_products, transaction_file, support_threshold=1, min_confidence=0.5):
        self.all_products = all_products
        self.transaction_file = transaction_file
        self.support_threshold = support_threshold
        self.min_confidence = min_confidence

    def read_current_transactions(self):
        with open(self.transaction_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            result = set()
            for row in csv_reader:
                yield frozenset(row)

    @staticmethod
    def read_transactions(transaction_file):
        with open(transaction_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                yield row

    @staticmethod
    def combinations(input_list, number):
        input_list = sorted(list(set(input_list)))
        input_list_length = len(input_list)
        if number <= 0 or number > input_list_length:
            return list()
        elif number == 1:
            return [[i] for i in input_list]
        results = list()
        # shows the current index of the current result from the input list
        index = list(range(number))
        index.append(input_list_length)
        result = input_list[:number]
        results.append(result.copy())
        idx = number - 1
        # loop completes when we process last combination
        while index[0] != len(input_list) - number:
            # reset value in result
            index[idx] += 1
            for i in range(idx, number - 1):
                index[i + 1] = index[i] + 1
                result[i] = input_list[index[i]]
            idx = number - 1
            # incrases index from right to left
            while index[idx] < index[idx + 1]:
                result[idx] = input_list[index[idx]]
                results.append(result.copy())
                index[idx] += 1
            # decreases position from right to left until there is a combination we haven't encountered
            while index[idx] + 1 >= index[idx + 1]:
                idx -= 1
        return results