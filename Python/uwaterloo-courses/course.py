from datetime import datetime
import requests
import re
import numpy as np
import json
import copy
import pandas as pd


class console:
    @staticmethod
    def found(sth:str) -> None:
        print(f'\033[0;32m[{sth.upper()}]\tFound\033[0m')

    @staticmethod
    def missing(sth:str) -> None:
        print(f'\033[0;31m[{sth.upper()}]\tMissing\033[0m')


class link:
    year = datetime.now().year % 100
    api = 'https://uwflow.com/graphql'
    base = 'http://ugradcalendar.uwaterloo.ca/page/uWaterloo-Undergraduate-Calendar-Access'
    faculty = 'http://ugradcalendar.uwaterloo.ca/group/Courses-Faculty-of-'
    course = f'https://ucalendar.uwaterloo.ca/{year}{year+1}/COURSE/'
    js = {"operationName": "getCourse",
          "variables": {
              "code": None
              },
          "query": "query getCourse($code: String) {\n  course(where: {code: {_eq: $code}}) {\n    ...CourseInfo\n    ...CourseSchedule\n    ...CourseRequirements\n    ...CourseRating\n    __typename\n  }\n}\n\nfragment CourseInfo on course {\n  id\n  code\n  name\n  description\n  profs_teaching {\n    prof {\n      id\n      code\n      name\n      rating {\n        liked\n        comment_count\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment CourseSchedule on course {\n  id\n  sections {\n    id\n    enrollment_capacity\n    enrollment_total\n    class_number\n    section_name\n    term_id\n    updated_at\n    meetings {\n      days\n      start_date\n      end_date\n      start_seconds\n      end_seconds\n      location\n      prof {\n        id\n        code\n        name\n        __typename\n      }\n      is_closed\n      is_cancelled\n      is_tba\n      __typename\n    }\n    exams {\n      date\n      day\n      end_seconds\n      is_tba\n      location\n      section_id\n      start_seconds\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment CourseRequirements on course {\n  id\n  antireqs\n  prereqs\n  coreqs\n  postrequisites {\n    postrequisite {\n      id\n      code\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment CourseRating on course {\n  id\n  rating {\n    liked\n    easy\n    useful\n    filled_count\n    comment_count\n    __typename\n  }\n  __typename\n}\n"
          }


def lookup(course:list) -> list:
    category = ['liked', 'easy', 'useful', 'filled_count', 'comment_count']
    stdz = lambda x: np.nan if x is None else round(x, 2)
    js = copy.deepcopy(link.js)
    course = course[0]
    
    # request data from uwflow
    js['variables']['code'] = course
    res = requests.post(url=link.api, json=js)
    data = json.loads(res.text)['data']['course']
    
    # grab useful information out, length of return value is always 8
    if len(data) > 0:
        data = data[0]
        rating = list(map(stdz, [data['rating'][i] for i in category]))
        info = [data['name'], data['description']]
        console.found(course)
        return [course] + rating + info
    else:
        console.missing(course)
        return [course] + [np.nan]*7


# inputs for all the methods here are NOT case sensitive
class get:
    @staticmethod
    def faculties() -> list:
        html = requests.get(url=link.base)
        data = re.findall(r'Faculty of (\w+)', html.text)
        return data
    
    
    @staticmethod
    def programs(faculty:str) -> list:
        url = link.faculty + faculty.capitalize()
        html = requests.get(url=url)
        data = re.findall(r'href="/courses/(\w+)" class="Level2Group"', html.text)
        return data

    
    @staticmethod
    def courses(program:str) -> list:
        url = link.course + f'course-{program.upper()}.html'
        html = requests.get(url=url)
        data = re.findall(r'<a name = "(\w+)">', html.text)
        return data
    
    
    @staticmethod
    def details(course:str|list) -> pd.DataFrame:
        shrink = lambda x: ''.join(x.lower().split())

        # allow user enter a program code(string) or a list of your courses(list)
        if isinstance(course, str): 
            course = get.courses(course) 
        if not isinstance(course, list) or not len(course):
            course = ['?']

        loads = pd.DataFrame(map(shrink, course))
        df = loads.apply(lookup, axis=1, result_type='expand')
        df.columns = ['code', 'liked', 'easy', 'useful', 'rated', 'comments', 'name', 'description']
        return df.set_index('code')
    
    