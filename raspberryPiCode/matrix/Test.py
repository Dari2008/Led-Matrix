from Test2 import Test2 as Test2
import threading as threading

class S:
    @staticmethod
    def start():
        s = Test2()
        s.factory("TestPlugin")


threading.Thread(target=S.start, daemon=True).start()

