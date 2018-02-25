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
	h := new(Node)
	r := h
	for i:=1; i<x;i++{
		if h.data == 0{
			h.data = i
		}else {
			h.next = Append(i)
			h = h.next
		}
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
	if link == nil{
		return
	}
	for link.next != nil{
		str :=  fmt.Sprintf("%d", link.data)
		res += str
		res += "->"
		link = link.next
	}
	fmt.Println(res)
}

func Reverse(link *Node) *Node{
	h := new(Node)
	for link != nil {
		rest := link.next
		link.next = h
		h = link
		link = rest
	}
	return h
}

type mapfunc func(int) int
type filterfunc func(int) bool

func MapLink(f mapfunc, link *Node) *Node {
	cur := link
	for cur.next != nil  {
		cur.data = f(cur.data)
		cur = cur.next
	}
	return link
}

func FilterLink(f filterfunc, link *Node) *Node  {
	if link == nil{
		return nil
	}else {
		filtered := FilterLink(f, link.next)
		if f(link.data){
			return &Node{link.data, filtered}
		}else{
			return filtered
		}
	}
}

func square(x int) int  {
	return x*x
}

func main()  {
	link := buildLink(10)
	printLink(link)
	r := Reverse(link)
	printLink(r)
	r = MapLink(square, r)
	printLink(r)
	// 匿名函数使用
	x := MapLink(func(i int) int {
		return i*3
	}, r)
	printLink(x)
	r = FilterLink(func(i int) bool {
		return i%2==1
	}, r)
	printLink(r)
}