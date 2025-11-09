#ifndef BROWSER_H
#define BROWSER_H

// 浏览器结构
typedef struct {
    void* driver;
    char* window_size;
    char* proxy;
    char* driver_path;
} Browser;

// 函数声明
browser* browser_init(const char* window_size, const char* proxy, const char* driver_path);
void browser_cleanup(Browser* browser);
bool browser_login(Browser* browser, const char* username, const char* password);
bool browser_add_to_cart(Browser* browser, const char* url, int quantity);
bool browser_checkout(Browser* browser);
bool browser_place_order(Browser* browser);
bool browser_navigate(Browser* browser, const char* url);
bool browser_find_element(Browser* browser, const char* element_id, void** element);
bool browser_click_element(void* element);
bool browser_send_keys(void* element, const char* text);
bool browser_wait_for_element(Browser* browser, const char* element_id, int timeout_ms);

#endif // BROWSER_H