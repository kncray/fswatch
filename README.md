# fswatch

fswatch는 지정된 경로의 파일시스템의 파일 변화를 모니터링하여 지정된 모듈로 전달합니다.

* 지정된 경로

    `--target`로 지정된 디렉토리 경로입니다. 디렉토리 내부의 모든 파일의 변화를 감시합니다. 


*  지정된 모듈

    `--module`로 지정된 함수 경로입니다. 지정된 모듈로 모니터링 결과를 전달합니다.


## 사용법

mymodule.py의 myfunction에 변경 내역을 전달합니다.

*주의* 변경 내역 전달 전 기존 내역이 일괄 전달됩니다. 이것을 막으려면 `--only-changes` 옵션을 부가합니다.

```bash
pip install watchdog
```

```python
# cat mymodule.py
def myfunction(data):
    print(data, end='')
```

```bash
python fswatch.py --target=./mydir/ --module=mymodule.myfunction
```

변경 내역만 전달합니다.

```bash
python fswatch.py --target=./mydir/ --module=mymodule.myfunction --only-changes
```

### 변경 내역을 HTTP로 전달하기

`./tmpdir/` 내부에 위치한 파일이 아래와 같은 컬럼으로 구성된 csv 파일이고 새로운 라인이 지속적으로 추가된다고 가정합니다.

```csv
timestamp,auth_key,post_body,is_valid
2024-01-01T11:00:00+09,qkfienvier,{"abc":"def"},true
```

example2.py
```python
import csv

import urllib.parse
import urllib.request

from os import getenv

ENTRYPOINT = getenv('ENDPOINT')
HTTP_PROXY = getenv('HTTP_PROXY')
HTTPS_PROXY = getenv('HTTP_PROXY', HTTP_PROXY)


def listen(contents):
    for row in csv.reader(contents.splitlines()):
        print(row)

        timestamp, auth_key, post_body, *etc = row

        req = urllib.request.Request(
            ENTRYPOINT,
            data=post_body.encode(),
            headers={
                'Content-Type': 'application/json'
            },
        )
        req.set_proxy(HTTP_PROXY, 'http')
        req.set_proxy(HTTP_PROXY, 'https')

        with urllib.request.urlopen(req, timeout=10) as response:
            result = response.read()
            print(result.decode())
```


```bash
python fswatch.py --target=./mydir/ --module=example2.listen --only-changes
```
