try:
    from ethiopia_search import EthiopiaSearchNode
    from ethiopia_graph import ETHIOPIA_GRAPH
    
    # Mocking rclpy.node.Node since we might not want to init a full node
    # Actually, let's just inspect the class or try to instantiation if rclpy is available
    import rclpy
    rclpy.init()
    node = EthiopiaSearchNode()
    
    print("Graph loaded keys:", len(node.graph.keys()))
    print("Expected keys:", len(ETHIOPIA_GRAPH.keys()))
    
    assert node.graph == ETHIOPIA_GRAPH
    print("Graph verification PASSED.")
    
    # Test path finding
    path = node.bfs_find_path('Gambella', 'Gode')
    print("Path found:", path)
    assert path is not None
    assert path[0] == 'Gambella'
    assert path[-1] == 'Gode'
    print("Path verification PASSED.")
    
    node.destroy_node()
    rclpy.shutdown()

except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
