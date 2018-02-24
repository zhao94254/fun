package main

import "fmt"

type Node struct {
	data int
	next *Node
}

func Append(x int) *Node {
	r := Node{data:x, next:nil}
	return &r
}

func buildLink(x int) *Node {
	// 构造一个长度为 x 的链表
	h := &Node{}
	r := h
	for i:=1; i<x;i++{
		h.next = Append(i)
		h = h.next
	}
	return r
}

func Length(h *Node) int {
	// 获取链表长度
	i := 1
	for h.next != nil{
		i++
		h = h.next
	}
	return i
}


func main()  {
	r := buildLink(10)
	fmt.Println(Length(r))
}