#include "ui.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

// 全局窗口句柄
void* g_ui_window = NULL;

// 窗口类名
#define WINDOW_CLASS_NAME "TaoBaoAutoBuyerClass"

// 窗口回调函数
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);

// 初始化用户界面
void init_ui(void) {
    // 注册窗口类
    WNDCLASSEX wc = {0};
    wc.cbSize        = sizeof(WNDCLASSEX);
    wc.style         = CS_HREDRAW | CS_VREDRAW;
    wc.lpfnWndProc   = WindowProc;
    wc.hInstance     = GetModuleHandle(NULL);
    wc.hCursor       = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW+1);
    wc.lpszClassName = WINDOW_CLASS_NAME;

    if (!RegisterClassEx(&wc)) {
        printf("注册窗口类失败\n");
        return;
    }

    // 创建窗口
    HWND hwnd = CreateWindowEx(
        0,
        WINDOW_CLASS_NAME,
        "淘宝自动购买器",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 500, 300,
        NULL, NULL, GetModuleHandle(NULL), NULL
    );

    if (!hwnd) {
        printf("创建窗口失败\n");
        UnregisterClass(WINDOW_CLASS_NAME, GetModuleHandle(NULL));
        return;
    }

    // 创建状态标签
    HWND status_label = CreateWindow(
        "STATIC",
        "初始化中...",
        WS_CHILD | WS_VISIBLE | SS_LEFT,
        20, 20, 460, 30,
        hwnd, NULL, GetModuleHandle(NULL), NULL
    );

    // 设置字体
    HFONT hFont = CreateFont(
        14, 0, 0, 0, FW_NORMAL,
        FALSE, FALSE, FALSE,
        DEFAULT_CHARSET,
        OUT_DEFAULT_PRECIS,
        CLIP_DEFAULT_PRECIS,
        DEFAULT_QUALITY,
        DEFAULT_PITCH | FF_SWISS,
        "微软雅黑"
    );
    SendMessage(status_label, WM_SETFONT, (WPARAM)hFont, TRUE);

    // 保存控件句柄到窗口用户数据
    SetWindowLongPtr(hwnd, GWLP_USERDATA, (LONG_PTR)status_label);

    // 显示窗口
    ShowWindow(hwnd, SW_SHOWNORMAL);
    UpdateWindow(hwnd);

    // 设置全局窗口句柄
    g_ui_window = hwnd;
}

// 清理用户界面
void cleanup_ui(void) {
    if (g_ui_window) {
        // 获取状态标签句柄
        HWND status_label = (HWND)GetWindowLongPtr((HWND)g_ui_window, GWLP_USERDATA);
        
        // 获取字体并释放
        HFONT hFont = (HFONT)SendMessage(status_label, WM_GETFONT, 0, 0);
        if (hFont) {
            DeleteObject(hFont);
        }
        
        // 销毁窗口
        DestroyWindow((HWND)g_ui_window);
        
        // 注销窗口类
        UnregisterClass(WINDOW_CLASS_NAME, GetModuleHandle(NULL));
        
        g_ui_window = NULL;
    }
}

// 更新UI状态
void update_ui_status(const char* message) {
    if (g_ui_window) {
        HWND status_label = (HWND)GetWindowLongPtr((HWND)g_ui_window, GWLP_USERDATA);
        if (status_label) {
            SetWindowText(status_label, message ? message : "");
        }
        
        // 处理窗口消息，确保UI更新
        MSG msg;
        while (PeekMessage(&msg, (HWND)g_ui_window, 0, 0, PM_REMOVE)) {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
    }
}

// 显示错误消息
void show_error(const char* title, const char* message) {
    MessageBox(NULL, message ? message : "未知错误", title ? title : "错误", MB_ICONERROR | MB_OK);
}

// 显示信息消息
void show_info(const char* title, const char* message) {
    MessageBox(NULL, message ? message : "", title ? title : "信息", MB_ICONINFORMATION | MB_OK);
}

// 窗口回调函数
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;
        
        case WM_CLOSE:
            // 询问用户是否确认退出
            if (MessageBox(hwnd, "确定要退出程序吗？", "确认退出", MB_YESNO | MB_ICONQUESTION) == IDYES) {
                DestroyWindow(hwnd);
            }
            return 0;
        
        default:
            return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
}