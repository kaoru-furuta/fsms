from itertools import groupby

from sales.models import Sale


class Summary:
    def __init__(self):
        self.sale_list = Sale.objects.all()

    def total(self):
        return sum(s.amount for s in self.sale_list)

    def calc(self, interval):
        if interval == 'monthly':
            date_format = '%Y/%m'
        else:
            date_format = '%Y/%m/%d'

        result_list = []

        sorted_list = sorted(self.sale_list, key=lambda x: x.sold_at, reverse=True)
        for key, group in groupby(sorted_list, lambda x: x.sold_at.strftime(date_format)):
            group = list(group)
            fruit_list = self.calc_fruit(group)
            result_list.append({
                'sold_at': key,
                'amount': sum(sale.amount for sale in group),
                'fruits': ' '.join(
                    f'{fruit["name"]}:{fruit["amount"]}円({fruit["number"]})' for fruit in fruit_list
                )
            })

        return result_list[:3]

    @classmethod
    def calc_fruit(cls, sale_list):
        fruit_list = []

        sorted_list = sorted(sale_list, key=lambda x: x.fruit.name)
        for key, group in groupby(sorted_list, lambda x: x.fruit.name):
            group = list(group)
            fruit_list.append({
                'name': key,
                'number': sum(g.number for g in group),
                'amount': sum(g.amount for g in group)
            })

        return fruit_list
