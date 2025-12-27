import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from collections import deque

class EthiopiaSearchNode(Node):
    def __init__(self):
        super().__init__('ethiopia_search_node')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        
        # Graph data manually extracted from Figure 1
        self.graph = {
            'Gambella': ['Dembi Dollo', 'Gore'],
            'Dembi Dollo': ['Gambella', 'Gimbi'],
            'Gimbi': ['Dembi Dollo', 'Nekemete'],
            'Nekemete': ['Gimbi', 'Ambo', 'Bedelle'],
            'Gore': ['Gambella', 'Tepi', 'Bedelle'],
            'Tepi': ['Gore', 'Bonga', 'Mezan Teferi'],
            'Mezan Teferi': ['Tepi', 'Bonga'],
            'Bonga': ['Tepi', 'Mezan Teferi', 'Dawro', 'Jimma'],
            'Jimma': ['Bonga', 'Bedelle', 'Wolkite'],
            'Bedelle': ['Nekemete', 'Gore', 'Jimma'],
            'Dawro': ['Bonga', 'Wolaita Sodo'],
            'Wolaita Sodo': ['Dawro', 'Arba Minch', 'Hossana'],
            'Arba Minch': ['Wolaita Sodo'],
            'Wolkite': ['Jimma', 'Ambo', 'Worabe', 'Hossana'],
            'Worabe': ['Wolkite', 'Buta Jirra', 'Hossana'],
            'Hossana': ['Wolkite', 'Worabe', 'Wolaita Sodo', 'Shashemene'],
            'Buta Jirra': ['Worabe', 'Batu'],
            'Ambo': ['Nekemete', 'Addis Ababa', 'Wolkite'],
            'Addis Ababa': ['Ambo', 'Debre Birhan', 'Adama'],
            'Debre Birhan': ['Addis Ababa'],
            'Adama': ['Addis Ababa', 'Matahara', 'Batu', 'Assella'],
            'Matahara': ['Adama', 'Awash'],
            'Awash': ['Matahara', 'Chiro'],
            'Chiro': ['Awash', 'Dire Dawa'],
            'Dire Dawa': ['Chiro', 'Harar'],
            'Harar': ['Dire Dawa', 'Babile'],
            'Babile': ['Harar', 'Jigjiga'],
            'Jigjiga': ['Babile', 'Dega Habur'],
            'Dega Habur': ['Jigjiga', 'Kebri Dehar', 'Goba'],
            'Kebri Dehar': ['Dega Habur', 'Gode', 'Sof Oumer'],
            'Gode': ['Kebri Dehar'],
            'Batu': ['Buta Jirra', 'Adama', 'Shashemene'],
            'Shashemene': ['Batu', 'Hossana', 'Hawassa', 'Dodolla'],
            'Hawassa': ['Shashemene', 'Dilla'],
            'Dilla': ['Hawassa'],
            'Assella': ['Adama', 'Assasa'],
            'Assasa': ['Assella', 'Dodolla'],
            'Dodolla': ['Assasa', 'Shashemene', 'Bale'],
            'Bale': ['Dodolla', 'Goba', 'Sof Oumer'],
            'Goba': ['Bale', 'Dega Habur'],
            'Sof Oumer': ['Bale', 'Kebri Dehar']
        }

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
