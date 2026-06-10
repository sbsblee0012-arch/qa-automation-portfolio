class InventoryPage:
    def __init__(self, page):
        self.page = page

    def click_first_item(self):
        self.page.click("[data-test='inventory-item-name']")

    def add_to_cart(self):
        self.page.click("[data-test='add-to-cart']")

    def get_cart_count(self):
        return self.page.locator("[data-test='shopping-cart-badge']").inner_text()

    def go_to_cart(self):
        self.page.click("[data-test='shopping-cart-link']")