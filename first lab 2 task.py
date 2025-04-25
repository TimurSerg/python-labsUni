def update_inventory(product, quantity, inventory):
    if product in inventory:
        inventory[product] += quantity
    else:
        inventory[product] = quantity

    # Видаляємо продукти, якщо їх кількість менше 5
    low_stock_products = [prod for prod, qty in inventory.items() if qty < 5]
    return inventory, low_stock_products

inventory = {'apple': 10, 'banana': 3, 'orange': 2}
update_inventory('apple', 5, inventory)
update_inventory('banana', -1, inventory)
inventory, low_stock_products = update_inventory('orange', -1, inventory)
print(inventory)
print(low_stock_products)