
// basic_imread.h : PROJECT_NAME Ӧ�ó������ͷ�ļ�
//

#pragma once

#ifndef __AFXWIN_H__
	#error "�ڰ������ļ�֮ǰ������stdafx.h�������� PCH �ļ�"
#endif

#include "resource.h"		// ������


// Cbasic_imreadApp: 
// �йش����ʵ�֣������ basic_imread.cpp
//

class Cbasic_imreadApp : public CWinApp
{
public:
	Cbasic_imreadApp();

// ��д
public:
	virtual BOOL InitInstance();

// ʵ��

	DECLARE_MESSAGE_MAP()
};

extern Cbasic_imreadApp theApp;