from CommonTools import CommonTools
from BruteForceRuleGeneration import BruteForceRuleGeneration


class AprioriRuleGeneration(BruteForceRuleGeneration):
    infrequent_items = list()

    # itemset generation logic
    # f(k-1) candidate generation
    def fKMinusOneGeneration(self, level):
        # list of itemset at the new level
        results = list()
        # previous itemset
        prev = list()
        # level 1 only
        if level == 1:
            input = [next(iter(s)) for s in self.item_lattice[level - 1]]
            return [frozenset(i) for i in list(CommonTools.combinations(input, level + 1))]
        for idx, itemset in enumerate(self.item_lattice[level - 1]):
            # sorted itemset
            itemset = sorted(list(itemset))
            # setup first itemset
            if idx == 0:
                prev = itemset
                continue
            # set currennt itemset
            current = itemset
            # flag to see if k-1 items are the same
            sameKMinusOneItems = True
            # new itemset
            result = list()
            #goes through each item in current and previous itemset
            for l in range(level - 1):
                if prev[l] != current[l]:
                    sameKMinusOneItems = False
                    break
                else:
                    result.append(current[l])
            #adds new candidate
            if sameKMinusOneItems:
                result.append(prev[level - 1])
                result.append(current[level - 1])
                result = frozenset(result)
                #check if result is a superset of infrequent item
                for infrequent_item in self.infrequent_items:
                    if result.issuperset(infrequent_item):
                        sameKMinusOneItems = False
                        break
                if sameKMinusOneItems:
                    results.append(frozenset(result))
            #resets each itemset
            prev = current
        #returns the new candidates
        return results

    # level 0 lists all products. level>0 uses f(k-1) f(k-1) generation logic (private helper method)
    def generate_itemset(self, level):
        if level == 0:
            self.item_lattice[level] = [frozenset(i) for i in
                                        list(CommonTools.combinations(self.all_products, level + 1))]
        elif level > 0:
            self.item_lattice[level] = self.fKMinusOneGeneration(level)

    def remove_infrequent_itemsets(self, level):
        result = list()
        self.infrequent_items = list()
        for itemset in self.item_lattice[level]:
            if self.get_support_count(itemset) >= self.support_threshold:
                result.append(itemset)
            else:
                self.infrequent_items.append(itemset)
        self.item_lattice[level] = result

    def candidate_generation(self):
        candidate_itemsets = list()
        max_level = 0
        while len(self.get_support_lattice(max_level)) > 0:
            self.remove_infrequent_itemsets(max_level)
            candidate_itemsets = candidate_itemsets + [k for candidate in self.get_support_lattice(max_level) for k in
                                                       candidate]
            max_level += 1
        return candidate_itemsets
