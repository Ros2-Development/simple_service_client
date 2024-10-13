import rclpy
from rclpy.node import Node
from simple_msgs.srv import AddTwoInt
import sys


class SimpleServiceClient(Node):
    def __init__(self, a, b):
        super().__init__("simple_service_client")

        self.client_ = self.create_client(AddTwoInt, "add_two_int")

        while not self.client_.wait_for_service(timeout_sec = 1.0):
            self.get_logger().info("Service not available,waiting again ...")

        self.request_ = AddTwoInt.Request()
        self.request_.a = a
        self.request_.b = b

        self.future_ = self.client_.call_async(self.request_) # this will act as a variable once the value is retrived from the server
        self.future_.add_done_callback(self.responseCallback)  #to terminate once the value is received 

    def responseCallback(self, future):
        self.get_logger().info(f"service Response {future.result().sum}")







def main():
    rclpy.init()

    if len(sys.argv) != 3:
        print("Wrong number of arguments! Usage: simple_Service_client A B")
        return -1
    

    simple_service_client = SimpleServiceClient(int(sys.argv[1]), int(sys.argv[2]))
    rclpy.spin(simple_service_client)
    simple_service_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()