// Histogram_show.cpp : 实现文件
//

#include "stdafx.h"
#include "basic_imread.h"
#include "Histogram_show.h"
#include "afxdialogex.h"


// Histogram_show 对话框

IMPLEMENT_DYNAMIC(Histogram_show, CDialogEx)

Histogram_show::Histogram_show(float bi2[256 + 5])
{
	for (int i = 0; i < 256; i++)
	{
		bi[i] = bi2[i];
	}
	float high = 0;
	for (int i = 0; i < 256; i++)
	{
		//bi[i] = 1.0* histogram[i] / sum;
		high = max(bi[i], high);
	}
	for (int i = 0; i < 256; i++)
	{
			bi[i] = bi[i] / high;
	}
}

Histogram_show::Histogram_show(CWnd* pParent /*=NULL*/)
	: CDialogEx(IDD_DIALOG1, pParent)
{

}

Histogram_show::~Histogram_show()
{
}

void Histogram_show::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}
void Histogram_show::myshow()
{
	CClientDC dlgDC(this);
	const int maxnh = 200,maxnk=350,offh=4,offk=4,si=5;
	
	float cha = 1.0*maxnk / (1 << bitcount);
	for (int i = 0; i < maxnh; i++)
	{
		dlgDC.SetPixel(offk+0, offh+i, RGB(0, 0, 0));
	}
	for (int i = 0; i < maxnk; i++)
	{
		dlgDC.SetPixel(offk+i , offh+maxnh, RGB(0, 0, 0));
	}
	for (int i = 0; i < maxnk; i++)
	{
		int ti =int( 1.0*i/maxnk*256);
		if (ti < 0)ti = 0;
		if (ti > 255)ti = 255;
		for (int j = 0; j <= (int) maxnh*(bi[ti]); j++)
		{
			dlgDC.SetPixel(offk + i, maxnh-j+offh, RGB(255, 0, 0));
		}
	}
}

BEGIN_MESSAGE_MAP(Histogram_show, CDialogEx)
END_MESSAGE_MAP()


// Histogram_show 消息处理程序
