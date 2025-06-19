# gauhop
tools like [gau](https://github.com/lc/gau) are great for finding endpoints, but they fall short on non-production targets like dev/staging/uat — since those often are not indexed yet. **gauhop** hopes to solve this by running gau across all known subdomains of one or more root domains associated with your in-scope target. it then maps the discovered endpoints to the target domain, giving you a better shot at finding reused paths, sensitive files, or hidden directories.

## requirements
- python 3
- [gau](https://github.com/lc/gau) (must be in your system's `PATH`)

### installation
```sh
git clone https://github.com/ph5i/gauhop.git
cd gauhop
```

### usage
grab endpoints from all subdomains of the root domain `example.com` and probe them on your in-scope target `dev.example.biz` using `httpx`:

```sh
python3 gauhop.py -r example.com -t dev.example.biz | httpx -silent -title -ct -cl
```

for multiple root domains `example.com` and `example.org` and testing them on your in-scope target `dev.example.biz`:
```sh
python3 gauhop.py -r example.com,example.org -t dev.example.biz | httpx -silent -title -ct -cl
```

to save the URLs to a file for testing later:
```
python3 gauhop.py -r example.com -t dev.example.com -o urls.txt
```

### todo
- add deduplication support
- add option to extract solely the raw endpoints, e.g., instead of `http://example.com/foo/bar.png` --> `/foo/bar.png`
- benchmark against manual flow

### license
---
this tool is licensed under the [MIT](https://opensource.org/license/MIT) license.
