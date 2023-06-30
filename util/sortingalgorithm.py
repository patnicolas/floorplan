__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from typing import AnyStr, Any, List


class SortingAlgorithm(object):
    """
        Wraps the various sorting algorithms
        :param algorithm_type Specify the type of sorting algorithm, 'quick_sort', 'merge_sort' ...
    """
    def __init__(self, algorithm_type: AnyStr):
        if algorithm_type == 'merge_sort':
            self.algorithm_type = lambda x: SortingAlgorithm.__merge_sort(x)
        else:
            self.algorithm_type = lambda x: SortingAlgorithm.__quick_sort(x)

    def __call__(self, list_to_sort: List[Any]):
        return self.algorithm_type(list_to_sort)

    @staticmethod
    def __quick_sort(_in_list: List[Any]) -> List[Any]:
        """
            Quick sort: Worst case scenario time complexity O(n.n)
                        Average case scenario O(n.log(n))
        """
        def partition(items: List[Any], low: int, high: int) -> int:
            pivot = items[(low + high) // 2]
            i = low - 1
            j = high + 1
            while True:
                i += 1
                while items[i] < pivot:
                    i += 1
                j -= 1
                while items[j] > pivot:
                    j -= 1
                if i >= j:
                    return i
                items[i], items[j] = items[j], items[i]

        def quick_sort(items: List[Any], low: int, high: int):
            if low < high:
                split_index = partition(items, low, high)
                quick_sort(items, low, split_index)
                quick_sort(items, split_index+1, high)

        quick_sort(_in_list, 0, len(_in_list) - 1)
        return _in_list

    @staticmethod
    def __merge_sort(in_list: List[Any]) -> List[Any]:
        """
            recursive execution of merge sort
            :param in_list Input list to sort
        """
        if len(in_list) <= 1:
            return in_list
        mid = len(in_list) // 2
        left_list = SortingAlgorithm.__merge_sort(in_list[:mid])
        right_list = SortingAlgorithm.__merge_sort(in_list[mid:])
        return SortingAlgorithm.__merge(left_list, right_list)

    @staticmethod
    def __merge(left_list: List[Any], right_list: List[Any]):
        sorted_list = []
        left_list_index = right_list_index = 0
        left_list_len = len(left_list)
        right_list_len = len(right_list)

        for _ in range(left_list_len + right_list_len):
            if left_list_index < left_list_len and right_list_index < right_list_len:
                # Check which value from the start of each list (left, or right) is smaller

                # If the item at the start of the left list is smaller add it to the sorted list
                if left_list[left_list_index] <= right_list[right_list_index]:
                    sorted_list.append(left_list[left_list_index])
                    left_list_index += 1
                # otherwise add the item of the start of the right list to the sorted list
                else:
                    sorted_list.append(right_list[right_list_index])
                    right_list_index += 1

            # If we reach the end of the left list....add the element from the right list
            elif left_list_index == left_list_len:
                sorted_list.append(right_list[right_list_index])
                right_list_index += 1

            elif right_list_index == right_list_len:
                sorted_list.append(left_list[left_list_index])
                left_list_index += 1
        return sorted_list


if __name__ == '__main__':
    input_list = [34, 1, 55, 12, 981, 3, 8, 88]
    sorting_algorithm = SortingAlgorithm("quick_sort")
    print(str(sorting_algorithm(input_list)))

