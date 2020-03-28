#include<iostream>
#include "Histogram_show.h"
using namespace std;
const int maxn =1200000;

#pragma once
class mytran //二进制读入bmp文件，并进行操作 如果原来的一个数据是2字节为 10010000 01101111的话，那么实际存储的数据为：11110110 00001001
{
public:
	int cnt=0;
	static char yu[maxn+5];//二进制读取的图片数据
	static char yu2[maxn+5];
	int histogram[256+5];
	float bi[256 + 5];
	long long bfsize_pos = 2; //文件长度的偏移量 大小4字节
	long long bfoffbits_pos = 10;//图像数据开始的偏移量 4
	long long bisize_pos = 14;// 信息头大小 4
	long long kuan_pos = 18;// 图像宽度 偏移量4
	long long gao_pos = 22;// 图像高度 偏移量4
	long long bitcount_pos = 28;// 像素位数目 2 决定调色板数量、大小
	long long bmicolors = 54;//调色板位置，长度为4*bitcount
	long long bfoff, kuan, gao, bitcount, hang,bfsize=0,tiaose=0;
	long long st;
	mytran();
	~mytran();
	void init()
	{
		bfsize = get(bfsize_pos, 4);
		bfoff = get(bfoffbits_pos, 4);// 图像数据的offset
		kuan = get(kuan_pos, 4);//图像宽度
		gao = get(gao_pos, 4); // 图像高度
		bitcount = get(bitcount_pos, 2);// bitcount
		st = bfoff;
		hang = (bitcount*kuan + 31) / 32*4; //一行占据的实际字节数
		if (bitcount != 8)
		{
			MessageBox(NULL, TEXT("图片不是三通道的bmp， 要求bitcount=24"), TEXT("错误"), MB_OK);
		}
		//cout << "st:" << st << " bitcount:" << bitcount << " kuan:" << kuan << " gao:" << gao << endl;
	}
	void init_2()
	{
		tiaose = get(bitcount_pos, 2);
		bfsize = get(bfsize_pos, 4);
		bfoff = get(bfoffbits_pos, 4);// 图像数据的offset
		kuan = get(kuan_pos, 4);//图像宽度
		gao = get(gao_pos, 4); // 图像高度
		bitcount = get(bitcount_pos, 2);// bitcount
		st = bfoff;
		hang = (bitcount*kuan + 31) / 32 * 4; //一行占据的实际字节数
		if (bitcount != 8)
		{
			MessageBox(NULL, TEXT("图片不是单通道的bmp， 要求bitcount=8"), TEXT("错误"), MB_OK);
		}
		

		for (int i = 0; i < 256; i++)
		{
			histogram[i] = 0;
		}
		for (int i = 0; i < gao; i++)
		{
			for (int j = 0; j < kuan; j++)
			{
				long long tmp_hui = get(st + i*hang + j, 1);
				histogram[tmp_hui]++;
			}
		}
		
		for (int i = 0; i < 256; i++)
		{
			int tmp_hui =i;
			int b = get(54 + 4 * tmp_hui, 1);
			int g = get(54 + 4 * tmp_hui + 1, 1);
			int r = get(54 + 4 * tmp_hui + 2, 1);
			int nx = get(54 + 4 * tmp_hui + 3, 1);
			if (tmp_hui != b || b != r || b != g)
			{			
				MessageBox(NULL, TEXT("图片bmp的调色板有误，不是灰度图的调色板"), TEXT("错误"), MB_OK);	
			}
		}
		
		
		int sum = 0;
		//float bi[350 + 5];
		int bit = (1 << bitcount);
		for (int i = 0; i < bit; i++)
		{
			sum += histogram[i];
		}
		//float high = 0;
		for (int i = 0; i < bit; i++)
		{
			bi[i] = 1.0* histogram[i] / sum;
			//high = max(bi[i], high);
		}
		//cout << "st:" << st << " bitcount:" << bitcount << " kuan:" << kuan << " gao:" << gao << endl;
	}
	long long get(long long st, long long si)//从图像数据中得到从st开始的到st+si结束的数据，并且每1个字节进行反向（因为小为存储，反向后就是符合人逻辑的了）
	{
		long long s = 0;
		long long th = 0;
		for (int i = st + si - 1; i >= st; i--) // 字节之间小端存储
		{
			char tmp = yu[i];
			th = 0;
			for (int j = 7; j >= 0; j--) // 一个字节里是小端储存
			{
				s <<= 1;
				s += (tmp >> j) & 1;
			}
		}
		return s;
	}
	void show(long long st, long long si)// 打印得到的字节，帮助debug
	{
		printf(" %lld ", get(st, si));
	}
	void change(long long st, long long si, long long tmp)// 修改，将st到st+si处的数据变成tmp，此时输入的tmp是符合逻辑的顺序，此函数会将每隔1个字节反序后存入
	{

		for (int i = st; i<st + si; i++)
		{
			yu2[i] = 0;
			long long now = tmp % 256;
			tmp /= 256;
			for (int j = 0; j<8; j++)
			{
				yu2[i] += (((now >> (j)) & 1) << (j));
			}
		}
	}
	void show2(long long st) // 打印一个字节 debug用
	{
		printf(" %c ", yu[st]);
	}
	long long bit_trans(long long b, long long g, long long r) // rgb转灰度
	{
		return int(0.299*r + 0.587*g + 0.114*b)>255 ? 255 : int(0.299*r + 0.587*g + 0.114*b);
	}
	void open(CString tpath)
	{
		USES_CONVERSION;
		char *pa = T2A(tpath);
		FILE *fin = fopen(pa, "rb");
		cnt = 0;
		while (cnt<maxn && fread(yu+cnt, sizeof(char), 1, fin))
		{
			yu2[cnt] = yu[cnt]; cnt++;
		}
		if (cnt >= maxn)
		{
			MessageBox(NULL,TEXT( "图片太大"), TEXT("错误"),MB_OK);
			return;
		}
		fclose(fin);
	}
	bool save(CString tpath, int len = 271078)
	{
		if (len <54)
			return false;
		USES_CONVERSION;
		char *pa = T2A(tpath);
		FILE *fout = fopen(pa, "wb");
		for (int i = 0; i<len; i++)
		{
			fwrite(yu2 + i, sizeof(char), 1, fout);
		}
		
		fclose(fout);
		return true;
	}
	void trans_3_3(float k) // 第一次作业 （改变局部亮度的trans)
	{
		int gao_st = gao / 2;
		int kuan_st = kuan / 2;
		for (int i = 0; i < gao_st; i++)
		{
			for (int j = kuan_st; j < kuan; j++)
			{
				int b, g, r;// 小端序 顺序 蓝绿红
				b = get(st + i*hang + j * 3, 1);
				g = get(st + i*hang + j * 3+1, 1);
				r = get(st + i*hang + j * 3+2, 1);
			//	int Y, U, V;
			//	Y = ((66 * r + 129 * g + 25 * b + 128) >> 8) + 16;
			//	U = ((-38 * r - 74 * g + 112 * b + 128) >> 8) + 128;
			//	V = ((112 * r - 94 * g - 18 * b + 128) >> 8) + 128;
			//	Y *= (1 + k);
				b *= 1 + k;
				g *= 1 + k;
				r *= 1 + k;
				if (b > 255)b = 255;
				if (r > 255)r = 255;
				if (g > 255)g = 255;
				change(st + i*hang + j * 3, 1, b);
				change(st + i*hang + j * 3+1, 1, g);
				change(st + i*hang + j * 3+2, 1, r);
			}
		}
	}
	
	void trans_2() // 第二次作业 （直方图均衡化）
	{
		float now = 0;
		int used = -1;
		int pre = 0; int myst=0;
		int bit = (1 << bitcount);
		int mytran[256 + 50];
		for (int i = 0; i < bit; i++)
		{
			now += bi[i];
			while (now > 1.0*pre / 256)
			{
				pre++;
			}
			pre--;
			if (1.0*pre / 256 > now)
			{
				continue;
			}
			if (pre <= used)
			{
				continue;
			}
			else
			{
				used = pre;
				for (int j = myst; j <= i; j++)
				{
					if (pre > 255)
						pre = 255;
					mytran[j] = pre;
				}
				myst = i + 1;
			}
		}
		for (int i = myst; i < 256; i++)
		{
			mytran[i] = 255;
		}


		for (int i = 0; i < gao; i++)
		{
			for (int j = 0; j < kuan; j++)
			{
				long long yuan = get(st + i*hang + j, 1);
				if (yuan < 0 || yuan >255)
				{
					MessageBox(NULL, TEXT("变换出错"), TEXT("错误"), MB_OK);
				}
				long long xian = mytran[yuan];
				change(st + i*hang + j, 1, xian);
				
			}
		}
	}
};

