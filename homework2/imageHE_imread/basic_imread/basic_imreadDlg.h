
// basic_imreadDlg.h : ͷ�ļ�
//

#pragma once
#include "afxwin.h"
#include "mytran.h"
#include <iostream>
#include "Histogram_show.h"
using namespace std;
// Cbasic_imreadDlg �Ի���
class Cbasic_imreadDlg : public CDialogEx
{
// ����
public:
	Cbasic_imreadDlg(CWnd* pParent = NULL)
	;	// ��׼���캯��

// �Ի�������
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_BASIC_IMREAD_DIALOG };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV ֧��


// ʵ��
protected:
	HICON m_hIcon;

	// ���ɵ���Ϣӳ�亯��
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
	// ����k��
	int t_k;
	// k�ı���ʾ
	//CString t_kkk;
	// k����ʾ
	CString t_kk;
	//afx_msg void OnStnClickedStatictext();
	//afx_msg void OnTRBNThumbPosChangingSlider1(NMHDR *pNMHDR, LRESULT *pResult);
	afx_msg void OnNMReleasedcaptureSlider1(NMHDR *pNMHDR, LRESULT *pResult);
	afx_msg void OnBnClickedSave();
	afx_msg void OnBnClickedButton1();
};

