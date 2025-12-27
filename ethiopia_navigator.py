import rclpy
import time
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from collections import deque
from ethiopia_graph import ETHIOPIA_GRAPH
from city_coordiantes import CITY_COORDS

class EthiopiaNavigator(Node):
    def __init__(self):
        super().__init__('ethiopia_navigator')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.graph = ETHIOPIA_GRAPH

    def bfs_find_path(self, start, goal):
        queue = deque([[start]])
        visited = {start}
        while queue:
            path = queue.popleft()
            node = path[-1]
            if node == goal:
                return path
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        return None

    def move_to(self, x_goal, y_goal):
        twist = Twist()
        rate = 10  # Hz
        x, y = 0.0, 0.0  # robot starting position (for simplicity)
        while True:
            dx = x_goal - x
            dy = y_goal - y
            distance = math.sqrt(dx**2 + dy**2)
            if distance < 0.1:
                break
            angle = math.atan2(dy, dx)
            twist.linear.x = min(0.5, distance)
            twist.angular.z = 0.0
            self.publisher_.publish(twist)
            rclpy.spin_once(self, timeout_sec=0.1)
            x += 0.05 * math.cos(angle)
            y += 0.05 * math.sin(angle)
        twist.linear.x = 0.0
        self.publisher_.publish(twist)

    def travel_path(self, path):
        if not path:
            self.get_logger().error("No path found")
            return
        self.get_logger().info(f"Path Found: {' -> '.join(path)}")
        for city in path:
            self.get_logger().info(f"Moving to {city}")
            x, y = CITY_COORDS[city]
            self.move_to(x, y)
            time.sleep(0.5)

def main(args=None):
    rclpy.init(args=args)
    node = EthiopiaNavigator()
    start_city = "Gambella"
    goal_city = "Gode"
    path = node.bfs_find_path(start_city, goal_city)
    node.travel_path(path)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
