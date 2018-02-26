package main

import "fmt"

type tree struct {
	val int
	left, right *tree
}

func build(values []int, start, end int ) *tree {
	if start > end{
		return nil
	}
	root := tree{val:values[(start + end) / 2]}
	root.left = build(values, start, (start+end)/2 -1)
	root.right = build(values, (start+end)/2+1, end)
	return &root
}

func sortedToBst(values []int) *tree {
	return build(values, 0, len(values)-1)
}

func preOrder(values []int, t *tree) []int {
	if t != nil {
		values = append(values, t.val)
		values = preOrder(values, t.left)
		values = preOrder(values, t.right)
	}
	return values

}

func test1(test []int)  {
	lenval := len(test)
	fmt.Println(lenval/2, test[lenval-1])
}

func main()  {
	test := []int{1,2,3,4,5,6,7,8,9}
	tree := sortedToBst(test)
	fmt.Println(preOrder([]int{}, tree))
}