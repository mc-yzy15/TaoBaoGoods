#include "browser.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

typedef struct {
    int reserved;
} BrowserDriver;

static char* duplicate_string(const char* value) {
    size_t length;
    char* copy;

    if (!value) {
        return NULL;
    }

    length = strlen(value) + 1;
    copy = (char*)malloc(length);
    if (!copy) {
        return NULL;
    }

    memcpy(copy, value, length);
    return copy;
}

static bool prompt_manual_confirmation(const char* message) {
    char buffer[16];

    printf("%s\n", message);
    printf("输入 y 确认已完成，其他任意输入取消: ");
    if (!fgets(buffer, sizeof(buffer), stdin)) {
        return false;
    }

    return buffer[0] == 'y' || buffer[0] == 'Y';
}

Browser* browser_init(const char* window_size, const char* proxy, const char* driver_path) {
    Browser* browser = (Browser*)calloc(1, sizeof(Browser));
    BrowserDriver* driver;

    if (!browser) {
        return NULL;
    }

    browser->window_size = duplicate_string(window_size ? window_size : "1280,720");
    browser->proxy = duplicate_string(proxy ? proxy : "");
    browser->driver_path = duplicate_string(driver_path ? driver_path : "chromedriver.exe");

    driver = (BrowserDriver*)calloc(1, sizeof(BrowserDriver));
    if (!driver) {
        browser_cleanup(browser);
        return NULL;
    }

    browser->driver = driver;
    printf("当前 C 版本处于实验性手动辅助模式，不再尝试自动控制浏览器。\n");
    return browser;
}

void browser_cleanup(Browser* browser) {
    if (!browser) {
        return;
    }

    free(browser->driver);
    free(browser->window_size);
    free(browser->proxy);
    free(browser->driver_path);
    free(browser);
}

bool browser_login(Browser* browser, const char* username, const char* password) {
    if (!browser) {
        return false;
    }

    ShellExecute(NULL, "open", "https://login.taobao.com", NULL, NULL, SW_SHOWNORMAL);
    printf("用户名: %s\n", username ? username : "(空)");
    if (password && password[0] != '\0') {
        printf("密码已省略显示。\n");
    }
    return prompt_manual_confirmation("请在浏览器中手动完成登录。");
}

bool browser_add_to_cart(Browser* browser, const char* url, int quantity) {
    if (!browser || !url) {
        return false;
    }

    ShellExecute(NULL, "open", url, NULL, NULL, SW_SHOWNORMAL);
    printf("目标商品: %s\n", url);
    printf("计划数量: %d\n", quantity);
    return prompt_manual_confirmation("请在浏览器中手动完成加购。");
}

bool browser_checkout(Browser* browser) {
    if (!browser) {
        return false;
    }

    ShellExecute(NULL, "open", "https://cart.taobao.com/cart.htm", NULL, NULL, SW_SHOWNORMAL);
    return prompt_manual_confirmation("请在浏览器中手动完成结算前确认。");
}

bool browser_place_order(Browser* browser) {
    if (!browser) {
        return false;
    }

    return prompt_manual_confirmation("请在浏览器中手动确认订单并提交。");
}

bool browser_navigate(Browser* browser, const char* url) {
    if (!browser || !url) {
        return false;
    }

    ShellExecute(NULL, "open", url, NULL, NULL, SW_SHOWNORMAL);
    return true;
}

bool browser_find_element(Browser* browser, const char* element_id, void** element) {
    (void)browser;
    (void)element_id;
    if (element) {
        *element = NULL;
    }
    printf("browser_find_element 未实现，C 版本仅保留手动辅助能力。\n");
    return false;
}

bool browser_click_element(void* element) {
    (void)element;
    printf("browser_click_element 未实现，C 版本仅保留手动辅助能力。\n");
    return false;
}

bool browser_send_keys(void* element, const char* text) {
    (void)element;
    (void)text;
    printf("browser_send_keys 未实现，C 版本仅保留手动辅助能力。\n");
    return false;
}

bool browser_wait_for_element(Browser* browser, const char* element_id, int timeout_ms) {
    (void)browser;
    (void)element_id;
    if (timeout_ms > 0) {
        Sleep((DWORD)timeout_ms);
    }
    printf("browser_wait_for_element 未实现，C 版本仅保留手动辅助能力。\n");
    return false;
}
