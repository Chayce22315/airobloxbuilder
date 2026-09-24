package main

import (
  "encoding/json"
  "fmt"
)

type capability struct {
  ID string
  Available bool
}

func main() {
  capabilities := []capability{
    {ID: "filesystem", Available: true},
    {ID: "processes", Available: true},
    {ID: "roblox-studio-mcp", Available: false},
  }
  data, _ := json.MarshalIndent(capabilities, "", "  ")
  fmt.Println(string(data))
}
