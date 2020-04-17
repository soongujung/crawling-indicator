# 경제지표 크롤링

매일 23:00:00 마다 데이터 수집(crawling) 및 INSERT 하는 프로그램  

# 크롤링 대상

- 금리(한국, 미국, 일본)
- 환율(한국, 미국, 일본)
- KOSPI, 다우존스 종합주가지수
- 금 거래가 (일 종가)
- KOSPI 등록기업 리스트 (월별)
- KOSDAQ 등록기업 리스트 (월별)
- 국내 주식 재무제표 주요지표(PER, PBR, 주당순이익, etc) 
- 채권... (채권 관련 공부 필요...)



# 초기설정

```bash
# virtualenv가 설치되어 있지 않다면 pip install virtualenv
$ virtualenv indicator

$ source activate.sh
$ pip install -r requirements.txt
```



# infra 

- AWS 에서 매일 23:00:00 마다 데이터 크롤링
- AWS RDS 에 데이터 insert
- 추후 람다로의 전환 여부 검토