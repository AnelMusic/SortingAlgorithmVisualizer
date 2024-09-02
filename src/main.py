import pygame
from visualizer import SortVisualizer
from pygame_setup import initialize_pygame, main_loop

def main():
    """Main function to set up and run the visualizer."""
    screen = initialize_pygame()
    visualizer = SortVisualizer(screen)
    clock = pygame.time.Clock()
    main_loop(visualizer, clock)
    pygame.quit()

if __name__ == "__main__":
    main()
