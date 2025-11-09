#include "config.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 最大行长度
#define MAX_LINE_LENGTH 1024

// 最大商品数量
#define MAX_ITEMS 100

// 创建默认配置文件
void config_create_default(const char* file_path) {
    FILE* file = fopen(file_path, "w");
    if (!file) {
        printf("创建默认配置文件失败: %s\n", file_path);
        return;
    }

    fprintf(file, "# 淘宝自动购买器配置文件\n");
    fprintf(file, "window_size=1280,720\n");
    fprintf(file, "proxy=\n");
    fprintf(file, "driver_path=chromedriver.exe\n");
    fprintf(file, "username=your_username\n");
    fprintf(file, "password=your_password\n");
    fprintf(file, "# 商品列表，每行一个商品，格式: item_url:quantity\n");
    fprintf(file, "item=https://example.com/item1:1\n");
    fprintf(file, "item=https://example.com/item2:2\n");

    fclose(file);
    printf("默认配置文件已创建: %s\n", file_path);
}

// 解析配置文件中的键值对
void parse_key_value(char* line, char** key, char** value) {
    char* equals = strchr(line, '=');
    if (!equals) {
        *key = NULL;
        *value = NULL;
        return;
    }

    *equals = '\0';
    *key = strdup(line);
    *value = strdup(equals + 1);

    // 去除值两端的空白字符
    char* val = *value;
    while (*val <= ' ') val++;
    char* end = val + strlen(val) - 1;
    while (end > val && *end <= ' ') end--;
    *(end + 1) = '\0';

    *value = strdup(val);
    free(val - (strlen(*value) - strlen(val)));
}

// 解析商品行
void parse_item_line(char* line, Item* item) {
    // 跳过 "item=" 前缀
    char* content = strstr(line, "=") + 1;
    char* colon = strchr(content, ':');
    if (!colon) {
        item->url = strdup(content);
        item->quantity = 1;
        return;
    }

    *colon = '\0';
    item->url = strdup(content);
    item->quantity = atoi(colon + 1);
}

// 加载配置文件
Config* config_load(const char* file_path) {
    // 检查文件是否存在，如果不存在则创建默认配置
    FILE* file = fopen(file_path, "r");
    if (!file) {
        printf("配置文件不存在，创建默认配置...\n");
        config_create_default(file_path);
        file = fopen(file_path, "r");
        if (!file) {
            printf("创建默认配置后仍无法打开文件: %s\n", file_path);
            return NULL;
        }
    }

    // 分配配置结构
    Config* config = (Config*)malloc(sizeof(Config));
    if (!config) {
        fclose(file);
        return NULL;
    }

    // 初始化默认值
    config->window_size = strdup("1280,720");
    config->proxy = strdup("");
    config->driver_path = strdup("chromedriver.exe");
    config->username = strdup("your_username");
    config->password = strdup("your_password");
    config->items = (Item*)malloc(sizeof(Item) * MAX_ITEMS);
    config->item_count = 0;

    // 读取并解析配置文件
    char line[MAX_LINE_LENGTH];
    while (fgets(line, MAX_LINE_LENGTH, file)) {
        // 跳过注释行
        if (line[0] == '#' || line[0] == '\n' || line[0] == '\r') {
            continue;
        }

        // 去除行尾的换行符
        size_t len = strlen(line);
        if (len > 0 && line[len - 1] == '\n') {
            line[len - 1] = '\0';
        }
        if (len > 1 && line[len - 2] == '\r') {
            line[len - 2] = '\0';
        }

        // 解析配置项
        if (strstr(line, "item=") == line) {
            // 解析商品项
            if (config->item_count < MAX_ITEMS) {
                parse_item_line(line, &config->items[config->item_count]);
                config->item_count++;
            }
        } else {
            // 解析其他配置项
            char* key = NULL;
            char* value = NULL;
            parse_key_value(line, &key, &value);

            if (key && value) {
                if (strcmp(key, "window_size") == 0) {
                    free(config->window_size);
                    config->window_size = value;
                } else if (strcmp(key, "proxy") == 0) {
                    free(config->proxy);
                    config->proxy = value;
                } else if (strcmp(key, "driver_path") == 0) {
                    free(config->driver_path);
                    config->driver_path = value;
                } else if (strcmp(key, "username") == 0) {
                    free(config->username);
                    config->username = value;
                } else if (strcmp(key, "password") == 0) {
                    free(config->password);
                    config->password = value;
                } else {
                    free(value);
                }
                free(key);
            }
        }
    }

    fclose(file);
    return config;
}

// 清理配置资源
void config_cleanup(Config* config) {
    if (!config) return;

    free(config->window_size);
    free(config->proxy);
    free(config->driver_path);
    free(config->username);
    free(config->password);

    for (int i = 0; i < config->item_count; i++) {
        free(config->items[i].url);
    }
    free(config->items);
    free(config);
}