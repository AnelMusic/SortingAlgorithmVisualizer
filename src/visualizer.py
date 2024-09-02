import pygame
import random
from constants import (
    BLACK, WHITE, RED, GREEN, BLUE, LIGHT_GRAY,
    BUTTON_HEIGHT, Y_OFFSET, BUTTON_WIDTH, CORNER_RADIUS, VISUALIZATION_HEIGHT, DATA_AREA_PADDING,
    SCREEN_WIDTH,  NUM_ELEMENTS, FONT_SIZE, ALGORITHM_BUTTON_X, CONTROL_BUTTON_X,
    BUTTON_START_Y, GRADIENT_LIGHTNESS_INCREASE)
from algorithms import BubbleSort, InsertionSort, HeapSort, QuickSort, MergeSort



class SortVisualizer:
    """ Manages the visualization of sorting algorithms along with UI interaction within a pygame window."""

    def __init__(self, screen, num_elements=NUM_ELEMENTS):
        """Initializes the sorting visualizer with a screen and a set number of elements."""
        self.screen = screen
        self.num_elements = num_elements
        self.data = list(range(1, self.num_elements + 1))
        self.original_data = self.data.copy()  # Copy of original data for reset functionality
        random.shuffle(self.data)  # Shuffle data to create an unsorted state
        self.sorting = False  # Flag to check if sorting is currently active
        self.sort_gen = None  # Generator for sorting operations
        self.selected_algorithm = None  # Currently selected sorting algorithm
        self.font = pygame.font.Font(None, FONT_SIZE)  # Font for drawing text on UI components
        # Dictionary to map algorithm names to their corresponding classes
        self.sorting_algorithms = {
            "Bubble Sort": BubbleSort,
            "Insertion Sort": InsertionSort,
            "Heap Sort": HeapSort,
            "Quick Sort": QuickSort,
            "Merge Sort": MergeSort,
        }
        
    def draw_data(self, data, color_position=None):
        """Clears the screen, draws the sorting area, and updates the UI."""
        self.clear_screen()
        self.draw_data_area()
        bar_width, height_scale = self.calculate_dimensions()
        self.draw_bars(data, bar_width, height_scale, color_position)
        self.create_ui()
        pygame.display.update()

    def clear_screen(self):
        """Fills the entire screen with the background color."""
        self.screen.fill(BLACK)

    def calculate_dimensions(self):
        """Calculates the width of bars and their scaling factor based on the screen size."""
        bar_width = (SCREEN_WIDTH - 2 * DATA_AREA_PADDING) // self.num_elements
        height_scale = (VISUALIZATION_HEIGHT - 50) / self.num_elements
        return bar_width, height_scale

    def draw_bars(self, data, bar_width, height_scale, color_position=None):
        """Draws bars for the sorting visualization."""
        for i, value in enumerate(data):
            color = RED if color_position and i in color_position else LIGHT_GRAY
            pygame.draw.rect(self.screen, color, 
                            (i * bar_width + DATA_AREA_PADDING, 
                            VISUALIZATION_HEIGHT - value * height_scale, 
                            bar_width, 
                            value * height_scale))

    def reset_data(self):
        """Resets the data to the original unsorted state and reshuffles it."""
        self.data = self.original_data.copy()
        random.shuffle(self.data)
        self.sorting = False
        self.sort_gen = None
        self.draw_data(self.data)

    def start_sorting(self):
        """Initializes the sorting process using the selected algorithm."""
        if self.selected_algorithm and not self.sorting:
            self.sorting = True
            self.sort_gen = self.selected_algorithm(self.data, self).sort()

    def create_ui(self):
        """Creates the user interface including buttons for algorithm selection and control."""
        self.draw_algorithm_menu()
        self.draw_control_buttons()

    def draw_data_area(self):
        """Draws the background area for the sorting visualization."""
        data_area_rect = pygame.Rect(DATA_AREA_PADDING, DATA_AREA_PADDING, 
                                     SCREEN_WIDTH - 2 * DATA_AREA_PADDING, 
                                     VISUALIZATION_HEIGHT - 2 * DATA_AREA_PADDING)
        pygame.draw.rect(self.screen, BLACK, data_area_rect)

    def draw_algorithm_menu(self):
        """Draws buttons for each sorting algorithm."""
        self.draw_button(pygame.Rect(ALGORITHM_BUTTON_X, BUTTON_START_Y, BUTTON_WIDTH, BUTTON_HEIGHT), 
                         "Algorithm", GREEN, WHITE, CORNER_RADIUS)
        y_position = BUTTON_START_Y + BUTTON_HEIGHT + Y_OFFSET
        for name, algo in self.sorting_algorithms.items():
            color = RED if self.selected_algorithm == algo else BLUE
            self.draw_button(pygame.Rect(ALGORITHM_BUTTON_X, y_position, BUTTON_WIDTH, BUTTON_HEIGHT), 
                             name, color, WHITE, CORNER_RADIUS)
            y_position += BUTTON_HEIGHT + Y_OFFSET

    def draw_control_buttons(self):
        """Draws control buttons like 'Sort' and 'Reload'."""
        self.draw_button(pygame.Rect(CONTROL_BUTTON_X, BUTTON_START_Y, BUTTON_WIDTH, BUTTON_HEIGHT), 
                         "Sort", BLUE, WHITE, CORNER_RADIUS)
        self.draw_button(pygame.Rect(CONTROL_BUTTON_X, BUTTON_START_Y + BUTTON_HEIGHT + Y_OFFSET, 
                                     BUTTON_WIDTH, BUTTON_HEIGHT), 
                         "Reload", BLUE, WHITE, CORNER_RADIUS)

    def draw_button(self, rect, text, color, text_color, corner_radius):
        """Draws a rounded button with a gradient background and centered text."""
        self.draw_rounded_rect(self.screen, rect, color, corner_radius)
        self.create_gradient_rect(self.screen, color, self.lighten_color(color), rect)
        rendered_text = self.font.render(text, True, text_color)
        self.screen.blit(rendered_text, (rect.x + 10, rect.y + 5))

    def create_gradient_rect(self, window, colour, gradient, target_rect):
        """Creates a gradient effect on a button."""
        colour_rect = pygame.Surface((2, 2))
        pygame.draw.line(colour_rect, colour, (0, 0), (1, 0))
        pygame.draw.line(colour_rect, gradient, (0, 1), (1, 1))
        colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))
        window.blit(colour_rect, target_rect)

    def draw_rounded_rect(self, surface, rect, color, corner_radius):
        """Draws a rectangle with rounded corners."""
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

    def handle_ui_event(self, pos):
        """Handles user interactions with the UI, determining which button was pressed."""
        x, y = pos
        if ALGORITHM_BUTTON_X <= x <= ALGORITHM_BUTTON_X + BUTTON_WIDTH:
            self.handle_algorithm_selection(y)
        elif CONTROL_BUTTON_X <= x <= CONTROL_BUTTON_X + BUTTON_WIDTH:
            self.handle_control_buttons(y)

    def handle_algorithm_selection(self, y):
        """Determines which sorting algorithm button was pressed based on the y-coordinate."""
        for i, algo in enumerate(self.sorting_algorithms.values()):
            button_y = BUTTON_START_Y + (i + 1) * (BUTTON_HEIGHT + Y_OFFSET)
            if button_y <= y <= button_y + BUTTON_HEIGHT:
                self.selected_algorithm = algo
                break

    def handle_control_buttons(self, y):
        """Determines which control button was pressed and triggers the appropriate action."""
        sort_button_y = BUTTON_START_Y
        reload_button_y = BUTTON_START_Y + BUTTON_HEIGHT + Y_OFFSET
        if sort_button_y <= y <= sort_button_y + BUTTON_HEIGHT:
            self.start_sorting()
        elif reload_button_y <= y <= reload_button_y + BUTTON_HEIGHT:
            self.reset_data()

    @staticmethod
    def lighten_color(color):
        """Lightens a given color for aesthetic effects on UI elements."""
        return (color[0], color[1], min(255, color[2] + GRADIENT_LIGHTNESS_INCREASE))