from django.test import TestCase
from cabin import queries
from django.db.models.query import QuerySet


class SampleTests(TestCase):
    fixtures = ['sample_test_fixture.json']

    def test_1(self):
        q = queries.query_1(2)
        self.assertEqual(q['payment_sum'], 26000)

        q = queries.query_1(3)
        self.assertEqual(q['payment_sum'], 24000)

        q = queries.query_1(4)
        self.assertEqual(q['payment_sum'], None)

        q = queries.query_1(5)
        self.assertEqual(q['payment_sum'], 7500)

    def test_2(self):
        q = queries.query_2(1)
        self.assertEqual(type(q), QuerySet)
        self.assertEqual(q.count(), 2)
        q_list = []
        for i in q:
            q_list.append(i.id)
        self.assertEqual(sorted(q_list), [1, 5])

        q = queries.query_2(3)
        self.assertEqual(type(q), QuerySet)
        self.assertEqual(q.count(), 1)
        q_list = []
        for i in q:
            q_list.append(i.id)
        self.assertEqual(sorted(q_list), [3, ])

    def test_3(self):
        q = queries.query_3(5000)
        self.assertEqual(q, 5)
        q = queries.query_3(8500)
        self.assertEqual(q, 4)
        q = queries.query_3(10000)
        self.assertEqual(q, 3)
        q = queries.query_3(10900)
        self.assertEqual(q, 1)

    def test_4(self):
        q = queries.query_4(25, 60, 15)
        self.assertEqual(type(q), QuerySet)
        self.assertEqual(q.count(), 1)
        q_list = []
        for i in q:
            q_list.append(i.id)
        self.assertEqual(sorted(q_list), [2])

        q = queries.query_4(55, 35, 40)
        self.assertEqual(type(q), QuerySet)
        self.assertEqual(q.count(), 2)
        q_list = []
        for i in q:
            q_list.append(i.id)
        self.assertEqual(sorted(q_list), [1, 3])

        q = queries.query_4(40, 40, 70)
        self.assertEqual(type(q), QuerySet)
        self.assertEqual(q.count(), 3)
        q_list = []
        for i in q:
            q_list.append(i.id)
        self.assertEqual(sorted(q_list), [1, 2, 3])

    def test_5(self):
        q = queries.query_5(1, 'White')
        self.assertEqual(type(q), QuerySet)
        self.assertEqual(q.count(), 1)
        q_list = []
        for i in q:
            q_list.append(i.id)
        self.assertEqual(sorted(q_list), [5, ])

        q = queries.query_5(1, 'Gray')
        self.assertEqual(type(q), QuerySet)
        self.assertEqual(q.count(), 2)
        q_list = []
        for i in q:
            q_list.append(i.id)
        self.assertEqual(sorted(q_list), [3, 5])

    def test_6(self):
        # only for checking queries has no bugs
        queries.query_6(0, 0)

    def test_7(self):
        # only for checking queries has no bugs

        queries.query_7()

    def test_8(self):
        # only for checking queries has no bugs

        queries.query_8()

    def test_9(self):
        # only for checking queries has no bugs

        queries.query_9(93, 5000)

    def test_10(self):
        # only for checking queries has no bugs

        queries.query_10()
