#!/usr/bin/env python3
import csv
from collections import defaultdict

def main():
    unique_barcodes = set()
    duplicated_barcodes = set()
    unused_barcodes = set()
    order_barcode = dict()

    (duplicated_barcodes, unused_barcodes, orders_with_barcodes) = process_barcodes()


    (customer_orders, wrong_orders) = process_orders(orders_with_barcodes)
    
    
    
    customer_orders_with_barcodes = dict()
    for customer, orders in customer_orders.items():
        customer_orders_final = {}
        for order in orders:
            customer_orders_final[order] = orders_with_barcodes.get(order)
        customer_orders_with_barcodes[customer] = customer_orders_final

    for customer,orders in customer_orders_with_barcodes.items():
        for order, barcodes in orders.items():
            if barcodes:
                print(customer + ',' + order + ',' + ','.join(barcodes))
            else:
                print(customer + ',' + order + ',')

def process_orders(orders_with_barcodes):
    wrong_orders = set()
    customer_orders = defaultdict(lambda: list())

    with open('orders.csv') as csv_file:
        orders = csv.DictReader(csv_file, delimiter=',')
        for row_order in orders:
            order = row_order['order_id']
            customer = row_order['customer_id']

            if order not in orders_with_barcodes.keys():
                wrong_orders.add(order)
                continue

            customer_orders[customer].append(order)
    return (customer_orders, wrong_orders)

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