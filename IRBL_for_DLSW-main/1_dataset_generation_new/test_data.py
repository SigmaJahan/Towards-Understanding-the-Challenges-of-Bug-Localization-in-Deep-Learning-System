
import os
def count_files():
    file_count = sum(len(files) for _, _, files in
                     os.walk(r'C:\Users\sigma\Desktop\ICSME-2023\Dataset\Denchmark'))

    print("total file count : ", file_count)


count_files()




def count_files():
    file_count = sum(len(files) for _, _, files in
                     os.walk(r'C:\Users\sigma\Desktop\ICSME-2023\Dataset\Denchmark_bugs'))

    print("total bug file count : ", file_count)


count_files()




# def count_files():
#     file_count = sum(len(files) for _, _, files in os.walk(
#         r'C:\Sharad\Dalhousie\Study\Semester 3\Courses\DATA SCIENCE\Project\ICST2022\Dataset\Denchmark_searchspace'))
#
#     print("total search space file count : ", file_count)
#
#
# count_files()