# FlexAds
2019년 국민대학교 소프트웨어학부 캡스톤 디자인 프로젝트



### 1. 프로젝트 소개 

<img align="left" width="20%" height="20%" src="https://github.com/kookmin-sw/2019-cap1-2019_4/blob/upload_pictures/doc/회의록/pictures/logo.png"> 

 &nbsp;FlexAds는 쿠팡, 아마존닷컴과 같은 온라인 마켓에서 우리가 구매하거나 클릭한 상품들을 기반으로한 상품 추천을 오프라인 마켓으로 확장시켜, 회원제 오프라인 마켓에서의 광고 추천 시스템을 구현하는 프로젝트입니다. 클라우드 및 서버리스 환경에서 마켓을 이용하는 회원들의 얼굴을 인식하여 회원 정보를 반환하고, 추천 시스템을 통해 적합한 광고를 송출합니다. 
<br/>
 &nbsp; FlexAds is a project to implement advertising system. On online markets like Coupang and Amazon.com, they recommend the product which customers are more likely to buy, by using the records about what they have purchased or clicked on. Extending the available range from online to offline, we apply the recommendation system on offline markets. 

<br/>
**프로젝트 시나리오**<br/>
<img align="center" width="80%" height="80%" src="https://github.com/kookmin-sw/2019-cap1-2019_4/blob/upload_pictures/doc/회의록/pictures/flexadsscenario.png"> 
<br/>

### 2. 소개 영상

프로젝트 소개하는 영상을 추가하세요

### 3. 팀 소개

*  민지수<br/>

<img align="left" width="15%" height="15%" src="https://github.com/kookmin-sw/2019-cap1-2019_4/blob/upload_pictures/doc/회의록/pictures/민지수.jpg">

```
Project Leader
AWS RDS와 DynamoDB 데이터 처리 및 관리
추천 시스템 구조 설계 및 알고리즘 구현 관리
Serverless 기반의 광고 송출 시스템 구현(얼굴 인식 결과와 추천 시스템 연동)



jsmin0415@gmail.com
```


*  유지원<br/>

<img align="left" width="15%" height="15%" src="https://github.com/kookmin-sw/2019-cap1-2019_4/blob/upload_pictures/doc/회의록/pictures/유지원.jpg">

```
사용자와 상품 관련 추천 서비스(알고리즘) 개발 및 연구 - 상품 담당
AWS RDS와 DynamoDB 데이터 처리 및 관리
Feature Generator




jiwon72674@gmail.com
```


*  윤지영 <br/>

<img align="left" width="15%" height="15%" src="https://github.com/kookmin-sw/2019-cap1-2019_4/blob/upload_pictures/doc/회의록/pictures/윤지영.jpg">

```
사용자와 상품 관련 추천 서비스(알고리즘) 개발 및 연구 - 사용자 담당
회의록 및 문서 작성 





wldud8463@kookmin.ac.kr
```


*  이성재<br/>

<img align="left" width="15%" height="15%" src="https://github.com/kookmin-sw/2019-cap1-2019_4/blob/upload_pictures/doc/%ED%9A%8C%EC%9D%98%EB%A1%9D/pictures/%E1%84%8B%E1%85%B5%E1%84%89%E1%85%A5%E1%86%BC%E1%84%8C%E1%85%A2.jpg">


```
얼굴 인식을 위한 시스템 설계
Rekonition을 이용한 얼굴 학습 및 Jetson과의 연동 시스템 구축
Lambda Function을 이용한 S3-Rekognition-EC2의 연결




odobenuseKR@gmail.com
```


*  황수진<br/>

<img align="left" width="15%" height="15%" src="https://github.com/kookmin-sw/2019-cap1-2019_4/blob/upload_pictures/doc/회의록/pictures/황수진.jpg">

```
TX1 / TX2 설정 및 관리
얼굴 인식 서비스 개발 
AWS S3 저장소 데이터 관리


blue8957@gmail.com
```

### 4. 사용법
* 회의록 작성
1. markdown으로 회의록 양식에 맞추어 작성하기
2. /doc/회의록/에 회의록작성
3. preview로 확인하여 불필요한 commit 방지하기

* Pull requests
1. branch에서 작업 후 일정 작업이 완성된 후 작성, commit마다 request보내지 않기
2. 작업한 내용의 설명 및 변경 사항 기록과 함께 request

* Rules for creating folder / file / branch names
1. 영어 소문자 사용,  공백이 필요한 경우 _(underscore)사용
2. 포함되는 내용을 이해할 수 있도록 naming

