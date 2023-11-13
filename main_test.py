from resourses import Purchases_info
from datetime import date

info = Purchases_info('test_data.csv')

info.drow_a_bar_chart(date(2023,11,1), date(2023, 11,20))