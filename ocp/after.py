import datetime
import unittest


YEAR = datetime.timedelta(days=365)
SENIOR_AGE = 65 * YEAR


class Customer:
    def __init__(self, first_purchase_date, birth_date, is_veteran):
        assert isinstance(first_purchase_date, (type(None), datetime.datetime))
        assert isinstance(birth_date, datetime.datetime)
        assert isinstance(is_veteran, bool)

        self.first_purchase_date = first_purchase_date
        self.birth_date = birth_date
        self.is_veteran = is_veteran


class Discount:
    discount_if_eligible = 0

    def is_eligible(self, customer):
        raise False

    def get_discount(self, customer):
        if self.is_eligible(customer):
            return self.discount_if_eligible
        else:
            return 0


class SeniorDiscount(Discount):
    discount_if_eligible = 5
    def is_eligible(self, customer):
        now = datetime.datetime.now()
        return customer.birth_date <= now - SENIOR_AGE


class NewClientDiscount(Discount):
    discount_if_eligible = 15
    def is_eligible(self, customer):
        return customer.first_purchase_date is None


class LoyalCustomerDiscount(Discount):
    def __init__(self, years, discount):
        self.years = years
        self.discount = discount

    def is_eligible(self, customer):
        now = datetime.datetime.now()
        return (customer.first_purchase_date is not None and
                customer.first_purchase_date <= now - self.years * YEAR)
    
    @property
    def discount_if_eligible(self):
        return self.discount


class VeteranDiscount(Discount):
    discount_if_eligible = 10
    def is_eligible(self, customer):
        return customer.is_veteran


DEFAULT_DISCOUNT_RULES = [
    SeniorDiscount(),
    NewClientDiscount(),
    LoyalCustomerDiscount(years=1, discount=10),
    LoyalCustomerDiscount(years=5, discount=12),
    LoyalCustomerDiscount(years=10, discount=20),
    VeteranDiscount(),
]


def calculate_discount_percentage(customer):
    discounts = [d.get_discount(customer) for d in DEFAULT_DISCOUNT_RULES]
    return max(discounts, default=0)


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
