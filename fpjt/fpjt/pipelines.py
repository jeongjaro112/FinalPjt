# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import os
import datetime
from scrapy.exporters import CsvItemExporter
from itemadapter import ItemAdapter



class FpjtPipeline:
    def __init__(self):
        time_stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name = f'stockInfo_{time_stamp}.csv'
        file_path = os.path.join(os.getcwd(), 'fhs', file_name)
        self.file = open(file_path, 'wb')
        self.exporter =CsvItemExporter(self.file, encoding = 'utf-8')
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

# import os
# import datetime
# from scrapy.exporters import CsvItemExporter
# from itemadapter import ItemAdapter

# class FpjtPipeline:
#     def __init__(self):
#         time_stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
#         file_name_all = f'stockInfo_all_{time_stamp}.csv'
#         file_name_filtered = f'stockInfo_filtered_{time_stamp}.csv'
#         file_path_all = os.path.join(os.getcwd(), 'fhs', file_name_all)
#         file_path_filtered = os.path.join(os.getcwd(), 'fhs', file_name_filtered)
#         self.file_all = open(file_path_all, 'wb')
#         self.file_filtered = open(file_path_filtered, 'wb')
#         self.exporter_all = CsvItemExporter(self.file_all, encoding='utf-8')
#         self.exporter_filtered = CsvItemExporter(self.file_filtered, encoding='utf-8')
#         self.exporter_all.start_exporting()
#         self.exporter_filtered.start_exporting()
    
#     def close_spider(self, spider):
#         self.exporter_all.finish_exporting()
#         self.exporter_filtered.finish_exporting()
#         self.file_all.close()
#         self.file_filtered.close()
        
#     def process_item(self, item, spider):
#         adapter = ItemAdapter(item)
#         self.exporter_all.export_item(item)
        
#         condition1 = (
#             adapter.get('PER', 0) <= 20 and
#             adapter.get('PBR', 0) <= 2 and
#             adapter.get('배당수익율', 0) >= 2.0 and
#             adapter.get('EV_EBITDA', 0) < 5 and
#             adapter.get('부채비율', 0) <= 100 and
#             adapter.get('ROE', 0) >= 10
#         )
        
#         condition2 = (
#             adapter.get('투자의견') is not None and str(adapter.get('투자의견')).strip() != ''
#         )
        
#         if condition1 or condition2:
#             self.exporter_filtered.export_item(item)
            
#         return item

# import os
# import datetime
# from scrapy.exporters import CsvItemExporter
# from itemadapter import ItemAdapter

# class FpjtPipeline:
#     def __init__(self):
#         time_stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
#         file_name_all = f'stockInfo_all_{time_stamp}.csv'
#         file_name_condition1 = f'stockInfo_condition1_{time_stamp}.csv'
#         file_name_condition2 = f'stockInfo_condition2_{time_stamp}.csv'
#         file_name_combined = f'stockInfo_combined_{time_stamp}.csv'
#         file_path_all = os.path.join(os.getcwd(), 'fhs', file_name_all)
#         file_path_condition1 = os.path.join(os.getcwd(), 'fhs', file_name_condition1)
#         file_path_condition2 = os.path.join(os.getcwd(), 'fhs', file_name_condition2)
#         file_path_combined = os.path.join(os.getcwd(), 'fhs', file_name_combined)
#         self.file_all = open(file_path_all, 'wb')
#         self.file_condition1 = open(file_path_condition1, 'wb')
#         self.file_condition2 = open(file_path_condition2, 'wb')
#         self.file_combined = open(file_path_combined, 'wb')
#         self.exporter_all = CsvItemExporter(self.file_all, encoding='utf-8')
#         self.exporter_condition1 = CsvItemExporter(self.file_condition1, encoding='utf-8')
#         self.exporter_condition2 = CsvItemExporter(self.file_condition2, encoding='utf-8')
#         self.exporter_combined = CsvItemExporter(self.file_combined, encoding='utf-8')
#         self.exporter_all.start_exporting()
#         self.exporter_condition1.start_exporting()
#         self.exporter_condition2.start_exporting()
#         self.exporter_combined.start_exporting()
    
#     def close_spider(self, spider):
#         self.exporter_all.finish_exporting()
#         self.exporter_condition1.finish_exporting()
#         self.exporter_condition2.finish_exporting()
#         self.exporter_combined.finish_exporting()
#         self.file_all.close()
#         self.file_condition1.close()
#         self.file_condition2.close()
#         self.file_combined.close()
        
#     def process_item(self, item, spider):
#         adapter = ItemAdapter(item)
#         self.exporter_all.export_item(item)
        
#         condition1 = (
#             adapter.get('PER', 0) <= 20 and
#             adapter.get('PBR', 0) <= 2 and
#             adapter.get('배당수익율', 0) >= 2 and
#             adapter.get('EV_EBITDA', 0) < 5 and
#             adapter.get('부채비율', 0) <= 100 and
#             adapter.get('ROE', 0) >= 10
#         )
        
#         condition2 = (
#             adapter.get('투자의견') is not None and str(adapter.get('투자의견')).strip() != ''
#         )
        
#         if condition1:
#             self.exporter_condition1.export_item(item)
        
#         if condition2:
#             self.exporter_condition2.export_item(item)
        
#         if condition1 or condition2:
#             self.exporter_combined.export_item(item)
            
#         return item

###############
#import os
# import datetime
# from scrapy.exporters import CsvItemExporter
# from itemadapter import ItemAdapter
# import pandas as pd

# class FpjtPipeline:
#     def __init__(self):
#         time_stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
#         file_name = f'stockInfo_{time_stamp}.csv'
#         file_path = os.path.join(os.getcwd(), 'fhs', file_name)
#         self.file = open(file_path, 'wb')
#         self.exporter = CsvItemExporter(self.file, encoding='utf-8')
#         self.exporter.start_exporting()
#         self.df_filtered_1 = None
#         self.df_filtered_2 = None
#         self.df_filtered_3 = None
    
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()
        
#         if self.df_filtered_1 is not None:
#             self.df_filtered_1.to_csv('filtered_1.csv', index=False)
#         if self.df_filtered_2 is not None:
#             self.df_filtered_2.to_csv('filtered_2.csv', index=False)
#         if self.df_filtered_3 is not None:
#             self.df_filtered_3.to_csv('filtered_3.csv', index=False)
        
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         if self.df_filtered_1 is None:
#             self.df_filtered_1 = pd.DataFrame(item, index=[0])
#         else:
#             self.df_filtered_1 = self.df_filtered_1.append(item, ignore_index=True)
        
#         if self.df_filtered_2 is None:
#             self.df_filtered_2 = pd.DataFrame(item, index=[0])
#         else:
#             self.df_filtered_2 = self.df_filtered_2.append(item, ignore_index=True)
        
#         if self.df_filtered_3 is None:
#             self.df_filtered_3 = pd.DataFrame(item, index=[0])
#         else:
#             self.df_filtered_3 = self.df_filtered_3.append(item, ignore_index=True)
            
#         return item