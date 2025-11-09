#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <windows.h>
#include "config.h"
#include "browser.h"
#include "ui.h"

// 全局状态更新函数
void update_status(const char* message) {
    SYSTEMTIME st;
    GetLocalTime(&st);
    printf("[%04d-%02d-%02d %02d:%02d:%02d] - %s\n", 
           st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond, message);
    if (g_ui_window) {
        update_ui_status(message);
    }
}

// 主程序逻辑
void run_taobao_buyer(Config* config) {
    // 初始化浏览器
    Browser* browser = browser_init(config->window_size, config->proxy, config->driver_path);
    if (!browser) {
        update_status("浏览器初始化失败");
        return;
    }

    // 登录过程
    update_status("正在登录...");
    if (!browser_login(browser, config->username, config->password)) {
        update_status("登录失败");
        browser_cleanup(browser);
        return;
    }
    update_status("登录成功");

    // 添加商品到购物车
    for (int i = 0; i < config->item_count; i++) {
        update_status("正在添加商品到购物车...");
        if (!browser_add_to_cart(browser, config->items[i].url, config->items[i].quantity)) {
            update_status("添加商品到购物车失败");
            browser_cleanup(browser);
            return;
        }
        update_status("商品已添加到购物车");
    }

    // 结算
    update_status("正在结算...");
    if (!browser_checkout(browser)) {
        update_status("结算失败");
        browser_cleanup(browser);
        return;
    }
    update_status("结算成功");

    // 提交订单
    update_status("正在提交订单...");
    if (!browser_place_order(browser)) {
        update_status("提交订单失败");
        browser_cleanup(browser);
        return;
    }
    update_status("订单提交成功");

    // 清理资源
    browser_cleanup(browser);
}

// 主函数
int main(int argc, char* argv[]) {
    // 设置默认配置文件路径
    const char* config_path = "DefaultConfig.txt";
    if (argc > 1) {
        config_path = argv[1];
    }

    // 初始化配置
    Config* config = config_load(config_path);
    if (!config) {
        printf("加载配置文件失败: %s\n", config_path);
        return 1;
    }

    // 打印配置信息（除了密码）
    printf("配置信息:\n");
    printf("窗口大小: %s\n", config->window_size);
    printf("代理: %s\n", config->proxy);
    printf("驱动路径: %s\n", config->driver_path);
    printf("用户名: %s\n", config->username);
    printf("商品数量: %d\n", config->item_count);
    for (int i = 0; i < config->item_count; i++) {
        printf("商品 %d: %s (数量: %d)\n", i + 1, config->items[i].url, config->items[i].quantity);
    }

    // 初始化UI
    init_ui();
    update_status("程序已启动");

    // 运行淘宝购买器
    run_taobao_buyer(config);

    // 等待用户输入
    printf("\n程序执行完成，按回车键退出...");
    getchar();

    // 清理资源
    config_cleanup(config);
    cleanup_ui();

    return 0;
}