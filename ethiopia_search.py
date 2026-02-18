import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from collections import deque
from ethiopia_graph import ETHIOPIA_GRAPH

class EthiopiaSearchNode(Node):
    def __init__(self):
        super().__init__('ethiopia_search_node')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        
        # Graph data manually extracted from Figure 1
        # Graph data imported from ethiopia_graph.py
        self.graph = ETHIOPIA_GRAPH

    def bfs_find_path(self, start, goal):
        """Uninformed search: Breadth-First Search"""
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

    def execute_search(self, start_node, goal_node):
        path = self.bfs_find_path(start_node, goal_node)
        if path:
            self.get_logger().info(f"Path Found: {' -> '.join(path)}")
            # Logic for moving the robot between coordinates would go here
        else:
            self.get_logger().error("No path found between the given states.")

def main(args=None):
    rclpy.init(args=args)
    node = EthiopiaSearchNode()
    
    # Example: Travel from Gambella to Gode
    node.execute_search("Gambella", "Gode")
    
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
