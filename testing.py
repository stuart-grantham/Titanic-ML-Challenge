import datetime as date 

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        #loop through string
        #build list of non repeating characters 
        #note length when it finishes
        longest_dict = {}
        current_dict = {}
        for i in s:
            if i in current_dict.keys():
                if len(longest_dict) < len(current_dict):
                    longest_dictionary = current_dict
                else:
                    current_dict = {}
            else:
                current_dict[i] = True
        return len(longest_dict)
            
new_solution = Solution()
new_solution.lengthOfLongestSubstring("abcabcbb")