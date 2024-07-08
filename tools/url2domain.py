import tldextract

def extract_domain(url):
    extracted_info = tldextract.extract(url)
    domain = f"{extracted_info.domain}.{extracted_info.suffix}"
    return domain

mdict = {}

def read_file_line_by_line(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            mainDomain = extract_domain(line.strip()).strip()
            if mainDomain in mdict:
                mdict[mainDomain] = mdict[mainDomain] + 1
            else:
                mdict[mainDomain] = 1
            # print(extract_domain(line.strip()).strip())
    sorted_dict = sort_dict_descending(mdict)
    # print(sorted_dict)
    for key, value in sorted_dict.items():
        print(f"{key}: {value}")

def sort_dict_descending(input_dict):
    # 对字典按值从大到小排序
    sorted_dict = dict(sorted(input_dict.items(), key=lambda item: item[1], reverse=True))
    return sorted_dict

# url = "https://www.xlzx.zju.edu.cn"
# print(extract_domain(url))
# # 调用函数并传入文件路径
# read_file_line_by_line('URL.txt')