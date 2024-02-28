package main

import (
	"fmt"
	"sync"
	"time"
)

type MapWithExpiration struct {
	sync.RWMutex
	items map[string]Item
}

type Item struct {
	value interface{}
	timer time.Time
}

func main() {

	m := MapWithExpiration{
		items: make(map[string]Item),
	}
	m.Set("key1", "value1")
	m.Set("key2", "value2")
	go m.DeleteTimeCheck()
	fmt.Println(m.Get("key1"))
	fmt.Println(m.Get("key2"))
	fmt.Println("-----------")
	time.Sleep(time.Second * 2)
	fmt.Println(m.Get("key1"))
	fmt.Println(m.Get("key2"))
	fmt.Println("-----------")
	time.Sleep(time.Second * 2)
	fmt.Println(m.Get("key1"))
	fmt.Println(m.Get("key2"))
	fmt.Println("-----------")
}

func (m *MapWithExpiration) Set(key string, value interface{}) {
	m.Lock()
	defer m.Unlock()
	item := Item{
		value: value,
		timer: time.Now().Add(time.Second * 2),
	}
	m.items[key] = item
}

func (m *MapWithExpiration) Get(key string) (interface{}, bool) {
	m.RLock()
	defer m.RUnlock()
	item, found := m.items[key]
	if !found {
		return nil, false
	}
	return item.value, true
}

func (m *MapWithExpiration) DeleteTimeCheck() { // Можно запихнуть в методы(удаление в вызовах), поможет избавиться от пробуждения каждые секунды.
	for {
		m.Lock()
		for key, item := range m.items {
			if time.Now().After(item.timer) {
				delete(m.items, key)
			}
		}
		m.Unlock()
		time.Sleep(time.Second)
	}
}
