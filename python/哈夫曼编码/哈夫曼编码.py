#定义节点类
class node(object): #object类是所有类最终都会继承的类
    def __init__(self, value = None, left = None, right = None, father = None):
        self.value = value
        self.left = left
        self.right = right
        self.father = father

def find_father(left, right):
	fa = node(value = left.value + right.value, left = left, right = right)
	left.father = right.father = fa
	return fa

#构建哈夫曼树
def build_tree(cur_nodes):
	if len(cur_nodes) == 1: #root
		return cur_nodes
	#返回副本sorts，原始输入cur_nodes不变
	sorts = sorted(cur_nodes, key = lambda x:x.value) #按照出现次数升序
	n = find_father(sorts[0], sorts[1])
	sorts.pop(0)
	sorts.pop(0)
	sorts.append(n)
	return build_tree(sorts)

def encode(x):
	if x.father == None:
		return b''
	if x.father.left == x:
		return encode(x.father) + b'0' #左孩子编号'0'
	else:
		return encode(x.father) + b'1' #右孩子编号'1'
    
#得到编码表encode_dict
def code_table():
	for x in node_dict.keys():
		encode_dict[x] = encode(node_dict[x])

#图像编码
def encode_image(input_image):
	image = open(input_image, "rb") #按字节读取二进制文件
	image.seek(0, 2) #0表示偏移量，2表示从文件末尾算起
	count = image.tell()  #tell()返回文件游标的位置，意在计算字节数
	buff = [b''] * int(count)
	image.seek(0) #游标回到文件开头

	#统计每一个像素值的出现次数
	i = 0
	while i < count:
		buff[i] = image.read(1)
		if count_dict.get(buff[i], -1) == -1: #如果buff[i]不存在，则返回-1
			count_dict[buff[i]] = 0
		count_dict[buff[i]] = count_dict[buff[i]] + 1
		i = i + 1
	image.close()

	#将每个字节构建成一个树节点
	for x in count_dict.keys():
		node_dict[x] = node(count_dict[x])
		nodes.append(node_dict[x])
	build_tree(nodes) #构建哈夫曼树
	code_table() #构建编码表

   	#写压缩文件——必要信息 
	count_sorts = sorted(count_dict.items(), key = lambda x:x[1], reverse = True) #按照出现次数降序排列
	byte_width = 1
	if count_sorts[0][1] > 255: # >8 bits
		byte_width = 2
		if count_sorts[0][1] > 65535: # >16 bits
			byte_width = 3
			if count_sorts[0][1] > 16777215: # >24 bits
				byte_width = 4
	image_name = input_image.split('.')
	o = open(image_name[0]+".txt", 'wb')
	image_name = input_image.split('/')
	o.write((image_name[len(image_name)-1] + '\n').encode(encoding="utf-8")) #写入原图像名
	o.write(int.to_bytes(int(count), 4, byteorder = 'big')) #写入图像像素个数    
	o.write(int.to_bytes(len(encode_dict), 2, byteorder = 'big')) #写入节点数量
	o.write(int.to_bytes(byte_width, 1, byteorder = 'big')) #写入表示出现次数的字节长度
	for x in encode_dict.keys(): #列出原始像素值 出现次数
		o.write(x)
		o.write(int.to_bytes(count_dict[x], byte_width, byteorder = 'big'))

	#写压缩文件——编码
	raw = 0b1 #二进制 1
	i = 0
	while i < count: #存储每一个像素的编码
		for x in encode_dict[buff[i]]: #遍历这个编码的每一bit
			raw = raw << 1
			if x == 49: #左移一位补0，若编码为'1'，则需将新补的位变为1
				raw = raw | 1
			if raw.bit_length() == 9: #每8位写入一次
				raw = raw & (~(1 << 8)) #最高位（第9位）是初始化的1，此举可去掉最高位，剩下8位是真正的编码
				o.write(int.to_bytes(raw, 1, byteorder = 'big'))
				o.flush() #将缓冲区中的数据立刻写入文件,同时清空缓冲区
				raw = 0b1
		i = i + 1

	#对文件进行哈夫曼编码，01串不一定是8的倍数,故最后几位需另外处理
	if raw.bit_length() > 1: 
		raw = raw << (8 - (raw.bit_length() - 1)) #最后的01串后面全补0
		raw = raw & (~(1 << 8))
		o.write(int.to_bytes(raw, 1, byteorder = 'big'))
	o.close()
	print("Encode finish...")  

#图像解码
def decode_image(input_file):
	image = open(input_file, 'rb') #打开压缩文件
	image.seek(0, 2)
	eof = image.tell()
	image.seek(0)
	image_name = input_file.split('/')
	output_image = input_file.replace(image_name[len(image_name)-1], image.readline().decode(encoding="utf-8")) #原文件名（相对路径）
	output_image = output_image.replace('\n', '') #去掉换行符
	output_image = output_image.replace('.', '_new_now.') #解压后的文件名

   	#从压缩文件中获取必要信息
	o = open(output_image,'wb') 
	pixels_num = int.from_bytes(image.read(4), byteorder = 'big') #取出图像像素个数（4字节）
	count = int.from_bytes(image.read(2), byteorder = 'big') #取出节点数量（2字节）
	byte_width = int.from_bytes(image.read(1), byteorder = 'big') #取出表示出现次数的字节长度（1字节）
	i = 0
	while i < count: 
		key = image.read(1) #读取像素值（1字节）
		value = int.from_bytes(image.read(byte_width), byteorder = 'big') #读取出现次数
		count_dict[key] = value
		i = i + 1
	for x in count_dict.keys():
		node_dict[x] = node(count_dict[x])
		nodes.append(node_dict[x])
	build_tree(nodes)	 #重建哈夫曼树
	code_table() #构建编码表
	for x in encode_dict.keys(): #构建字典： 编码->原始像素值 
		inverse_dict[encode_dict[x]] = x

   	#开始解码	
	pixels_num_i = 0
	i = image.tell()
	data = b''
	while i < eof: #解压数据
		raw = int.from_bytes(image.read(1), byteorder = 'big')
		i = i + 1
		j = 8
		while j > 0: #按bit处理编码
			if (raw >> (j - 1)) & 1 == 1: #该bit为1
				data = data + b'1'
			else: #该bit为0
				data = data + b'0'
			if inverse_dict.get(data, 0) != 0: #如果没有该编码，则返回0
				o.write(inverse_dict[data])
				o.flush()
				data = b''
				pixels_num_i = pixels_num_i + 1 
				if pixels_num_i == pixels_num: #达到像素个数就不再继续解压，此举是为了防止对最后一个字节多余的0进行处理
					break;
			j = j - 1
	image.close()
	o.close()
	print("Decode finish...") 

if __name__ == '__main__':
	node_dict = {} #原始像素值->树节点
	count_dict = {} #原始像素值->出现次数
	encode_dict = {} #原始像素值->编码
	inverse_dict = {} #编码->原始像素值
	nodes = [] #原始像素值 

	if input("1:Compress the file\n2:Decompress the file\nPlease enter the operation:") == '1':
		encode_image(input("Please input the fileimage_name:"))
	else:
		decode_image(input("Please input the fileimage_name:"))  