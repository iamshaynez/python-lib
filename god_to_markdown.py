import pandas as pd

def read_excel_file(file_path):
    # 使用 pandas 读取 Excel 文件
    return pd.read_excel(file_path)

def generate_markdown(df):
    # 按照 nameOfGod 字段的首字母排序并分组
    df['initial'] = df['nameOfGod'].str[0].str.upper()
    grouped = df.groupby('initial')
    
    markdown_content = ""
    
    for initial, group in grouped:
        markdown_content += f"### {initial}\n\n"
        #markdown_content += "table with gods start with letter " + initial + "\n\n"
        
        # 创建 Markdown 表格
        markdown_content += "| nameOfGod | region | religion |\n"
        markdown_content += "|-----------|--------|----------|\n"
        
        for _, row in group.iterrows():
            markdown_content += f"| {row['nameOfGod']} | {row['region']} | {row['religion']} |\n"
        
        markdown_content += "\n"
    
    return markdown_content

def main():
    file_path = "output.xlsx"
    df = read_excel_file(file_path)
    markdown_document = generate_markdown(df)
    
    # 打印 Markdown 文档
    print(markdown_document)

if __name__ == "__main__":
    main()