#!/usr/bin/env python3
import csv

def main():
    unique_barcodes = set()
    duplicated_barcodes = set()
    unused_barcodes = set()
    order_barcode = dict()

    (duplicated_barcodes, unused_barcodes, orders_with_barcodes) = process_barcodes()


    customer_orders = process_orders()
    
    
    
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
    customer_orders = dict()

    with open('orders.csv') as csv_file:
        orders = csv.DictReader(csv_file, delimiter=',')
        for row_order in orders:
            order = row_order['order_id']
            customer = row_order['customer_id']
            if customer not in customer_orders.keys():
                customer_orders[customer] = []
            customer_orders[customer].append(order)
    return customer_orders

def process_barcodes():
    duplicated_barcodes = set()
    orders_with_barcodes = dict()
    unique_barcodes = set()
    unused_barcodes = set()
    
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
                if order not in orders_with_barcodes.keys():
                    orders_with_barcodes[order] = []
                orders_with_barcodes[order].append(barcode)
            else:
                unused_barcodes.add(barcode)
    
    return (duplicated_barcodes, unused_barcodes, orders_with_barcodes) 



if __name__ == '__main__':
    main()