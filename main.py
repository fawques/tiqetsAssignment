#!/usr/bin/env python3
import csv

def main():
    customer_orders = dict()
    order_barcode = dict()
    
    with open('orders.csv') as csv_file_2:
        orders = csv.DictReader(csv_file_2, delimiter=',')
        for row_order in orders:
            if row_order['customer_id'] not in customer_orders.keys():
                customer_orders[row_order['customer_id']] = []
            customer_orders[row_order['customer_id']].append(row_order['order_id'])
    
    with open('barcodes.csv') as csv_file:
        barcodes = csv.DictReader(csv_file, delimiter=',')
        for row_barcode in barcodes:
            if row_barcode['order_id'] not in order_barcode.keys():
                order_barcode[row_barcode['order_id']] = []
            order_barcode[row_barcode['order_id']].append(row_barcode['barcode'])
    
    customer_order_barcode = dict()
    for customer, orders in customer_orders.items():
        customer_orders_final = {}
        for order in orders:
            customer_orders_final[order] = order_barcode.get(order)
        customer_order_barcode[customer] = customer_orders_final

    for customer,orders in customer_order_barcode.items():
        for order, barcodes in orders.items():
            if barcodes:
                print(customer + ',' + order + ',' + ','.join(barcodes))
            else:
                print(customer + ',' + order + ',')



if __name__ == '__main__':
    main()