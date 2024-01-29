# looker-api-test-vf

## Python Sample Code 수행 설명 

### 01_create_and_test_connection

[Input Arguments]

1) Connection name : 신규 생성할 Connection 이름

---

### 02_create_and_update_project

[Input Arguments]

1) Project name : 신규 생성할 프로젝트 이름
  
2) Git Repository name : 신규 생성할 깃 리포지토리 이름 

---

### 03_create_lookml_model

[Input Arguments]

1) Connection name : 모델에 사용할 Connection name
  
2) Git Repository name : 모델이 생성될 프로젝트에 연결된 깃 리포지토리 이름 
  
3) Project name : 모델이 생성될 프로젝트 이름
  
4) Model name : 신규 생성할 모델 이름

---

### 04_create_query_and_look

[Input Arguments]

1) Look name : 신규 생성할 Look 이름
  
2) Model name : Look에서 사용할 모델 이름
  
3) Source Look ID : Look 생성을 위해 query 정보를 얻을 Look ID (Preset Look)

---

## Models / Views 폴더 설명

### Models/

model_template 파일의 "Your Connection" 부분을 신규 생성한 Connection 이름으로 대치하여 사용 

-> api_call_model_vf.model.lkml


### Views/

view_template 파일의 "Your_Schema", "Your_Table" 부분을 사용중인 스키마, 테이블 이름으로 대치하여 사용

-> superstore.view.lkml 

