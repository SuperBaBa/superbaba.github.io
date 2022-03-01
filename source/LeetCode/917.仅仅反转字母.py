#
# @lc app=leetcode.cn id=917 lang=python3
#
# [917] 仅仅反转字母
#

# @lc code=start
class Solution:
    def reverseOnlyLetters(self, s: str) -> str:
        letter_list = []
        for ch in s:
            if ord(ch) >= 65 and ord(ch) <= 90:
                letter_list.append(ch)
            if ord(ch) >= 97 and ord(ch) <= 122:
                letter_list.append(ch)
        i = 1
        reversed_str = ''
        for index, ch in enumerate(s):
            if (ord(ch) >= 65 and ord(ch) <= 90) or (ord(ch) >= 97 and ord(ch) <= 122):
                reversed_str += letter_list[len(letter_list)-i]
                i+=1
            else:
                reversed_str += ch
        return reversed_str

class Solution1:
    def reverseOnlyLetters(self, s: str) -> str:
        ans = list(s)
        left, right = 0, len(ans) - 1
        while True:
            while left < right and not ans[left].isalpha():  # 判断左边是否扫描到字母
                left += 1
            while right > left and not ans[right].isalpha():  # 判断右边是否扫描到字母
                right -= 1
            if left >= right:
                break
            ans[left], ans[right] = ans[right], ans[left]
            left += 1
            right -= 1
        return ''.join(ans)

# @lc code=end
if __name__ == "__main__":
    solution = Solution()
    solution.reverseOnlyLetters("ab-cd")
    



