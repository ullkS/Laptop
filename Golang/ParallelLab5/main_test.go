package main

import (
	"testing"
	"time"
)

func TestMapWithExpiration(t *testing.T) {
	m := MapWithExpiration{
		items: make(map[string]Item),
	}
	m.Set("key1", "value1")
	m.Set("key2", "value2")

	// Проверяем начальные значения
	value, found := m.Get("key1")
	if !found {
		t.Errorf("Ожидалось, что key1 будет найден")
	}
	if value != "value1" {
		t.Errorf("Ожидалось значение value1, получено %v", value)
	}

	value, found = m.Get("key2")
	if !found {
		t.Errorf("Ожидалось, что key2 будет найден")
	}
	if value != "value2" {
		t.Errorf("Ожидалось значение value2, получено %v", value)
	}

	// Ждем истечения времени
	time.Sleep(time.Second * 2)

	// Проверяем, что значения истекли
	_, found = m.Get("key1")
	if found {
		t.Errorf("Ожидалось, что key1 будет истекшим")
	}

	_, found = m.Get("key2")
	if found {
		t.Errorf("Ожидалось, что key2 будет истекшим")
	}
}
