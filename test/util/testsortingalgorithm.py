from unittest import TestCase
from src.util.sortingalgorithm import SortingAlgorithm


class TestSortingAlgorithm(TestCase):

    def test_quick_sort(self):
        input_list = [34, 1, 55, 12, 981, 3, 8, 88]
        sorting_algorithm = SortingAlgorithm("quick_sort")
        print(str(sorting_algorithm(input_list)))
