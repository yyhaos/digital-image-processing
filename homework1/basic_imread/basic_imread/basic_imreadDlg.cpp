
// basic_imreadDlg.cpp : ʵ���ļ�
//

#include "stdafx.h"
#include "basic_imread.h"
#include "basic_imreadDlg.h"
#include "afxdialogex.h"


#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// ����Ӧ�ó��򡰹��ڡ��˵���� CAboutDlg �Ի���

char mytran::yu[maxn + 5] = { 0 };
char mytran::yu2[maxn + 5] = { 0 };
class CAboutDlg : public CDialogEx
{
public:
	CAboutDlg();

// �Ի�������
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_ABOUTBOX };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV ֧��

// ʵ��
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


// Cbasic_imreadDlg �Ի���



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


// Cbasic_imreadDlg ��Ϣ�������

BOOL Cbasic_imreadDlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// ��������...���˵�����ӵ�ϵͳ�˵��С�

	// IDM_ABOUTBOX ������ϵͳ���Χ�ڡ�
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

	// ���ô˶Ի����ͼ�ꡣ  ��Ӧ�ó��������ڲ��ǶԻ���ʱ����ܽ��Զ�
	//  ִ�д˲���
	SetIcon(m_hIcon, TRUE);			// ���ô�ͼ��
	SetIcon(m_hIcon, FALSE);		// ����Сͼ��

	// TODO: �ڴ���Ӷ���ĳ�ʼ������
	fi = 1;
	

	return TRUE;  // ���ǽ��������õ��ؼ������򷵻� TRUE
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

// �����Ի��������С����ť������Ҫ����Ĵ���
//  �����Ƹ�ͼ�ꡣ  ����ʹ���ĵ�/��ͼģ�͵� MFC Ӧ�ó���
//  �⽫�ɿ���Զ���ɡ�

void Cbasic_imreadDlg::OnPaint()
{
	if(fi==1)
		ShowIniImage(IDC_Main);
	fi = 0;
	CDialogEx::OnPaint();
	if (IsIconic())
	{
		CPaintDC dc(this); // ���ڻ��Ƶ��豸������

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// ʹͼ���ڹ����������о���
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// ����ͼ��
		dc.DrawIcon(x, y, m_hIcon);


	}
	else
	{
		
		
	}
}

//���û��϶���С������ʱϵͳ���ô˺���ȡ�ù��
//��ʾ��
HCURSOR Cbasic_imreadDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}



void Cbasic_imreadDlg::OnBnClickedOk()
{
	// TODO: �ڴ���ӿؼ�֪ͨ����������

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
	CString defaultDir = _T("D:\\video"); //����Ĭ�ϴ��ļ���
	CString fileFilter = _T("�ļ�(*.jpg;*.bmp)|*.jpg;*.bmp|All File (*.*)|*.*||"); //�����ļ�����
	CFileDialog fileDlg(true, defaultDir, _T(""), OFN_HIDEREADONLY | OFN_OVERWRITEPROMPT, fileFilter, NULL);
	fileDlg.m_ofn.lpstrTitle = _T("Open Image");
	if (fileDlg.DoModal() != IDOK)
		return;
	path = fileDlg.GetPathName();
	path.Replace(_T("//"), _T("////"));
	
	ShowImage(path, IDC_Main);
	UpdateData();
	
	// TODO: �ڴ���ӿؼ�֪ͨ����������
}


void Cbasic_imreadDlg::OnBnClickedChange()
{
	if (path == "")
	{
		MessageBox(TEXT("�����ȴ�bmpͼƬ"),TEXT( "����"), MB_OK);
		return;
	}
	//mytrans ttr;
	ttr.open(path);
	ttr.init();
	ttr.trans_3_3(1.0*t_k / 50.0);
	
	CString tmp("yyh.bmp");
	ttr.save(tmp, ttr.bfsize);
	ShowImage(tmp, IDC_Main);
	// TODO: �ڴ���ӿؼ�֪ͨ����������
}


void Cbasic_imreadDlg::OnNMReleasedcaptureSlider1(NMHDR *pNMHDR, LRESULT *pResult)
{
	// TODO: �ڴ���ӿؼ�֪ͨ����������
	*pResult = 0;
	UpdateData(TRUE);
	t_kk.Format(_T("%.2f"),1.0*t_k/50.0);
	UpdateData(FALSE);
}


void Cbasic_imreadDlg::OnBnClickedSave()
{
	CString tt("������exeͬһĿ¼�£��ļ���");
	CString tnum;
	tnum.Format(_T("%d"), fth);
	CString ed(".bmp");
	tt = tt + tnum + ed;
	if (ttr.save(tnum + ed, ttr.bfsize))
	{
		MessageBox(tt, TEXT("����ͼƬ"), MB_OK);
		fth++;
	}
	else 
		MessageBox(TEXT("����ʧ�ܣ������´�ͼƬ"), TEXT("����ͼƬ"), MB_OK);
	
	// TODO: �ڴ���ӿؼ�֪ͨ����������
}
