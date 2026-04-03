#include "ui.h"

#include <stdio.h>
#include <windows.h>

void* g_ui_window = NULL;

#define WINDOW_CLASS_NAME "TaoBaoAutoBuyerClass"

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);

void init_ui(void) {
    WNDCLASSEX wc = {0};
    HWND hwnd;
    HWND status_label;
    HFONT font;

    wc.cbSize = sizeof(WNDCLASSEX);
    wc.style = CS_HREDRAW | CS_VREDRAW;
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = GetModuleHandle(NULL);
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.lpszClassName = WINDOW_CLASS_NAME;

    if (!RegisterClassEx(&wc)) {
        printf("注册窗口类失败\n");
        return;
    }

    hwnd = CreateWindowEx(
        0,
        WINDOW_CLASS_NAME,
        "TaoBaoGoods C Experimental Helper",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT,
        CW_USEDEFAULT,
        560,
        280,
        NULL,
        NULL,
        GetModuleHandle(NULL),
        NULL
    );

    if (!hwnd) {
        printf("创建窗口失败\n");
        UnregisterClass(WINDOW_CLASS_NAME, GetModuleHandle(NULL));
        return;
    }

    status_label = CreateWindow(
        "STATIC",
        "初始化中...",
        WS_CHILD | WS_VISIBLE | SS_LEFT,
        20,
        20,
        500,
        60,
        hwnd,
        NULL,
        GetModuleHandle(NULL),
        NULL
    );

    font = CreateFont(
        16,
        0,
        0,
        0,
        FW_NORMAL,
        FALSE,
        FALSE,
        FALSE,
        DEFAULT_CHARSET,
        OUT_DEFAULT_PRECIS,
        CLIP_DEFAULT_PRECIS,
        DEFAULT_QUALITY,
        DEFAULT_PITCH | FF_SWISS,
        "Microsoft YaHei UI"
    );
    SendMessage(status_label, WM_SETFONT, (WPARAM)font, TRUE);

    SetWindowLongPtr(hwnd, GWLP_USERDATA, (LONG_PTR)status_label);
    ShowWindow(hwnd, SW_SHOWNORMAL);
    UpdateWindow(hwnd);
    g_ui_window = hwnd;
}

void cleanup_ui(void) {
    if (g_ui_window) {
        HWND status_label = (HWND)GetWindowLongPtr((HWND)g_ui_window, GWLP_USERDATA);
        HFONT font = (HFONT)SendMessage(status_label, WM_GETFONT, 0, 0);
        if (font) {
            DeleteObject(font);
        }

        DestroyWindow((HWND)g_ui_window);
        UnregisterClass(WINDOW_CLASS_NAME, GetModuleHandle(NULL));
        g_ui_window = NULL;
    }
}

void update_ui_status(const char* message) {
    if (g_ui_window) {
        HWND status_label = (HWND)GetWindowLongPtr((HWND)g_ui_window, GWLP_USERDATA);
        MSG msg;

        if (status_label) {
            SetWindowText(status_label, message ? message : "");
        }

        while (PeekMessage(&msg, (HWND)g_ui_window, 0, 0, PM_REMOVE)) {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
    }
}

void show_error(const char* title, const char* message) {
    MessageBox(NULL, message ? message : "未知错误", title ? title : "错误", MB_ICONERROR | MB_OK);
}

void show_info(const char* title, const char* message) {
    MessageBox(NULL, message ? message : "", title ? title : "信息", MB_ICONINFORMATION | MB_OK);
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    (void)wParam;
    (void)lParam;

    switch (uMsg) {
        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;
        case WM_CLOSE:
            if (MessageBox(hwnd, "确定要退出程序吗？", "确认退出", MB_YESNO | MB_ICONQUESTION) == IDYES) {
                DestroyWindow(hwnd);
            }
            return 0;
        default:
            return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
}
