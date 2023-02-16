import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from project.package1 import module1
from project.package1.module2 import func2
from project.package2 import module3
from project.package2.subpackage import module4

if __name__ == '__main__':


    print('func0')
    module1.func1()
    func2()
    module3.func3()
    module4.func4()

def func0() -> None:
    print('func0')
