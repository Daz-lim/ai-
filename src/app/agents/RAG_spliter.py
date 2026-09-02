from langchain_text_splitters import CharacterTextSplitter

# 准备一段较长的文本
long_text = docs[0].page_content

# 创建字符切分器
text_splitter = CharacterTextSplitter(
    separator="\n",    # 以换行符作为分隔
    chunk_size=1000,     # 每块最大1000字符
    chunk_overlap=200,   # 块之间重叠200字符
)


# 切分文本
chunks = text_splitter.split_text(long_text)

print(f"原始文本长度: {len(long_text)} 字符")
print(f"切分为 {len(chunks)} 个块:\n")
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ({len(chunk)}字符) ---")
    print(chunk)
    print()