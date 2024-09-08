from urllib.parse import urlparse
url = "https://fanyi.baidu.com/mtpe-individual/multimodal?query=resource&lang=en2zh"
s = urlparse(url)
print(s.netloc)