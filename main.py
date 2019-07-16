#!/usr/bin/env python3
import csv

def main():
    unique_barcodes = set()
    duplicated_barcodes = set()
    unused_barcodes = set()
    order_barcode = dict()


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
                if order not in order_barcode.keys():
                    order_barcode[order] = []
                order_barcode[order].append(barcode)
            else:
                unused_barcodes.add(barcode)


    customer_orders = dict()
    
    with open('orders.csv') as csv_file_2:
        orders = csv.DictReader(csv_file_2, delimiter=',')
        for row_order in orders:
            if row_order['customer_id'] not in customer_orders.keys():
                customer_orders[row_order['customer_id']] = []
            customer_orders[row_order['customer_id']].append(row_order['order_id'])
    
    
    
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