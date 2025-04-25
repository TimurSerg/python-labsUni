def sales_statistics(sales):
    income = {}
    for sale in sales:
        product = sale['product']
        total_income = sale['quantity'] * sale['price']
        if product in income:
            income[product] += total_income
        else:
            income[product] = total_income
    return income

sales = [
    {'product': 'apple', 'quantity': 10, 'price': 2},
    {'product': 'banana', 'quantity': 5, 'price': 1.5},
    {'product': 'apple', 'quantity': 7, 'price': 2}
]
income = sales_statistics(sales)

# Створюємо список продуктів, де дохід більше ніж 1000
high_income_products = [product for product, total in income.items() if total > 1000]
print(income)
print(high_income_products)