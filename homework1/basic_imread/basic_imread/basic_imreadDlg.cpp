
// basic_imreadDlg.cpp : 实现文件
//

#include "stdafx.h"
#include "basic_imread.h"
#include "basic_imreadDlg.h"
#include "afxdialogex.h"


#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// 用于应用程序“关于”菜单项的 CAboutDlg 对话框

char mytran::yu[maxn + 5] = { 0 };
char mytran::yu2[maxn + 5] = { 0 };
class CAboutDlg : public CDialogEx
{
public:
	CAboutDlg();

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_ABOUTBOX };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 支持

// 实现
protected:
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialogEx(IDD_ABOUTBOX)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialogEx)
END_MESSAGE_MAP()


// Cbasic_imreadDlg 对话框



Cbasic_imreadDlg::Cbasic_imreadDlg(CWnd* pParent /*=NULL*/)
	: CDialogEx(IDD_BASIC_IMREAD_DIALOG, pParent)
	, t_k(25)
	//, t_kkk(_T(""))
	//, t_kkk(_T(""))
	, t_kk(_T("0.5"))
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void Cbasic_imreadDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	//	DDX_Control(pDX, IDC_TMP, tmp_pic);
	DDX_Slider(pDX, IDC_SLIDER1, t_k);
	DDV_MinMaxInt(pDX, t_k, 0,100);
	//DDX_Text(pDX, IDC_EDIT2, t_kkk);
	//DDX_Text(pDX, IDC_EDIT2, t_kkk);
	DDX_Text(pDX, IDC_STATICTEXT, t_kk);
}

BEGIN_MESSAGE_MAP(Cbasic_imreadDlg, CDialogEx)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_BN_CLICKED(IDOK, &Cbasic_imreadDlg::OnBnClickedOk)
	ON_BN_CLICKED(IDOPEN, &Cbasic_imreadDlg::OnBnClickedOpen)
	ON_BN_CLICKED(IDCHANGE, &Cbasic_imreadDlg::OnBnClickedChange)
	ON_NOTIFY(NM_RELEASEDCAPTURE, IDC_SLIDER1, &Cbasic_imreadDlg::OnNMReleasedcaptureSlider1)
	ON_BN_CLICKED(IDSAVE, &Cbasic_imreadDlg::OnBnClickedSave)
END_MESSAGE_MAP()


// Cbasic_imreadDlg 消息处理程序

BOOL Cbasic_imreadDlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// 将“关于...”菜单项添加到系统菜单中。

	// IDM_ABOUTBOX 必须在系统命令范围内。
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		BOOL bNameValid;
		CString strAboutMenu;
		bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
		ASSERT(bNameValid);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// 设置此对话框的图标。  当应用程序主窗口不是对话框时，框架将自动
	//  执行此操作
	SetIcon(m_hIcon, TRUE);			// 设置大图标
	SetIcon(m_hIcon, FALSE);		// 设置小图标

	// TODO: 在此添加额外的初始化代码
	fi = 1;
	

	return TRUE;  // 除非将焦点设置到控件，否则返回 TRUE
}
void Cbasic_imreadDlg::ShowIniImage(int IDC_tmp)
{
	CBitmap startbmp;
	HBITMAP hbmp;
	//tmp_pic = (CStatic)GetDlgItem(IDC_Main);
	startbmp.LoadBitmapW(IDB_BITMAP1);
	hbmp = (HBITMAP)startbmp.GetSafeHandle();
	//tmp_pic.SetBitmap(hbmp);
	CStatic *pStatic = (CStatic*)GetDlgItem(IDC_tmp);
	pStatic->SetBitmap(hbmp);
}
void Cbasic_imreadDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialogEx::OnSysCommand(nID, lParam);
	}
}

// 如果向对话框添加最小化按钮，则需要下面的代码
//  来绘制该图标。  对于使用文档/视图模型的 MFC 应用程序，
//  这将由框架自动完成。

void Cbasic_imreadDlg::OnPaint()
{
	if(fi==1)
		ShowIniImage(IDC_Main);
	fi = 0;
	CDialogEx::OnPaint();
	if (IsIconic())
	{
		CPaintDC dc(this); // 用于绘制的设备上下文

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// 使图标在工作区矩形中居中
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// 绘制图标
		dc.DrawIcon(x, y, m_hIcon);


	}
	else
	{
		
		
	}
}

//当用户拖动最小化窗口时系统调用此函数取得光标
//显示。
HCURSOR Cbasic_imreadDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}



void Cbasic_imreadDlg::OnBnClickedOk()
{
	// TODO: 在此添加控件通知处理程序代码

	CDialogEx::OnOK();
}

void Cbasic_imreadDlg::ShowImage(CString path, int IDC_tmp)
{
	UpdateWindow();
	CDC *pDc = GetDlgItem(IDC_tmp)->GetDC();
	CStatic *pStatic = (CStatic*)GetDlgItem(IDC_tmp);
	pStatic->SetBitmap(NULL);
	CRect rect;
	GetClientRect(&rect);
	HBITMAP m_hBitmap = (HBITMAP)::LoadImage(NULL, path, IMAGE_BITMAP, 0, 0, LR_LOADFROMFILE);
	CBitmap m_Bitmap;
	m_Bitmap.Attach(m_hBitmap);
	CDC MemDc;
	MemDc.CreateCompatibleDC(pDc);
	MemDc.SelectObject(&m_Bitmap);
	pDc->BitBlt(0, 0, rect.Width(), rect.Height(), &MemDc, 0, 0, SRCCOPY);
	
}

void Cbasic_imreadDlg::OnBnClickedOpen()
{
	CBitmap bitmap;
	HBITMAP hbmp;
	CString defaultDir = _T("D:\\video"); //设置默认打开文件夹
	CString fileFilter = _T("文件(*.jpg;*.bmp)|*.jpg;*.bmp|All File (*.*)|*.*||"); //设置文件过滤
	CFileDialog fileDlg(true, defaultDir, _T(""), OFN_HIDEREADONLY | OFN_OVERWRITEPROMPT, fileFilter, NULL);
	fileDlg.m_ofn.lpstrTitle = _T("Open Image");
	if (fileDlg.DoModal() != IDOK)
		return;
	path = fileDlg.GetPathName();
	path.Replace(_T("//"), _T("////"));
	
	ShowImage(path, IDC_Main);
	UpdateData();
	
	// TODO: 在此添加控件通知处理程序代码
}


void Cbasic_imreadDlg::OnBnClickedChange()
{
	if (path == "")
	{
		MessageBox(TEXT("必须先打开bmp图片"),TEXT( "错误"), MB_OK);
		return;
	}
	//mytrans ttr;
	ttr.open(path);
	ttr.init();
	ttr.trans_3_3(1.0*t_k / 50.0);
	
	CString tmp("yyh.bmp");
	ttr.save(tmp, ttr.bfsize);
	ShowImage(tmp, IDC_Main);
	// TODO: 在此添加控件通知处理程序代码
}


void Cbasic_imreadDlg::OnNMReleasedcaptureSlider1(NMHDR *pNMHDR, LRESULT *pResult)
{
	// TODO: 在此添加控件通知处理程序代码
	*pResult = 0;
	UpdateData(TRUE);
	t_kk.Format(_T("%.2f"),1.0*t_k/50.0);
	UpdateData(FALSE);
}


void Cbasic_imreadDlg::OnBnClickedSave()
{
	CString tt("保存在exe同一目录下，文件名");
	CString tnum;
	tnum.Format(_T("%d"), fth);
	CString ed(".bmp");
	tt = tt + tnum + ed;
	if (ttr.save(tnum + ed, ttr.bfsize))
	{
		MessageBox(tt, TEXT("保存图片"), MB_OK);
		fth++;
	}
	else 
		MessageBox(TEXT("保存失败，请重新打开图片"), TEXT("保存图片"), MB_OK);
	
	// TODO: 在此添加控件通知处理程序代码
}
