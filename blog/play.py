import operator
import math

class MyClass():

    def __init__(self, input1):
        self.input1 = input1
        # self.input2 = input2



list_of_instances = []
for i in range(-3,3):
    list_of_instances.append(MyClass(math.fabs(i)))


for instance in list_of_instances:
    print instance.input1
print
list_of_instances = sorted(list_of_instances, key=operator.attrgetter('input1'))
for instance in list_of_instances:
    print instance.input1


# print sorted_list
