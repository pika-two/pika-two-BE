from sqlalchemy import or_,and_,func, text
import math
from src.database import db

# company 기본 정보 등록
from src.model.models import Company, JobPost, Wage, User

# 기업 검색
def get_search_company(com_keyword:str, com_category:str, com_type:str, com_is_certified:int, p_size:int, p_num:int):
    # 한 페이지 당 최대 기업 개수
    p_size = 20
    
    # 회사 이름으로 검색 & 기업 규모로 검색, & 산업별로 검색 & 인증된 기업 여부 검색
    query_filter = [Company.name.like(f'%{com_keyword}%'), Company.category.like(f'%{com_category}%'), Company.type.like(f'%{com_type}%'), Company.is_certificated>=com_is_certified]
    result = Company.query.filter(and_(*query_filter))

    resultlist = []
    for res in result:
        resultlist.append({
            "company_id":res.id,
            "company_name":res.name,
            "type" :res.type,
            "category":res.category,
            "is_certificated":res.is_certificated
        })

    # 최대 페이지를 구하는 부분
    total_page = math.ceil(result.count() / p_size)

    return {
        "company_list": resultlist,
        "page_size": p_size,
        "page_num" : p_num,
        "total_page" : total_page
    }


def get_company_info(company_id:int):

    com = Company.query.get(company_id)
    job_post = JobPost.query.filter(JobPost.company_id == company_id)

    job_posts = []
    for job_p in job_post:
        res = {
            "post_id": job_p.id,
            "post_title":  job_p.title,
            "start_dt": job_p.start_dt,
            "end_dt": job_p.end_dt,
            "company_name": com.name
        }
        job_posts.append(res)

    ur = User.query.filter(User.cur_company_id == company_id).first()
    wage_list = []
    if ur is not None:
        for i in range(1, 6):
            # 연차별로 평균, 최소, 최대 연봉
            q = db.session.query(Wage).filter(Wage.company_id==company_id)
            avg_wage = q.with_entities(func.avg(Wage.amount).label("avg")).group_by(Wage.yr).having(Wage.yr == i).first()
            min_wage = q.with_entities(func.min(Wage.amount).label("avg")).group_by(Wage.yr).having(Wage.yr == i).first()
            max_wage = q.with_entities(func.max(Wage.amount).label("avg")).group_by(Wage.yr).having(Wage.yr == i).first()

            avg_wage = 0 if avg_wage == None else int(avg_wage[0])
            min_wage = 0 if min_wage == None else int(min_wage[0])
            max_wage = 0 if max_wage == None else int(max_wage[0])

            res = {
                "profession" : ur.profession,
                "avg": avg_wage,
                "min": min_wage,
                "max": max_wage,
                "year" : i
            }
            wage_list.append(res)

    return {
        "company_name" : com.name,
        "job_posts":job_posts,
        "wages" : wage_list
    }
def get_company_wage(company_id:int, year:int, pro:str):
    com = Company.query.get(company_id)

    results = (db.session.query(Wage)
               .join(User, Wage.user_id == User.id)
               .filter((Wage.yr == year) & (Wage.company_id == company_id) & (User.profession.like(f'%{pro}%')))
               .values(User.nickname,
                       Wage.amount))

    resultlist = []
    for u_nick, u_wage  in results:
        resultlist.append({'nickname': u_nick,
                           'wage': u_wage} )
    return {
        "company_name": com.name,
        "wages": resultlist
    }

def get_or_create_company(name: str, company_type="", category="", is_certificated=False):
    company_obj = Company.query.filter(Company.name==name).first()
    if company_obj is None:
        company_obj = Company(
            name = name,
            type=company_type,
            category=category,
            is_certificated=is_certificated
        )
        db.session.add(company_obj)
        db.session.commit()        
    return company_obj.id