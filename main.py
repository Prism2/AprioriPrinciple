from AprioriRuleGeneration import AprioriRuleGeneration
from BruteForceRuleGeneration import BruteForceRuleGeneration
from CommonTools import CommonTools

import pandas as pd
import ast
import time


# def read_transactions(file_number):
# all_products = pd.read_excel(r'transactions.xlsx', sheet_name='all_products')
# all_products = all_products['Product'].to_list()
# database = pd.read_excel(r'transactions.xlsx', sheet_name='database_{}'.format(file_number))
# transactions = [set(ast.literal_eval(i)) for i in list(database['transactions'])]
# return all_products, transactions


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
    print("--- %s seconds ---" % (time.time() - start_time))
    print("\n")

    print("Generating association rules using Apriori principle optimization for sheet {}".format(transaction_file))
    start_time = time.time()
    rule_generator = AprioriRuleGeneration(common)
    rule_generator.rule_generation()
    print("--- %s seconds ---" % (time.time() - start_time))
    print("\n")


def user_run_rule():
    print("\n")
    print("Please input the minimum support value:")
    support = float(input())
    print("Please input the minimum confidence value:")
    confidence = float(input())
    print("Please input the filename containing the transaction data:")
    tranaction = input()
    print("\n")
    generate_association_rule_from_dataset(support, confidence, tranaction)


if __name__ == '__main__':
    user_run_rule()
