import requests
import json
from datetime import date, time, datetime, timedelta
from calendar import monthrange
import re


class SchoolmealApi:
    def __init__(self, api_key, base_url="https://open.neis.go.kr/hub/mealServiceDietInfo", citicode="B10", schoolcode="7010536"):
        self.api_key = api_key # API Key
        self.base_url = base_url # API URL
        self.citicode = citicode # 교육청코드
        self.schoolcode = schoolcode # 학교코드
        self.base_type = "json" # xml, json

        self.params = {
            "KEY": self.api_key,
            "Type": self.base_type,
            "ATPT_OFCDC_SC_CODE": self.citicode,
            "SD_SCHUL_CODE": self.schoolcode,
        }
        
    def format_data_style(self, data):
        if isinstance(data, dict):
            data = [data]
        results = []

        for item in data:
            raw_date = item.get("MLSV_YMD")
            if not raw_date:
                continue
            formatted_date = datetime.strptime(raw_date, "%Y%m%d").strftime("%Y-%m-%d")
            dish_list = item.get("DDISH_NM", "").split("\n")
            meals = []
            for idx, dish in enumerate(dish_list):
                dish = dish.strip()
                if not dish:
                    continue
                brackets = re.findall(r'\((.*?)\)', dish) # 괄호안 내용 추출
                code = None
                option = []
                if brackets:
                    if re.fullmatch(r'[\d\.]+', brackets[-1]):
                        code = brackets[-1]
                        option = brackets[:-1]
                    else:
                        option = brackets
                name = re.sub(r'\s*\(.*?\)', '', dish).strip() # 괄호 제외한 실제 메뉴 이름 추출 ex: '계란국 (추가) (1.5.6.18)' → '계란국'
                meals.append({
                    "id": idx + 1,
                    "meal": name,
                    "code": code,
                    "option": option if option else []
                })
            results.append({
                "date": formatted_date,
                "meals": meals
            })
        return results
    
    def get_day_meal_data(self, date: datetime):
        date_int = date.strftime('%Y%m%d') # 날짜를 YYYYMMDD 형식으로 변환
        URL = self.base_url

        req_params = self.params
        req_params["MLSV_YMD"] = date_int

        response = requests.get(URL, params=req_params)
        response_data = json.dumps(response.json()).replace("<br/>", "\\n") # <br/>를 \n으로 변환
        try:
            j_response = json.loads(response_data)["mealServiceDietInfo"]
            if j_response[0]["head"][0]["list_total_count"] == 1:
                return {"status": "success", "data":  j_response[1]["row"][0]}
            else:
                return {"status": "success", "data": j_response[1]["row"]}
        except:
            return {"status": "fail", "reason": "Not found data", "data": response.json()}

    def get_fromto_meal_data(self, from_date: datetime, to_date: datetime):
        from_date_int = from_date.strftime('%Y%m%d')
        to_date_int = to_date.strftime('%Y%m%d')
        URL = self.base_url

        req_params = self.params
        req_params["MLSV_FROM_YMD"] = from_date_int # 시작일
        req_params["MLSV_TO_YMD"] = to_date_int # 종료일

        response = requests.get(URL, params=req_params)
        response_data = json.dumps(response.json()).replace("<br/>", "\\n") # <br/>를 \n으로 변환
        try:
            j_response = json.loads(response_data)["mealServiceDietInfo"]
            if j_response[0]["head"][0]["list_total_count"] == 1:
                return {"status": "success", "data":  j_response[1]["row"][0]}
            else:
                return {"status": "success", "data": j_response[1]["row"]}
        except:
            return {"status": "fail", "reason": "Not found data", "data": response.json()}
    
    def get_today_meal_data(self):
        if date is None:
            date = datetime.today()
        result = self.get_day_meal_data(date)
        return result

    def get_tomorrow_meal_data(self, date: datetime = None):
        if date is None:
            date = datetime.today()
        date = date + timedelta(days=1)
        result = self.get_day_meal_data(date)
        return result
    
    def get_yesterday_meal_data(self, date: datetime = None):
        if date is None:
            date = datetime.today()
        date = date - timedelta(days=1) # 어제 날짜
        result = self.get_day_meal_data(date)
        return result

    def get_week_meal_data(self, date: datetime = None):
        if date is None:
            date = datetime.today()

        weekday = date.weekday()
        monday = date - timedelta(days=weekday)
        friday = monday + timedelta(days=4)

        result = self.get_fromto_meal_data(monday, friday)
        if result["status"] == "success" and isinstance(result["data"], list): # 날짜순 정렬
            result["data"].sort(key=lambda row: row["MLSV_YMD"])
        return result
    
    def get_month_meal_data(self, date: datetime = None):

        if date is None:
            date = datetime.today()
        year = date.year
        month = date.month

        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, monthrange(year, month)[1])

        result = self.get_fromto_meal_data(first_day, last_day)
        if result["status"] == "success" and isinstance(result["data"], list): # 날짜순 정렬
            result["data"].sort(key=lambda row: row["MLSV_YMD"])
        return result
    
