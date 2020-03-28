#pragma once


// Histogram_show 对话框

class Histogram_show : public CDialogEx
{
	DECLARE_DYNAMIC(Histogram_show)

public:
	
	Histogram_show(float[256 + 5]);
	Histogram_show(CWnd* pParent = NULL);   // 标准构造函数
	virtual ~Histogram_show();
	int bitcount;
	float bi[256 + 5];
	void myshow();

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_DIALOG1 };
#endif

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 支持

	DECLARE_MESSAGE_MAP()
};
