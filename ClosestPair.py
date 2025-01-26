import math
import matplotlib.pyplot as plt

# Helper function to calculate the distance between two points
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Brute force solution for small inputs (<= 3 points)
def brute_force(points):
    min_dist = float('inf')
    closest_pair = None
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            d = distance(points[i], points[j])
            if d < min_dist:
                min_dist = d
                closest_pair = (points[i], points[j])
    return min_dist, closest_pair

# Function to find the closest points in the strip
def closest_in_strip(strip, d, best_pair):
    min_dist = d
    strip.sort(key=lambda x: x[1])  # Sort strip according to y-coordinate
    
    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and (strip[j][1] - strip[i][1]) < min_dist:
            d = distance(strip[i], strip[j])
            if d < min_dist:
                min_dist = d
                best_pair = (strip[i], strip[j])
            j += 1
    
    return min_dist, best_pair

# Main recursive function using divide and conquer
def closest_pair_recursive(points_sorted_by_x):
    n = len(points_sorted_by_x)
    
    # Base case: If there are 2 or 3 points, use brute force
    if n <= 3:
        return brute_force(points_sorted_by_x)
    
    # Divide the points into two halves
    mid = n // 2
    mid_point = points_sorted_by_x[mid]
    
    # Recursively find the smallest distance in left and right halves
    d_left, pair_left = closest_pair_recursive(points_sorted_by_x[:mid])
    d_right, pair_right = closest_pair_recursive(points_sorted_by_x[mid:])
    
    # Find the smaller of the two distances
    if d_left < d_right:
        d = d_left
        best_pair = pair_left
    else:
        d = d_right
        best_pair = pair_right
    
    # Build a list of points that lie within distance 'd' from the midline
    strip = [point for point in points_sorted_by_x if abs(point[0] - mid_point[0]) < d]
    
    # Find the closest points in the strip
    return closest_in_strip(strip, d, best_pair)

# Main function to solve the closest pair problem
def closest_pair(points):
    # Sort points according to x-coordinate
    points_sorted_by_x = sorted(points, key=lambda x: x[0])
    
    # Start the recursive process
    return closest_pair_recursive(points_sorted_by_x)

# Visualization function
def plot_points_and_pair(points, closest_pair):
    # Unpack the closest pair
    (p1, p2) = closest_pair
    
    # Scatter plot for all points
    plt.scatter([p[0] for p in points], [p[1] for p in points], color='blue')
    
    # Highlight the closest pair in red
    plt.scatter([p1[0], p2[0]], [p1[1], p2[1]], color='red')
    
    # Draw a line between the closest pair
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color='red', linestyle='--')
    
    # Add labels to the points
    for p in points:
        plt.text(p[0], p[1], f'({p[0]}, {p[1]})', fontsize=9, ha='right')

    # Set title and labels
    plt.title('Closest Pair of Points')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    
    # Add grid
    plt.grid()
    
    # Show the plot
    plt.show()

def read_points_from_file(file_path):
    points = []
    
    # Open the file for reading
    with open(file_path, 'r') as file:
        for line in file:
            # Strip any surrounding whitespace/newlines and split the line into x and y
            x, y = line.strip().split()
            
            # Convert x and y to float or int and create a tuple
            point = (float(x), float(y))
            
            # Append the tuple to the points list
            points.append(point)
    
    return points

try:
    points = read_points_from_file('points.txt')
except FileNotFoundError:
    print("File not found. Please make sure the file exists in the current directory.")
    exit()

# Find the closest pair and their distance
min_dist, closest_pair = closest_pair(points)
print(f"The closest pair is: {closest_pair} with a distance of: {min_dist}")

# Plot the points and the closest pair
plot_points_and_pair(points, closest_pair)
