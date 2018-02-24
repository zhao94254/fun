package main

import (
	"fmt"
)

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

func printLink(link *Node)  {
	res := ""
	for link.next != nil{
		link = link.next
		str :=  fmt.Sprintf("%d", link.data)
		res += str
		res += "->"
	}
	fmt.Println(res)
}


func Reverse(link *Node) *Node{
	h := &Node{}
	for link != nil {
		rest := link.next
		link.next = h
		h = link
		link = rest
		printLink(rest)
	}
	return h
}

func main()  {
	link := buildLink(10)
	printLink(link)
	r := Reverse(link)
	fmt.Println(Length(r))
	printLink(r)
}