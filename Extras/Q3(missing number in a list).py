def missingNumber(nums):
    nums.sort()
    for i in range(len(nums)):
        if nums[i] != nums[i] + 1:
            return nums[i]+2
    else:
        return (len(nums) - 1) + 1

print(missingNumber([1,2,3,5]))