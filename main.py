#!/usr/bin/env python3
import csv
from collections import defaultdict

def main():
    unique_barcodes = set()
    duplicated_barcodes = set()
    unused_barcodes = set()
    order_barcode = dict()

    (duplicated_barcodes, unused_barcodes, orders_with_barcodes) = process_barcodes()
    (customers_with_orders, wrong_orders) = process_orders(orders_with_barcodes)
    
    customer_orders_with_barcodes = aggregate_data(customers_with_orders, orders_with_barcodes)

    for customer,orders in customer_orders_with_barcodes.items():
        for order, barcodes in orders.items():
            if barcodes:
                print(customer + ',' + order + ',' + ','.join(barcodes))
            else:
                print(customer + ',' + order + ',')

def aggregate_data(customers_with_orders, orders_with_barcodes):
    customer_orders_with_barcodes = {}
    for customer, orders in customers_with_orders.items():
        customer_orders_with_barcodes[customer] = {}
        for order in orders:
            customer_orders_with_barcodes[customer].update({order : orders_with_barcodes[order]})
    return customer_orders_with_barcodes

def process_orders(orders_with_barcodes):
    wrong_orders = set()
    customers_with_orders = defaultdict(lambda: list())

    with open('orders.csv') as csv_file:
        orders = csv.DictReader(csv_file, delimiter=',')
        for row_order in orders:
            order = row_order['order_id']
            customer = row_order['customer_id']

            if order not in orders_with_barcodes.keys():
                wrong_orders.add(order)
                continue

            customers_with_orders[customer].append(order)
    return (customers_with_orders, wrong_orders)

def process_barcodes():
    duplicated_barcodes = set()
    unique_barcodes = set()
    unused_barcodes = set()
    orders_with_barcodes = defaultdict(lambda: list())
    
    with open('barcodes.csv') as csv_file:
        barcodes = csv.DictReader(csv_file, delimiter=',')
        for row_barcode in barcodes:
            barcode = row_barcode['barcode']
            order = row_barcode['order_id']

            if barcode not in unique_barcodes:
                unique_barcodes.add(barcode)
            else:
                unique_barcodes.remove(barcode)
                duplicated_barcodes.add(barcode)

            if order:
                orders_with_barcodes[order].append(barcode)
            else:
                unused_barcodes.add(barcode)
    
    return (duplicated_barcodes, unused_barcodes, orders_with_barcodes) 



if __name__ == '__main__':
    main()