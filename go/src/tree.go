package main

import (
	"fmt"
)

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

func max(a, b int) int {
	if a > b{
		return a
	}
	return b
}

func treeHeight(t *tree) int {
	if t == nil{
		return 0
	}
	return max(treeHeight(t.left),  treeHeight(t.right)) + 1
}

// 不用指针的方式
func levelOrder(t *tree, level int, res [][]int) [][]int{
	if t != nil{
		if len(res) < level+1{
			res = append(res, []int{})
		}
		res[level] = append(res[level], t.val)
		res = levelOrder(t.left, level+1, res)
		res = levelOrder(t.right, level+1, res)
	}
	return res
}

func printLevelOrder(t *tree)  {
	res := [][]int{}
	res = levelOrder(t, 0, res)
	for _, v := range res{
		fmt.Println(v)
	}
}

// 使用指针的方式. 在python中传入一个数组也类似于使用了指针， 相当于传入的是一个引用
// 函数内将传入的改变了，对应的引用的地址的值也改变了。

func levelOrderPoint(t *tree, level int, res *[][]int){
	if t != nil{
		if len(*res) < level+1{
			*res = append(*res, []int{})
		}
		(*res)[level] = append((*res)[level], t.val)
		levelOrderPoint(t.left, level+1, res)
		levelOrderPoint(t.right, level+1, res)
	}
}

func printOrderPoint(t *tree)  {
	res := [][]int{}
	levelOrderPoint(t, 0, &res)
	for _, v := range res{
		fmt.Println(v)
	}
}


func main()  {
	test := []int{1,2,3,4,5,6,7,8,9}
	tree := sortedToBst(test)
	fmt.Println(preOrder([]int{}, tree))
	fmt.Println(treeHeight(tree))
	//printLevelOrder(tree)
	printOrderPoint(tree)
}