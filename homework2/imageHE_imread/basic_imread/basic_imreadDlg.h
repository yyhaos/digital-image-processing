
// basic_imreadDlg.h : 头文件
//

#pragma once
#include "afxwin.h"
#include "mytran.h"
#include <iostream>
#include "Histogram_show.h"
using namespace std;
// Cbasic_imreadDlg 对话框
class Cbasic_imreadDlg : public CDialogEx
{
// 构造
public:
	Cbasic_imreadDlg(CWnd* pParent = NULL)
	;	// 标准构造函数

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_BASIC_IMREAD_DIALOG };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV 支持


// 实现
protected:
	HICON m_hIcon;

	// 生成的消息映射函数
	virtual BOOL OnInitDialog();
	void ShowIniImage(int IDC_tmp);
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	CStatic tmp_pic;
	Histogram_show *m_pTipDlg;
	int fth = 1;
	int fi=0;
	CString path;
	mytran ttr;
	afx_msg
		void OnBnClickedOk();
	void ShowImage(CString path, int IDC_tmp);
	//void ShowImage(CString path, HWND IDC_tmp);
	void OnBnClickedOpen();
	afx_msg void OnBnClickedChange();
	//void OnNMCustomdrawSlider1(NMHDR * pNMHDR, LRESULT * pResult);
	// 调亮k倍
	int t_k;
	// k文本表示
	//CString t_kkk;
	// k的显示
	CString t_kk;
	//afx_msg void OnStnClickedStatictext();
	//afx_msg void OnTRBNThumbPosChangingSlider1(NMHDR *pNMHDR, LRESULT *pResult);
	afx_msg void OnNMReleasedcaptureSlider1(NMHDR *pNMHDR, LRESULT *pResult);
	afx_msg void OnBnClickedSave();
	afx_msg void OnBnClickedButton1();
};

