import pygame

def initialize_pygame():
    """Initialize pygame and set up the display."""
    pygame.init()
    width, height = 425, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sorting Algorithm Visualization")
    return screen

def handle_events(visualizer):
    """Handle user input events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            visualizer.handle_ui_event(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                visualizer.start_sorting()
    return True

def update_sorting(visualizer):
    """Update the sorting process if sorting is ongoing."""
    if visualizer.sorting:
        try:
            next(visualizer.sort_gen)
        except StopIteration:
            visualizer.sorting = False

def main_loop(visualizer, clock):
    """Main loop to run the sorting visualization."""
    running = True
    while running:
        clock.tick(480)
        running = handle_events(visualizer)
        update_sorting(visualizer)
        visualizer.draw_data(visualizer.data)
