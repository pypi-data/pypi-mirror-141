
import json

def parse_spending_patterns(response):
    return response["spendingPatterns"]

def parse_transaction_history(response):
    return response["historyItemList"] 