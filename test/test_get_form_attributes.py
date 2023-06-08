from src.scraping.form_spider import FormSpider

URL_42 = 'https://candidatura.42malaga.com/users/sign_up'

if __name__ == '__main__':
    spider = FormSpider(URL_42)
    forms_info = spider.form_info()
    for form in forms_info:
        print(f'method: {form.method}')
        print(f'action: {form.action}')
        for f_input in form.inputs:
            print(f'  type:  {f_input.type}')
            print(f'  id:    {f_input.id}')
            print(f'  name:  {f_input.name}')
            print(f'  value: {f_input.value}')
            print()
        print()
