# 경제지표 크롤링

매일 23:00:00 마다 데이터 수집(crawling) 및 INSERT 하는 프로그램  

# 크롤링 대상

- 한국은행 (거시지표 위주)
  - 금리(한국, 미국, 일본)
  - 환율(한국, 미국, 일본)
  - KOSPI, 다우존스 종합주가지수
  - 금 거래가 (월 평균)
  - 채권... (채권 관련 공부 필요...)
- KRX
  - KOSPI 등록기업 리스트 (월별)
  - KOSDAQ 등록기업 리스트 (월별)
  - 국내 주식 재무제표 주요지표 (PER, PBR, 주당순이익, etc) 

# 초기설정

```bash
# virtualenv가 설치되어 있지 않다면 pip install virtualenv
$ virtualenv indicator

$ source activate.sh
$ pip install -r requirements.txt
```



## selenium 설정

KOSPI, KOSDAQ 등록 기업 리스트의 경우 KRX의 데이터를 조회해 가져오는데 도저히 API로 해결이 안된다. 이런 이유로 셀레늄(Selenium)을 이용해 크롤링을 하는 방식을 선택했다. 단순히 

- csv 파일을 내려받고 (셀레늄, Selenium 이용)
- panadas로 읽어들인다.

와 같은 절차를 사용하면 된다. 셀레늄(Selenium)설치 과정은 아래와 같다.

```bash
$ source activate.sh
$ pip install selenium

### geckodriver 설치
# mac os 
$ wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-macos.tar.gz
# linux
$ wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz

### 환경변수 설정 (binary 파일을 전역패스로 등록)
$ mkdir -p ~/env
$ mkdir -p ~/env/webdriver
$ cd ~/env/webdriver
$ tar xvzf geckodriver-v0.26.0-macos.tar.gz

## mac os
$ vim ~/.zshrc
## linux
$ vim ~/.bashrc
or
$ sudo vim /etc/profile
# .......
export WEBDRIVER=~/env/webdriver/geckodriver
# .......
export PATH=$PATH:$WEBDRIVER
# .......
:wq

## mac os
$ source ~/.zshrc
## linux
$ vim ~/.bashrc
or
$ vim /etc/profile
```



셀레늄을 돌리기 위해서는 WebDriver 라는 바이너리 파일이 필요한데, 널리 알려진 WebDriver중 가장 대중적으로 사용되는 것이 [geckodriver](https://github.com/mozilla/geckodriver/releases/tag/v0.26.0) 이다.



# infra 

- AWS 에서 매일 23:00:00 마다 데이터 크롤링
- AWS RDS 에 데이터 insert
- AWS S3에 월별 KOSPI/KOSDAQ 등록 기업 csv파일 관리
- 추후 람다로의 전환 여부 검토
- 젠킨스 vs 코드디플로이&Travis .... (검토중)