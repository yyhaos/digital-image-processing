#pragma once


// Histogram_show �Ի���

class Histogram_show : public CDialogEx
{
	DECLARE_DYNAMIC(Histogram_show)

public:
	
	Histogram_show(float[256 + 5]);
	Histogram_show(CWnd* pParent = NULL);   // ��׼���캯��
	virtual ~Histogram_show();
	int bitcount;
	float bi[256 + 5];
	void myshow();

// �Ի�������
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_DIALOG1 };
#endif

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV ֧��

	DECLARE_MESSAGE_MAP()
};
