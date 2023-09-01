#
# @lc app=leetcode.cn id=1 lang=python3
#
# [1] 两数之和
#

# @lc code=start
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        m = {}
        for (index, item) in enumerate(nums):
            other = target - nums[index]
            if other in m.keys():
                index_list = [index, m[other]]
                index_list.sort()
                return index_list
            m[nums[index]] = index
        return []
# @lc code=end


solution = Solution()
nums = [2, 7, 11, 15]
target = 9
reuslt = solution.twoSum(nums, target)
print(reuslt)
