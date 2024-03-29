from CommonTools import CommonTools


class BruteForceRuleGeneration:

    # constructor
    def __init__(self, commonTools):
        self.all_products = commonTools.all_products
        self.support_threshold = commonTools.support_threshold
        self.min_confidence = commonTools.min_confidence
        self.commonTools = commonTools
        # level: itemsets
        self.item_lattice = dict()
        # itemset: count
        self.support_lattice = dict()
        # list of candidate itemsets
        self.candidate_itemsets = list()

    # itemset generation logic
    # level starts with 0 and generates all possible combinations of products at that level (private helper method)
    def generate_itemset(self, level):
        self.item_lattice[level] = [frozenset(i) for i in list(CommonTools.combinations(self.all_products, level + 1))]

    # gets the combination of products at specific level and caches (private method)
    def __get_item_lattice(self, level):
        if level not in self.item_lattice:
            self.generate_itemset(level)
        return self.item_lattice[level]

    # calculate support logic
    # add to counter
    def __increment_support_lattice_count(self, itemset):
        if itemset in self.support_lattice:
            self.support_lattice[itemset] += 1
        else:
            self.support_lattice[itemset] = 1

    # helper method comapares a single itemset with all transactions
    def __compare_itemset_with_transactions(self, itemset):
        for transaction in self.commonTools.read_current_transactions():
            if itemset.issubset(transaction):
                self.__increment_support_lattice_count(itemset)

    # generate the support based on level
    def __generate_support(self, level):
        for itemset in self.__get_item_lattice(level):
            self.__compare_itemset_with_transactions(itemset)

    # public method to generate both item and support per level
    def get_support_lattice(self, level):
        if level not in self.item_lattice:
            self.__generate_support(level)
        return [{item: self.support_lattice.get(item, 0)} for item in self.item_lattice[level] if
                self.support_lattice.get(item, 0) >= self.support_threshold]

    # gets the support level for a single item
    def get_support_count(self, item):
        return self.support_lattice.get(item, 0)

    def candidate_generation(self):
        if self.candidate_itemsets:
            return self.candidate_itemsets
        candidate_itemsets = list()
        max_level = 0
        while len(self.get_support_lattice(max_level)) > 0:
            candidate_itemsets = candidate_itemsets + [k for candidate in self.get_support_lattice(max_level) for k in
                                                       candidate]
            max_level += 1
        self.candidate_itemsets = candidate_itemsets
        return candidate_itemsets

    def rule_generation(self):
        candidate_itemsets = self.candidate_generation()
        for itemset in candidate_itemsets:
            numerator = self.get_support_count(itemset)
            max_denom_level = len(itemset) - 1
            for level in range(max_denom_level):
                for combination in CommonTools.combinations(itemset, level + 1):
                    precedent = frozenset(combination)
                    denominator = self.get_support_count(precedent)
                    if numerator / denominator >= self.min_confidence:
                        output = "{} -> {} Support level: {} Confidence level: {}"
                        precedent_str = str(precedent)[10:-1]
                        consequent_str = str(itemset.difference(precedent))[10:-1]
                        support = numerator / len(self.commonTools.all_products)
                        confidence = numerator / denominator
                        print(output.format(precedent_str,
                                            consequent_str,
                                            support,
                                            confidence))
