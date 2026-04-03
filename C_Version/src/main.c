#include <stdio.h>
#include <windows.h>

#include "browser.h"
#include "config.h"
#include "ui.h"

static void update_status(const char* message) {
    SYSTEMTIME st;

    GetLocalTime(&st);
    printf(
        "[%04d-%02d-%02d %02d:%02d:%02d] %s\n",
        st.wYear,
        st.wMonth,
        st.wDay,
        st.wHour,
        st.wMinute,
        st.wSecond,
        message ? message : ""
    );

    if (g_ui_window) {
        update_ui_status(message);
    }
}

static void run_taobao_buyer(Config* config) {
    Browser* browser = browser_init(config->window_size, config->proxy, config->driver_path);
    int index;

    if (!browser) {
        update_status("浏览器辅助模块初始化失败。");
        return;
    }

    update_status("等待手动登录确认...");
    if (!browser_login(browser, config->username, config->password)) {
        update_status("登录步骤未确认，流程结束。");
        browser_cleanup(browser);
        return;
    }

    for (index = 0; index < config->item_count; index++) {
        update_status("等待手动加购确认...");
        if (!browser_add_to_cart(browser, config->items[index].url, config->items[index].quantity)) {
            update_status("加购步骤未确认，流程结束。");
            browser_cleanup(browser);
            return;
        }
    }

    update_status("等待手动结算确认...");
    if (!browser_checkout(browser)) {
        update_status("结算步骤未确认，流程结束。");
        browser_cleanup(browser);
        return;
    }

    update_status("等待手动提交订单确认...");
    if (!browser_place_order(browser)) {
        update_status("提交订单步骤未确认，流程结束。");
        browser_cleanup(browser);
        return;
    }

    update_status("实验性手动辅助流程完成。");
    browser_cleanup(browser);
}

int main(int argc, char* argv[]) {
    const char* config_path = "DefaultConfig.txt";
    Config* config;
    int index;

    if (argc > 1) {
        config_path = argv[1];
    }

    config = config_load(config_path);
    if (!config) {
        printf("加载配置文件失败: %s\n", config_path);
        return 1;
    }

    printf("TaoBaoGoods C Version\n");
    printf("状态: 实验性手动辅助原型\n");
    printf("配置文件: %s\n", config_path);
    printf("窗口大小: %s\n", config->window_size ? config->window_size : "");
    printf("代理: %s\n", config->proxy ? config->proxy : "");
    printf("驱动路径: %s\n", config->driver_path ? config->driver_path : "");
    printf("商品数量: %d\n", config->item_count);
    for (index = 0; index < config->item_count; index++) {
        printf("商品 %d: %s x %d\n", index + 1, config->items[index].url, config->items[index].quantity);
    }

    init_ui();
    update_status("C 版本已启动，等待手动辅助流程。");
    run_taobao_buyer(config);

    printf("\n程序执行完成，按回车键退出...");
    getchar();

    cleanup_ui();
    config_cleanup(config);
    return 0;
}
