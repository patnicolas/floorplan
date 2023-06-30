import polars as pl
from polars import Expr

"""
    Reference: https://pola-rs.github.io/polars/py-polars/html/reference/dataframe/api
"""


class PolarsEval(object):
    def __init__(self, input_data: dict[str, list[any]]):
        self.df = pl.DataFrame(input_data)

    def __str__(self) -> str:
        return str(self.df.limit())

    def metadata(self) -> str:
        return f'Types: {str(self.df.dtypes)}\nColumns: {str(self.df.columns)}'

    def insert(self, entry: dict[str, list[any]]) -> int:
        new_row_df = pl.DataFrame(entry)
        self.df = self.df.vstack(new_row_df)
        return len(self.df)

    def query(self, columns: list[str], condition: Expr) -> pl.DataFrame:
        assert len(columns) > 0, 'Columns in the query are undefined'
        return self.df.select(columns).filter(condition.is_in(True))


if __name__ == '__main__':
    data = {
        'name': ['Patrick', 'Betty'],
        'age': [46, 12],
        'score': [8.3, 9.1]
    }
    polar_eval = PolarsEval(data)
    new_data = {
        'name': ['Henry'],
        'age': [23],
        'score': [7.4]
    }
    polar_eval.insert(new_data)
    print(str(polar_eval))
    condition_age: Expr = pl.col("age") > 18
    print(str(polar_eval.query(['name', 'age'], condition_age)))

    # print(polar_eval.df.filter(pl.col("age") > 18))
