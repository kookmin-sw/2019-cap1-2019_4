# Flex Ads
2019년 국민대학교 소프트웨어학부 캡스톤 디자인 프로젝트<br/>
https://kookmin-sw.github.io/2019-cap1-2019_4
<br/><br/>


## 1. 프로젝트 소개 

<img align="left" width="20%" height="20%" src="./doc/회의록/pictures/logo.png"> 

 &nbsp;Flex Ads는 쿠팡, 아마존닷컴과 같은 온라인 마켓에서 우리가 구매하거나 클릭한 상품들을 기반으로한 상품 추천을 오프라인 마켓으로 확장시켜, 회원제 오프라인 마켓에서의 광고 추천 시스템을 구현하는 프로젝트입니다. 클라우드 및 서버리스 환경에서 마켓을 이용하는 회원들의 얼굴을 인식하여 회원 정보를 반환하고, 추천 시스템을 통해 적합한 광고를 송출합니다. 
<br/><br/>
 &nbsp; Flex Ads is a project to implement advertising system. On online markets like Coupang and Amazon.com, they recommend the product which customers are more likely to buy, by using the records about what they have purchased or clicked on. Extending the available range from online to offline, we apply the recommendation system on offline markets. 

<br/>

<b>프로젝트 시나리오</b><br/><br/>
<img align="center" width="100%" height="100%" src="https://github.com/kookmin-sw/2019-cap1-2019_4/blob/master/doc/%ED%9A%8C%EC%9D%98%EB%A1%9D/pictures/architecture.jpeg"> 
<br/><br/>
ⓐ 딥러닝을 통해 얼굴 데이터셋을 생성하고, 회원 ID와 함게 Rekognition에 얼굴을 등록한다.<br/>
ⓑ 일정 기간을 정하여 회원의 구매내역을 XGBoost를 통해 학습하여 가장 구매 가능성이 높은 상품에 대한 광고 정보를 입력한다.<br/>
① 회원이 Jetson에 연결된 카메라에 포착된다.<br/>
② 딥러닝을 통해 얼굴이 detect 되고, S3로 전송된다.<br/>
③ 클라우드에서 Rekognition을 통해 얼굴이 인식된다.<br/>
④ 인식된 회원 정보를 이용해 송출할 광고 정보를 API Gateway를 통해 DynamoDB에서 가져온다.<br/>
⑤ 해당하는 광고를 S3에서 가져와 디스플레이로 송출한다.<br/>

## 2. 소개 영상
사진을 클릭하면 Youtube로 넘어갑니다.<br/>
##### (1) 최종 데모 영상
[![flexads](./doc/%ED%9A%8C%EC%9D%98%EB%A1%9D/pictures/flexads_youtube_thumbnail_final.png)](
https://youtu.be/uspIkRLVFe4)<br/><br/>

##### (2) 소개 영상
[![flexads](./doc/%ED%9A%8C%EC%9D%98%EB%A1%9D/pictures/flexads_youtube_thumbnail.png)](https://youtu.be/yIW5yL--zU8)<br/><br/>


## 3. 팀 소개

<img align="left" width="15%" height="15%" src="https://github.com/kookmin-sw/2019-cap1-2019_4/blob/upload_pictures/doc/회의록/pictures/prof_leeky.jpg">

```
이경용 교수님

캡스톤 디자인 프로젝트 지도교수님
프로젝트 검수

leeky@kookmin.ac.kr
```


<img align="left" width="15%" height="15%" src="https://github.com/kookmin-sw/2019-cap1-2019_4/blob/upload_pictures/doc/회의록/pictures/민지수.jpg">

```
민지수
Project Leader
AWS RDS와 DynamoDB 데이터 처리 및 관리
추천 시스템 구조 설계 및 알고리즘 구현 관리
Serverless 기반의 광고 송출 시스템 구현(얼굴 인식 결과와 추천 시스템 연동)


jsmin0415@gmail.com
```

<img align="left" width="15%" height="15%" src="https://github.com/kookmin-sw/2019-cap1-2019_4/blob/upload_pictures/doc/회의록/pictures/유지원.jpg">

```
유지원
사용자와 상품 관련 추천 서비스(알고리즘) 개발 및 연구
데이터 분석 및 처리
Feature & Model Generator



jiwon72674@gmail.com
```

<img align="left" width="15%" height="15%" src="https://github.com/kookmin-sw/2019-cap1-2019_4/blob/upload_pictures/doc/회의록/pictures/윤지영.jpg">

```
윤지영
AWS RDS 데이터 처리 및 관리
추천 알고리즘 수현을 위한 Feature Generator 
회의록 및 문서 작성



wldud8463@kookmin.ac.kr
```

<img align="left" width="15%" height="15%" src="https://github.com/kookmin-sw/2019-cap1-2019_4/blob/upload_pictures/doc/%ED%9A%8C%EC%9D%98%EB%A1%9D/pictures/%E1%84%8B%E1%85%B5%E1%84%89%E1%85%A5%E1%86%BC%E1%84%8C%E1%85%A2.jpg">

```
이성재
얼굴 인식을 위한 시스템 설계
Rekognition을 이용한 얼굴 학습 및 Jetson과의 연동 시스템 구축
Lambda Function을 이용한 S3-Rekognition-EC2의 연결



odobenuseKR@gmail.com
```


<img align="left" width="15%" height="15%" src="https://github.com/kookmin-sw/2019-cap1-2019_4/blob/upload_pictures/doc/회의록/pictures/황수진.jpg">

```
황수진
Jeston TX1 설정 및 관리
Jetson 과 AWS S3 연동 시스템 구축 
Web UI 개발


blue8957@gmail.com
```

## 4. 기타
* 기타 기록과 문서는 wiki를 사용합니다.
* 코드는 해당하는 작업 branch에 작성되어있으며, 최종 결과가 나온 후 master로 합쳐질 예정입니다.
* 회의록과 제출해야하는 문서는 각 평가일에 맞추어 master로 merge됩니다.
* **최종 결과물에 대한 내용은 최종보고서에 기술되어있습니다.**
* **기타 작업 내용은 Issue를 통해 살펴볼 수 있습니다.**
