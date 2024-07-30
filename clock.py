import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime, timedelta
from PIL import Image

def draw_clock(hour, minute, save_path):
    # Create figure and axis
    fig, ax = plt.subplots()

    # Draw the black clock face
    clock_face = plt.Circle((0.5, 0.5), 0.45, color='black', ec='white', lw=3)
    ax.add_artist(clock_face)

    # Draw the hour ticks
    for i in range(12):
        angle = 2 * np.pi * i / 12
        x_outer = 0.5 + 0.42 * np.sin(angle)
        y_outer = 0.5 + 0.42 * np.cos(angle)
        x_inner = 0.5 + 0.32 * np.sin(angle)
        y_inner = 0.5 + 0.32 * np.cos(angle)
        ax.plot([x_inner, x_outer], [y_inner, y_outer], color='gray', lw=3)
    # Draw the minute ticks
    for i in range(60):
        if i % 5 != 0:
            angle = 2 * np.pi * i / 60
            x_outer = 0.5 + 0.42 * np.sin(angle)
            y_outer = 0.5 + 0.42 * np.cos(angle)
            x_inner = 0.5 + 0.40 * np.sin(angle)
            y_inner = 0.5 + 0.40 * np.cos(angle)
            ax.plot([x_inner, x_outer], [y_inner, y_outer], color='gray', lw=1)

    # Calculate hand angles
    hour_angle = 2 * np.pi * ((hour % 12) + minute / 60) / 12
    minute_angle = 2 * np.pi * minute / 60

    # Draw the hour hand
    hour_hand = plt.Line2D((0.5, 0.5 + 0.2 * np.sin(hour_angle)),
                           (0.5, 0.5 + 0.2 * np.cos(hour_angle)),
                           color='white', lw=5)
    ax.add_line(hour_hand)

    # Draw the minute hand
    minute_hand = plt.Line2D((0.5, 0.5 + 0.3 * np.sin(minute_angle)),
                             (0.5, 0.5 + 0.3 * np.cos(minute_angle)),
                             color='white', lw=3)
    ax.add_line(minute_hand)

    

    # Set the plot limits and aspect
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')

    # Save the figure as a JPG
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0, facecolor='black', format='jpg')
    plt.close(fig)

    

def generate_clock_images():
    # Change the output directory to clock directory
    output_dir = os.path.join(os.getcwd(), 'clock')
    os.makedirs(output_dir, exist_ok=True)

    current_time = datetime.strptime('01:00', '%H:%M')
    end_time = current_time + timedelta(hours=12)
    while current_time < end_time:
        hour = current_time.hour
        minute = current_time.minute
        filename = current_time.strftime('%H%M') + ".jpg"
        save_path = os.path.join(output_dir, filename)
        draw_clock(hour, minute, save_path)
        current_time += timedelta(minutes=1)
        print(f"Generated {filename}")

if __name__ == "__main__":
    generate_clock_images()
