package main

import (
	"net/http"
	"fmt"
	"bufio"
	"os"
	"strings"
	"github.com/fatih/color"
	"io/ioutil"
	"encoding/json"
	"net/url"
	"time"
)

var server_url, auth string

func main() {
	cool_art()
	server_url = "127.0.0.1:6666"
	for true {
		get_input()
	}
}

func get_input() {
	reader := bufio.NewReader(os.Stdin)

	prompt := color.New(color.FgCyan, color.Bold)
	prompt.Print("➜ ")
	text, _ := reader.ReadString('\n')

	switch text = strings.TrimSuffix(text, "\n"); text {
	
	case "help" :
		get_help()
	
	case "login" :
		info := color.New(color.FgMagenta, color.Bold)
		info.Print("Enter username : ")
		username, _ := reader.ReadString('\n')
		username = strings.TrimSuffix(username, "\n")
		info.Print("Enter password : ")
		password, _ := reader.ReadString('\n')
		password = strings.TrimSuffix(password, "\n")
		
		login(username, password)

	case "flag":
		warn := color.New(color.FgRed, color.Bold)
		warn.Println("forbiden")
		get_flag()

	case "hello":
		say_hello()

	case "ping":
		ping()

	case "secret":
		fmt.Println("0x41414141 is 1337")

	case "exit", "quit":
		red := color.New(color.FgRed, color.BgWhite)
		
		red.Println("bye")
		os.Exit(0)

	default :
		warn := color.New(color.FgRed).Add(color.Underline) 
		warn.Println("invalid input provided")
	}
}

func ping() {
	resp, err := http.Get(fmt.Sprintf("http://%s/ping", server_url))
	if err != nil {
		fmt.Println(err)
	}
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)
	}
	
	var result map[string]interface{}
	if jsonErr := json.Unmarshal(body, &result);jsonErr != nil {
		fmt.Println("woops an error occured please try again")
	}
	
	fmt.Println(result["message"])
}

func login(_user, _pass string) {
	data := url.Values {
		"username": {_user},
		"password": {_pass},
	}

	resp, err := http.PostForm(fmt.Sprintf("http://%s/login", server_url), data)

	if err != nil {
		fmt.Println("please try to login later")
	}
	var res map[string]interface{}

	json.NewDecoder(resp.Body).Decode(&res)

	if res["code"].(float64) != 200 {
		fmt.Println("bad credentials were supplied")
	}else {
		auth = res["token"].(string)
	}
}

func say_hello() {
	client := &http.Client{
		//CheckRedirect: ,
	}
	req, err := http.NewRequest("GET", fmt.Sprintf("http://%s/auth/hello", server_url), nil)
	if err != nil {
		fmt.Println(err)
	}
	req.Header.Add("Authorization", fmt.Sprintf("Bearer %s", auth))
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
	}
	var res map[string]interface{}

	json.NewDecoder(resp.Body).Decode(&res)
	if res["code"] != nil{
		fmt.Println("erorr please login again")
	}else {
		fmt.Println(res["text"])
	}
}

func get_flag() {
	client := &http.Client{
		//CheckRedirect: ,
	}
	req, err := http.NewRequest("GET", fmt.Sprintf("http://%s/auth/flag", server_url), nil)
	if err != nil {
		fmt.Println(err)
	}
	req.Header.Add("Authorization", fmt.Sprintf("Bearer %s", auth))
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
	}
	var res map[string]interface{}

	json.NewDecoder(resp.Body).Decode(&res)
	if res["code"] != nil{
		fmt.Println("erorr please login again")
	}else {
		fmt.Println(res["flag"])
	}
}

func cool_art() {
	art := `
	
	▄████▄   ██▓     ██▓    ▄▄▄▄    ██▀███   ▒█████   █     █░  ██████ ▓█████  ██▀███  
	▒██▀ ▀█  ▓██▒    ▓██▒   ▓█████▄ ▓██ ▒ ██▒▒██▒  ██▒▓█░ █ ░█░▒██    ▒ ▓█   ▀ ▓██ ▒ ██▒
	▒▓█    ▄ ▒██░    ▒██▒   ▒██▒ ▄██▓██ ░▄█ ▒▒██░  ██▒▒█░ █ ░█ ░ ▓██▄   ▒███   ▓██ ░▄█ ▒
	▒▓▓▄ ▄██▒▒██░    ░██░   ▒██░█▀  ▒██▀▀█▄  ▒██   ██░░█░ █ ░█   ▒   ██▒▒▓█  ▄ ▒██▀▀█▄  
	▒ ▓███▀ ░░██████▒░██░   ░▓█  ▀█▓░██▓ ▒██▒░ ████▓▒░░░██▒██▓ ▒██████▒▒░▒████▒░██▓ ▒██▒
	░ ░▒ ▒  ░░ ▒░▓  ░░▓     ░▒▓███▀▒░ ▒▓ ░▒▓░░ ▒░▒░▒░ ░ ▓░▒ ▒  ▒ ▒▓▒ ▒ ░░░ ▒░ ░░ ▒▓ ░▒▓░
	  ░  ▒   ░ ░ ▒  ░ ▒ ░   ▒░▒   ░   ░▒ ░ ▒░  ░ ▒ ▒░   ▒ ░ ░  ░ ░▒  ░ ░ ░ ░  ░  ░▒ ░ ▒░
	░          ░ ░    ▒ ░    ░    ░   ░░   ░ ░ ░ ░ ▒    ░   ░  ░  ░  ░     ░     ░░   ░ 
	░ ░          ░  ░ ░      ░         ░         ░ ░      ░          ░     ░  ░   ░     
	░                             ░                                                     
	`
	scanner := bufio.NewScanner(strings.NewReader(art))
	warn := color.New(color.FgRed, color.Bold)

	for scanner.Scan() {
		time.Sleep(160 * time.Millisecond)
		warn.Println(scanner.Text())
	}
}


func get_help() {
	help := color.New(color.FgGreen, color.Bold)
	help.Println("help page :")
	help_info := `- login 
- hello 
- ping
- flag
- exit`

	scanner := bufio.NewScanner(strings.NewReader(help_info))
	for scanner.Scan() {
		time.Sleep(110 * time.Millisecond)
		help.Println(scanner.Text())
	}
}