import hbshare as hbs
import ApiUtils
data = ApiUtils.commonQuery('SC_VALUATION', startDate ='2020-03-30 00:00:00', endDate='2020-03-31 00:00:00')
print(data)