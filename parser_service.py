from bs4 import BeautifulSoup
import requests
import lxml
import csv


session = requests.Session()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

stat_link = 'https://gomel.belstat.gov.by/'
salary_link = 'https://myfin.by/wiki/term/srednyaya-zarplata-v-gomelskoj-oblasti'
def load_page(url):
    res = session.get(url=url,headers=headers)
    return res.text

def get_avarage_salary_in_this_month():
    ''' Получение средней зарплаты в Гомеле в этом месяце '''
    soup = BeautifulSoup(load_page(stat_link),'lxml')
    salary = soup.select('p.promo__num')
    return salary[0].string + ' рублей'


def get_avarage_salary_in_prev_month():
    ''' Получения средней зарплаты в Гомеле в предыдущем месяце '''
    soup = BeautifulSoup(load_page(salary_link),'lxml')
    salary = soup.select('div.information-block__previous-value')
    salary_final = salary[0].string.split(': ')
    return salary_final[1][:-2]

def get_trand_salary():
    ''' Получения тренда(повышение или понижения) зарплаты в этом месяце по сравнению с предыдущим '''
    salary_this_month = get_avarage_salary_in_this_month().split(' ')
    salary_this_month = float(salary_this_month[0] + salary_this_month[1].replace(',','.'))

    salary_prev_month = get_avarage_salary_in_prev_month().split(' ')
    salary_prev_month = float(salary_prev_month[0] + salary_prev_month[1].replace(',','.'))

    return salary_this_month > salary_prev_month

def get_gomel_population():
    ''' Получения населения Гомеля '''
    soup = BeautifulSoup(load_page(stat_link),'lxml')
    population = soup.select('p.promo__num')
    population = population[-1].string
    population_final = population[0] + ' миллион' + population[1:-1] + '000 тысяч'
    return population_final
