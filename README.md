# M6-6 Smart Lock passcode generator
A passcode generator for M6-6 Smart Lock. M6-6 智能锁动态密码生成器。

#### Official manual / 官方说明书
https://ncstatic.clewm.net/rsrc/2019/1113/11/e56e8c5920f9aa382abd492f32631ad6.png
([archive](https://web.archive.org/web/20200528172830/https://ncstatic.clewm.net/rsrc/2019/1113/11/e56e8c5920f9aa382abd492f32631ad6.png))

or https://h5.clewm.net/?url=qr61.cn/o26ijp/qAYI9Ls&hasredirect=1
([archive](https://archive.is/BoUgJ))

#### Official passcode generator (in [WeChat](https://www.wechat.com/)) / 官方微信小程序
`云智锁动态密码工具V1` (appid: wx0d023f3be2b94298)

## Dependency / 依赖
#### `cryptography`

* install with `pip`
```
$ pip install cryptography
```

## Usage / 用法
* Generate a one-time passcode (valid in 3 minutes) / 生成临时密码（有效期 3 分钟）
```
$ python3 generate_code.py <secret>
```
* Generate a long-term passcode (valid until a custom date) / 生成长期密码（自定义有效期）
```
$ python3 generate_code.py <secret> <year> <month> <day> <hour>
```

`secret`: The 8-digit pairing code you entered into the lock / 8位数字配对码

`year`: 2000 to 2099 / 2000 至 2099

`hour`: 0 or 12 / 0 或 12

### Examples / 例子
```
$ python3 generate_code.py 12345678
```
```
$ python3 generate_code.py 12345678 2020 12 31 12
```
```
$ python3 generate_code.py 12345678 2050 6 15 0
```
