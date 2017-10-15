import datetime
import unittest


class Customer:
    def __init__(self, first_purchase_date, birth_date, is_veteran):
        assert isinstance(first_purchase_date, (type(None), datetime.datetime))
        assert isinstance(birth_date, datetime.datetime)
        assert isinstance(is_veteran, bool)

        self.first_purchase_date = first_purchase_date
        self.birth_date = birth_date
        self.is_veteran = is_veteran


def calculate_discount_percentage(customer):
    discount = 0
    now = datetime.datetime.now()
    year = datetime.timedelta(days=365)
    if customer.birth_date <= now - 65*year:
        # senior discount
        discount = 5
    if customer.first_purchase_date is not None:
        if customer.first_purchase_date <= now - year:
            # after one year, loyal customers get 10%
            discount = 10
            if customer.first_purchase_date <= now - 5*year:
                # after five years, 12%
                discount = 12
                if customer.first_purchase_date <= now - 10*year:
                    # after ten years, 20%
                    discount = 20
    else:
        # first time purchase ==> 15% discount
        discount = 15
    if customer.is_veteran:
        discount = max(discount, 10)
    return discount


class CalculateDiscountPercentageTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime.now()
        self.year = datetime.timedelta(days=365)

    def test_should_return_zero_for_casual_customer(self):
        customer = Customer(first_purchase_date=self.now,
                            birth_date=self.now-20*self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 0
        self.assertEqual(got, expected)

    def test_should_return_15_for_new_client(self):
        customer = Customer(first_purchase_date=None,
                            birth_date=self.now-20*self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 15
        self.assertEqual(got, expected)

    def test_should_return_10_for_veteran(self):
        customer = Customer(first_purchase_date=self.now,
                            birth_date=self.now-20*self.year,
                            is_veteran=True)
        got = calculate_discount_percentage(customer)
        expected = 10
        self.assertEqual(got, expected)

    def test_should_return_5_for_a_senior(self):
        customer = Customer(first_purchase_date=self.now,
                            birth_date=self.now-65*self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 5
        self.assertEqual(got, expected)

    def test_should_return_10_for_a_loyal_customer(self):
        customer = Customer(first_purchase_date=self.now-1*self.year,
                            birth_date=self.now-20*self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 10
        self.assertEqual(got, expected)

    def test_should_return_12_for_a_more_loyal_customer(self):
        customer = Customer(first_purchase_date=self.now-5*self.year,
                            birth_date=self.now-20*self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 12
        self.assertEqual(got, expected)

    def test_should_return_20_for_a_most_loyal_customer(self):
        customer = Customer(first_purchase_date=self.now-10*self.year,
                            birth_date=self.now-20*self.year,
                            is_veteran=False)
        got = calculate_discount_percentage(customer)
        expected = 20
        self.assertEqual(got, expected)

    def test_should_return_maximum_discount(self):
        customer = Customer(first_purchase_date=None,
                            birth_date=self.now-20*self.year,
                            is_veteran=True)
        # eligible for 15% discount as a new client and 10% as a veteran
        got = calculate_discount_percentage(customer)
        expected = 15
        self.assertEqual(got, expected)

if __name__ == "__main__":
    unittest.main()
