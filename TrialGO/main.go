package main

import (
	"fmt"
	"sort"
)

func main() {
	var tyty = [][]int{}
	tyty = append(tyty, []int{3, 1}, []int{9, 0}, []int{1, 0}, []int{1, 4}, []int{5, 3}, []int{8, 8})
	fmt.Println(maxWidthOfVerticalArea(tyty))
}
func maxWidthOfVerticalArea(points [][]int) int {
	sort.Slice(points, func(i, j int) bool {
		return points[i][0] < points[j][0]
	})
	var max int
	for i := 1; i < len(points); i++ {
		if points[i][0] > points[i-1][0] && max < points[i][0] - points[i-1][0]{
			max = points[i][0] - points[i-1][0]
		}
	}
	return max
}
