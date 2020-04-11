package main


import (
    "io/ioutil"
    "os"
    "fmt"
    "net/http"
    "math"
    "time"
    "crypto/md5"
    "regexp"
    "strconv"
    "strings"
    "encoding/base64"
)


const (
    DomainDatPath = ".domains.raw"
    DomainDBPath  = ".domains.csv"
    IPDatPath     = ".ips.raw"
    IPDBPath      = ".ips.csv"
)


func httpGet(url string) (string) {
    for i := 0; i <= 10; i++ {
        fmt.Printf("Get [%d] time(s) [%s]\n", i+1, url)
        time.Sleep(time.Duration(i*3) * time.Second)
        resp, err :=   http.Get(url)
        if err != nil {
            continue
        }
        defer resp.Body.Close()
        body, err := ioutil.ReadAll(resp.Body)
        if err != nil {
            panic(err)
        }
        ctx := string(body)
        if ctx != "" {
            return ctx
        }
    }
    os.Exit(2)
    return ""
}


func Md5(ctx string) string {
    return fmt.Sprintf("%x", md5.Sum([]byte(ctx)))
}


func Getmd5File(path string) string {
    _, err := os.Stat(path)
    if err != nil {
        return ""
    }
    ctx, err := ioutil.ReadFile(path)
    if err != nil {return ""}
    return Md5(string(ctx))
}


func SaveingtoFile(ctx string, path string) {
    if ioutil.WriteFile(path ,[]byte(ctx), 0644) == nil {
        fmt.Println("Save to " + path)
    }
}


func GetDomains(ctx string) (domains []string) {
    DecodeCtx, err := base64.StdEncoding.DecodeString(ctx)
    if err != nil {
        panic(err)
    }
    domainList := strings.Split(string(DecodeCtx), "\n")
    for _, line := range domainList {
        flg1 := regexp.MustCompile(
            `^\!|\[|^@@|\d+\.\d+\.\d+\.\d+|^ *$`).MatchString(line)
        flg2 := ! regexp.MustCompile(
            `([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*`).MatchString(line)
        if flg1 || flg2 {continue}
        r, err := regexp.Compile(`([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*`)
        if err != nil {
            panic(err)
        }
        domain := strings.Replace(r.FindString(line), "/", "", -1)
        domains = append(domains, domain)
    }
    return domains
}


func SaveingtoDB(domains []string, DomainDBPath string) {
    var ctx string
    for i, line := range domains {
        ctx += fmt.Sprintf("%d,%s\n", i + 1, line)
    }
    SaveingtoFile(ctx, DomainDBPath)
}


func SaveDomains(ctx string) {
    SaveingtoFile(ctx, DomainDatPath)
    domains := GetDomains(ctx)
    SaveingtoDB(domains, DomainDBPath)
}


func GetIPs(ctx string) (ips []string) {
    ipList := strings.Split(ctx, "\n")
    for _, line := range ipList {
        if regexp.MustCompile(`^ *#`).MatchString(line) {
            continue
        }
        if regexp.MustCompile(`CN\|ipv4`).MatchString(line) {
            lineList := strings.Split(line, "|")
            Num, err := strconv.ParseFloat(lineList[4], 64)
            if err != nil {panic(err)}
            ips = append(ips, fmt.Sprintf("%s/%d",
                lineList[3], 32 - int(math.Log2(Num))))
        }
    }
    return ips
}


func SaveIPs(ctx string) {
    SaveingtoFile(ctx, IPDatPath)
    ips := GetIPs(ctx)
    SaveingtoDB(ips, IPDBPath)
}


func main() {
    var ctx string
    urlDomain := "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"
    ctx = httpGet(urlDomain)
    md5NowDomain := Md5(ctx)
    md5FileDomain := Getmd5File(DomainDatPath)
    if md5NowDomain != md5FileDomain {
        SaveDomains(ctx)
    } else {
        fmt.Println("Domains are not changed.")
    }
    urlIP := "https://ftp.apnic.net/stats/apnic/delegated-apnic-latest"
    ctx = httpGet(urlIP)
    md5NowIP := Md5(ctx)
    md5FileIP := Getmd5File(IPDatPath)
    if md5NowIP != md5FileIP {
        SaveIPs(ctx)
    } else {
        fmt.Println("IPs are not changed.")
    }
}
