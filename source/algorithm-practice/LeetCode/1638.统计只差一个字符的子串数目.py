#
# @lc app=leetcode.cn id=1638 lang=python3
#
# [1638] 统计只差一个字符的子串数目
#


# @lc code=start

class Solution:
    def countSubstrings(self, s: str, t: str) -> int:
        """
        根据题目
        """
        answer = 0
        for i in range(len(s)):
            for j in range(len(t)):
                k = 0
                diff = 0
                while i + k < len(s) and j + k < len(t):
                    if s[i + k] != t[j + k]:
                        diff += 1
                    if diff == 1:
                        answer += 1
                    if s[i + k] == t[j + k]:
                        break
                    k += 1
        return answer


# @lc code=end

if __name__ == '__main__':
    arry = []
    for i in range(5):
        arry.append(i)
        print(arry)

    # 测试上方方法
    solution = Solution()
    result1 = solution.countSubstrings('ab', 'baba')
    print(result1)