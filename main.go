package main

import (
	"fmt"
)

func main() {
	s:=[]int{1,0}
	fmt.Println(missingNumber(s))
}

func missingNumber(nums []int) int {
	result:=-1
	for i:= 0 ; i< len(nums) ; i++ {
		if nums[i]>=result && result+1 >= nums[i]{
			result++
			i = 0
		}
	}
	return result
}