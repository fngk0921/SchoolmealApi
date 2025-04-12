# 📘 SchoolmealApi

**NEIS(나이스) 교육청 급식 조회 API**를 파이썬으로 쉽게 사용할 수 있도록 만든 클래스입니다.  
급식 데이터를 날짜별, 주별, 월별로 가져오고, 알레르기 코드와 옵션 포멧팅이 가능합니다.

---

## ✅ 필수 설치 라이브러리 및 준비

```bash
pip install requests
```

> 🔑 **API Key**는 [NEIS 오픈데이터포털](https://open.neis.go.kr/)에서 발급 가능

---

## 🧑‍💻 사용 예시

```python
from datetime import datetime
from schoolmeal import SchoolmealApi  # 예: SchoolmealApi 클래스가 정의된 파일

mealapi = SchoolmealApi("YOUR_API_KEY_HERE")

# 오늘 급식
print(mealapi.format_data_style(mealapi.get_today_meal_data()["data"]))

# 특정 날짜 급식
print(mealapi.format_data_style(mealapi.get_day_meal_data(datetime(2025, 4, 14))["data"]))

# 이번 주 급식
print(mealapi.format_data_style(mealapi.get_week_meal_data()["data"]))

# 이번 달 급식
print(mealapi.format_data_style(mealapi.get_month_meal_data()["data"]))
```

---

## 🧩 클래스 설명

### 📦 `SchoolmealApi(api_key, citicode="B10", schoolcode="7010536")`

| 파라미터         | 설명                              |
|------------------|-----------------------------------|
| `api_key`        | NEIS 오픈 API 키                   |
| `citicode`       | 교육청 코드 (기본: 서울 `B10`)     |
| `schoolcode`     | 학교 코드 (기본: 선린인터넷고 `7010536`) |

---

## 📚 주요 메서드

### 📅 날짜별 조회

```python
get_day_meal_data(date: datetime) → dict
get_today_meal_data() → dict
get_tomorrow_meal_data(date: datetime = None) → dict
get_yesterday_meal_data(date: datetime = None) → dict
```

### 📆 기간별 조회

```python
get_week_meal_data(date: datetime = None) → dict
get_month_meal_data(date: datetime = None) → dict
get_fromto_meal_data(from_date: datetime, to_date: datetime) → dict
```

### 🎨 데이터 포맷 정리

```python
format_data_style(data: dict or list) → list
```

급식 데이터를 아래와 같은 구조로 정리해줍니다:

```json
{
  "date": "2025-04-14",
  "meals": [
    {
      "id": 1,
      "meal": "계란국",
      "code": "1.5.6.18",
      "option": ["추가"]
    },
    {
      "id": 2,
      "meal": "자몽에이드",
      "code": "12.13",
      "option": ["완제"]
    }
  ]
}
```

---

## 📌 데이터 필드 설명

| 필드      | 설명                                   |
|-----------|----------------------------------------|
| `meal`    | 메뉴명                                 |
| `code`    | 알레르기 유발 식재료 코드               |
| `option`  | (선택적) 비고(예: "추가", "완제") 등    |
| `id`      | 리스트 내 순서 인덱스 (1부터 시작)      |
| `date`    | 해당 급식 날짜 (`YYYY-MM-DD` 형식)      |

---

## 🔁 알레르기 코드 안내 (예시)

| 코드 | 알레르기 유발 식재료 |
|------|-----------------------|
| 1    | 난류(계란)            |
| 2    | 우유                  |
| 5    | 대두                  |
| 6    | 밀                    |
| 13   | 돼지고기              |
| 18   | 조개류                |

---

## 🧪 테스트 예제

```python
api = SchoolmealApi("YOUR_API_KEY")
today = datetime(2025, 4, 14)
result = api.get_day_meal_data(today)
print(api.format_data_style(result["data"]))
```

---

