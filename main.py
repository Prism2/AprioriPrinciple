from CommonTools import CommonTools
from BruteForceRuleGeneration import BruteForceRuleGeneration
from AprioriRuleGeneration import AprioriRuleGeneration

import time


def generate_association_rule_from_dataset(min_support, min_confidence, transaction_file):
    transactions = CommonTools.read_transactions(transaction_file)
    all_products = set()
    total_transactions = 0
    for transaction in transactions:
        for item in transaction:
            all_products.add(item)
        total_transactions += 1
    all_products = sorted(list(all_products))
    support_threshold = total_transactions * min_support
    common = CommonTools(all_products, transaction_file, support_threshold, min_confidence)
    print("Generating association rules using bruteforce method for {}".format(transaction_file))
    start_time = time.time()
    rule_generator = BruteForceRuleGeneration(common)
    rule_generator.rule_generation()
    brute_force_time = time.time() - start_time
    with open("intermediary_steps_{}_brute_force.txt".format(transaction_file[:-4]), "w") as writer:
        for candidate in rule_generator.candidate_itemsets:
            writer.write(str(candidate)[10:-1] + "\n")
    print("---------------- %s seconds ----------------" % brute_force_time)
    print("\n")

    print("Generating association rules using Apriori principle optimization for sheet {}"
          .format(transaction_file))
    start_time = time.time()
    rule_generator = AprioriRuleGeneration(common)
    rule_generator.rule_generation()
    apriori_time = time.time() - start_time
    with open("intermediary_steps_{}_apriori.txt".format(transaction_file[:-4]), "w") as writer:
        for candidate in rule_generator.candidate_itemsets:
            writer.write(str(candidate)[10:-1] + "\n")
    print("---------------- %s seconds ----------------" % apriori_time)
    print("\n")

    print("Apriori is {} times faster".format(brute_force_time/apriori_time))


def user_run_rule():
    print("\n")
    tranaction = input("Please input the filename containing the transaction data:")
    support = float(input("Please input the minimum support value:"))
    confidence = float(input("Please input the minimum confidence value:"))
    print("\n")
    generate_association_rule_from_dataset(support, confidence, tranaction)


if __name__ == '__main__':
    user_run_rule()
