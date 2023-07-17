# 打开源文件和目标文件
with open('VirusShare_00420.zip.hashes', 'r') as src_file, open('target.txt', 'w') as tgt_file:
    # 逐行读取源文件
    for line in src_file:
        # 将每行按空格分割成单词列表
        words = line.strip().split()
        # 如果当前行有至少6个单词，则将第6个单词写入目标文件
        if len(words) >= 6:
            tgt_file.write(words[7] + ' ' + words[-1] + '\n')
