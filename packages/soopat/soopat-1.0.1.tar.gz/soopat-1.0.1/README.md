## Soopat PDF Downloader

### Installation
```bash
python3 -m pip install soopat
```

### Usage
`register`
```bash
# register an account
soopat register --help

soopat register
soopat register --auto
```

`download`
```bash
# download the pdf
soopat download --help

soopat download -i 202010463344
soopat download -i http://www.soopat.com/Patent/202111607937
soopat download -i 202010463344 -u your_username -p your_password -o out.pdf
```
