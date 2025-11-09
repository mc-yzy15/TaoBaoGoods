#ifndef CONFIG_H
#define CONFIG_H

// 商品结构
typedef struct {
    char* url;
    int quantity;
} Item;

// 配置结构
typedef struct {
    char* window_size;
    char* proxy;
    char* driver_path;
    char* username;
    char* password;
    Item* items;
    int item_count;
} Config;

// 函数声明
Config* config_load(const char* file_path);
void config_cleanup(Config* config);
void config_create_default(const char* file_path);

#endif // CONFIG_H