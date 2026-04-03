a = [1,6,3,2,5]
def secondLargestElement(nums):
    nums.sort(reverse=True)
    print(nums)
    max_num = nums[0]
    sec = 0
    for i in nums:
        if i < max_num:
            sec = i
            break
    if sec == 0:
        return -1
    return sec
print(secondLargestElement(a))
print(secondLargestElement([10,10,10,10,10]))