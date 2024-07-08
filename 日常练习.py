from types import new_class

#
# 代码中的类名、方法名、参数名已经指定，请勿修改，直接返回方法规定的值即可
#
#
# @param nums int整型一维数组
# @return int整型一维数组
#
class Number:
    def __init__(self, value, time):
        self.value = value
        self.time = time
    
    def comp(self,number):
        if(self.value == number.value and self.time == number.time):
            return True
        else:
            return False
    
    def addone(self):
        self.time += 1
    
    def check(self):
        if(self.time == 1):
            return True
        else:
            return False

class Solution:
    def hash(self, number):
        return number % 503

    def FindNumsAppearOnce(self, nums: List[int]):
         # 创建一个包含 504 个 None 元素的列表
        ans = [-1, -1]
        num = Number(0, 0)
        hash_table = [num]*504
       
       
        for number in nums:
            index = self.hash(number)
            if hash_table[index].comp(num) == True:
                numm = Number(number, 1)
                hash_table[index] = numm
            elif hash_table[index].value == number:
                hash_table[index].addone()
            else:
                a = 0
                while(hash_table[index].value != number and hash_table[index].value != 0):
                    index = (index + 1) % 504
                if(hash_table[index].comp(num) == True):
                    num = Number(number, 1)
                    hash_table[index] = num
                else:
                    hash_table[index].addone()
        a = 0
        b = 0
           
        while(b < 503):
            if(hash_table[b].check() == True):
                ans[a] = hash_table[b].value
                a+=1
                    
            b+=1
        if(ans[0] > ans[1]):
            tmp = ans[0]
            ans[0] =ans[1]
            ans[1] = tmp



        # 返回结果
        return ans
