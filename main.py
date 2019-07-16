#!/usr/bin/env python3
import sys
import csv
from collections import defaultdict

def main(output_file):
    (duplicated_barcodes, unused_barcodes, orders_with_barcodes) = process_barcodes()
    if duplicated_barcodes:
        sys.stderr.write("Ignoring duplicated barcodes:\n" + '\n'.join(duplicated_barcodes) + '\n')
    
    (customers_with_orders, wrong_orders) = process_orders(orders_with_barcodes)
    if wrong_orders:
        sys.stderr.write("Ignoring orders without barcodes:\n" + '\n'.join(wrong_orders) + '\n')
    
    customer_orders_with_barcodes = aggregate_data(customers_with_orders, orders_with_barcodes)

    top_customers = calculate_top_users(customers_with_orders)

    write_results(output_filename, customer_orders_with_barcodes, unused_barcodes, top_customers)

def calculate_top_users(customers_with_orders, amount=5):
    customers = list(map(lambda item:(item[0], len(item[1])), customers_with_orders.items()))
    top_customers = sorted(customers, key=lambda item:item[1], reverse=True)[:amount]
    return top_customers

def write_results(output_filename, customer_orders_with_barcodes, unused_barcodes, top_customers):
    sys.stdout.write('The top 5 users were:\n')
    sys.stdout.write('\n'.join(f'{x[0]}, {x[1]}' for x in top_customers) + '\n')

    output_filename = 'output.csv'
    with open(output_filename, 'w', newline='') as output_file:
        fieldnames = ['customer_id', 'order_id', 'barcodes']
        writer = csv.writer(output_file)
        writer.writerow(fieldnames)
        for customer,orders in customer_orders_with_barcodes.items():
            for order, barcodes in orders.items():
                row = flatten([customer, order, barcodes])
                writer.writerow(row)

def flatten(list_param):
  for item in list_param:
    if isinstance(item, list):
      for subitem in item: yield subitem
    else:
      yield item

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
    output_filename = 'output.csv'
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    main(output_filename)