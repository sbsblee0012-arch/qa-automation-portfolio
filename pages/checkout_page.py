class CheckoutPage:
    def __init__(self, page):
        self.page = page

    def enter_info(self, first_name, last_name, postal_code):
        self.page.fill("[data-test='firstName']", first_name)
        self.page.fill("[data-test='lastName']", last_name)
        self.page.fill("[data-test='postalCode']", postal_code)

    def continue_checkout(self):
        self.page.click("[data-test='continue']")

    def finish(self):
        self.page.click("[data-test='finish']")

    def is_complete(self):
        return "checkout-complete" in self.page.url