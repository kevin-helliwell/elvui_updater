package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strings"
	"time"
)

// Sets necessary parameters for program to run

const addonDir, downloadDir, apiUrl, sourceUrl string = "C:/Program Files (x86)/World of Warcraft/_retail_/Interface/Addons", "C:/Users/kbh78/Downloads", "https://api.github.com/repos/tukui-org/ElvUI/branches/main", "https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip"

func main() {
	fmt.Println("Hello, World!")
	getVersionNumber()
	getZipFileName()
}

type Todo struct {
	Name string `json:"name"`
	Commit struct {
		Commit struct {
			Message string `json:"message"`
		}
	}	
}

func getVersionNumber() (string) {
start := time.Now()
resp, err := http.Get(apiUrl)
if err != nil {
	log.Fatalln(err)
}
defer resp.Body.Close()
bodyBytes, _ := ioutil.ReadAll(resp.Body)
// Convert response body to Todo struct
// var todoStruct Todo
todoStruct := Todo{}
jsonErr := json.Unmarshal(bodyBytes, &todoStruct)
if jsonErr != nil {
	log.Fatal(jsonErr)
  }
message := todoStruct.Commit.Commit.Message
end := time.Now()
fmt.Printf("Version number %v Completed in %v",message, end.Sub(start))
return message
}

func getZipFileName() (string) {
	urlSplitList := strings.Split(apiUrl,"/")
	zipFileName := urlSplitList[5]+"-"+urlSplitList[7]
	return zipFileName
}

func checkLocalVersion() {}

func getSourceZipData() {}

func getZipFilePath() {}

func manageZip() {}

func managePaths() {}
