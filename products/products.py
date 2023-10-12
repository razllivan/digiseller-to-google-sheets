class Product:
    def __init__(self, product_id, name, price, cnt_sell):
        self.id = product_id
        self.name = name
        self.price = price
        self.cnt_sell = cnt_sell

    @staticmethod
    def to_gs_format(products: list['Product']) -> list[list[str]]:
        return [[product.id, product.name, product.price, product.cnt_sell]
                for product in products]
