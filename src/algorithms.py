from abc import ABC, abstractmethod
from utils import generate_sound, play_short_beep

wave = generate_sound()

class SortingAlgorithm(ABC):
    """
    Abstract base class for sorting algorithms.

    Attributes:
        data (list): The list of data to be sorted.
        visualizer (SortVisualizer): The visualizer object to visualize the sorting process.
    """

    def __init__(self, data, visualizer):
        """
        Initialize the sorting algorithm with data and visualizer.

        Parameters:
            data (list): The data to be sorted.
            visualizer (SortVisualizer): The visualizer instance for visualizing the sorting.
        """
        self.data = data
        self.visualizer = visualizer

    @abstractmethod
    def sort(self):
        """
        Abstract method to sort the data. This method must be implemented by subclasses.

        Yields:
            bool: True after each step for visualization.
        """
        pass

class BubbleSort(SortingAlgorithm):
    """
    Class for Bubble Sort algorithm.
    """

    def sort(self):
        """
        Perform Bubble Sort on the data.

        Yields:
            bool: True after each swap for visualization.
        """
        n = len(self.data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    self.visualizer.draw_data(self.data, color_position=[j, j + 1])
                    yield True
            play_short_beep(wave)

class InsertionSort(SortingAlgorithm):
    """
    Class for Insertion Sort algorithm.
    """

    def sort(self):
        """
        Perform Insertion Sort on the data.

        Yields:
            bool: True after each insertion for visualization.
        """
        for i in range(1, len(self.data)):
            key = self.data[i]
            j = i - 1
            while j >= 0 and key < self.data[j]:
                self.data[j + 1] = self.data[j]
                self.visualizer.draw_data(self.data, color_position=[j, j + 1])
                yield True
                j -= 1
            self.data[j + 1] = key
            self.visualizer.draw_data(self.data, color_position=[j + 1])
            play_short_beep(wave)
            yield True

class HeapSort(SortingAlgorithm):
    """
    Class for Heap Sort algorithm.
    """

    def heapify(self, heap_size, root_index):
        """
        Heapify a subtree rooted with the node at the given index in the data.

        Parameters:
            heap_size (int): Size of the heap.
            root_index (int): Root index of the current subtree.

        Yields:
            bool: True after each swap for visualization.
        """
        largest_index = root_index
        left_child_index = 2 * root_index + 1
        right_child_index = 2 * root_index + 2

        # Check if left child exists and is greater than the root
        if left_child_index < heap_size and self.data[root_index] < self.data[left_child_index]:
            largest_index = left_child_index

        # Check if right child exists and is greater than the largest found so far
        if right_child_index < heap_size and self.data[largest_index] < self.data[right_child_index]:
            largest_index = right_child_index

        # If the largest is not the root, swap it with the largest and continue heapifying
        if largest_index != root_index:
            self.data[root_index], self.data[largest_index] = self.data[largest_index], self.data[root_index]
            self.visualizer.draw_data(self.data, color_position=[root_index, largest_index])
            yield True
            yield from self.heapify(heap_size, largest_index)


    def sort(self):
        """
        Perform Heap Sort on the data.

        Yields:
            bool: True after each swap or heapify operation for visualization.
        """
        n = len(self.data)

        for i in range(n // 2 - 1, -1, -1):
            yield from self.heapify(n, i)

        for i in range(n - 1, 0, -1):
            self.data[i], self.data[0] = self.data[0], self.data[i]
            self.visualizer.draw_data(self.data, color_position=[0, i])
            yield True
            yield from self.heapify(i, 0)
            play_short_beep(wave)

class QuickSort(SortingAlgorithm):
    """
    Class for Quick Sort algorithm.
    """

    def partition(self, low, high):
        """
        Partition the array on the basis of pivot element.

        Parameters:
            low (int): Starting index of the array.
            high (int): Ending index of the array.

        Yields:
            bool: True after each swap or partition operation for visualization.

        Returns:
            int: Index of the pivot element after partition.
        """
        i = low - 1
        pivot = self.data[high]

        for j in range(low, high):
            if self.data[j] <= pivot:
                i += 1
                self.data[i], self.data[j] = self.data[j], self.data[i]
                self.visualizer.draw_data(self.data, color_position=[i, j])
                yield True

        self.data[i + 1], self.data[high] = self.data[high], self.data[i + 1]
        self.visualizer.draw_data(self.data, color_position=[i + 1, high])
        yield True
        play_short_beep(wave)

        return i + 1

    def quick_sort(self, low, high):
        """
        Recursive function to perform Quick Sort.

        Parameters:
            low (int): Starting index of the array.
            high (int): Ending index of the array.

        Yields:
            bool: True after each recursive call for visualization.
        """
        if low < high:
            pi = yield from self.partition(low, high)
            yield from self.quick_sort(low, pi - 1)
            yield from self.quick_sort(pi + 1, high)
            play_short_beep(wave)

    def sort(self):
        """
        Perform Quick Sort on the data.

        Yields:
            bool: True after each recursive call for visualization.
        """
        yield from self.quick_sort(0, len(self.data) - 1)
        play_short_beep(wave)


class MergeSort(SortingAlgorithm):
    """
    Class for Merge Sort algorithm.
    """

    def merge(self, left, right):
        """
        Merge two sorted sublists.

        Parameters:
            left (list): Left sublist to merge.
            right (list): Right sublist to merge.

        Yields:
            bool: True after each merge operation for visualization.

        Returns:
            list: The merged sorted list.
        """
        result = []
        i, j = 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
            self.visualizer.draw_data(self.data, color_position=[i, j])
            yield True

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def merge_sort(self, start, end):
        """
        Recursive function to perform Merge Sort.

        Parameters:
            start (int): Starting index of the list.
            end (int): Ending index of the list.

        Yields:
            bool: True after each recursive call for visualization.
        """
        if end - start > 1:
            mid = (start + end) // 2
            yield from self.merge_sort(start, mid)
            yield from self.merge_sort(mid, end)
            result = yield from self.merge(self.data[start:mid], self.data[mid:end])
            self.data[start:end] = result
            self.visualizer.draw_data(self.data, color_position=range(start, end))
            yield True
            play_short_beep(wave)

    def sort(self):
        """
        Perform Merge Sort on the data.

        Yields:
            bool: True after each recursive call for visualization.
        """
        yield from self.merge_sort(0, len(self.data))
        
