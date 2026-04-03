#include "config.h"

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 1024
#define MAX_ITEMS 100

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

static void trim_in_place(char* text) {
    char* start;
    char* end;
    size_t length;

    if (!text) {
        return;
    }

    start = text;
    while (*start && isspace((unsigned char)*start)) {
        start++;
    }

    if (start != text) {
        memmove(text, start, strlen(start) + 1);
    }

    length = strlen(text);
    if (length == 0) {
        return;
    }

    end = text + length - 1;
    while (end >= text && isspace((unsigned char)*end)) {
        *end = '\0';
        end--;
    }
}

static void assign_string(char** slot, const char* value) {
    char* copy = duplicate_string(value);
    if (!copy) {
        return;
    }

    free(*slot);
    *slot = copy;
}

static void parse_item_line(const char* raw_value, Item* item) {
    char buffer[MAX_LINE_LENGTH];
    char* separator;
    int quantity;

    if (!raw_value || !item) {
        return;
    }

    strncpy(buffer, raw_value, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';
    trim_in_place(buffer);

    separator = strrchr(buffer, ':');
    if (!separator) {
        item->url = duplicate_string(buffer);
        item->quantity = 1;
        return;
    }

    *separator = '\0';
    separator++;
    trim_in_place(buffer);
    trim_in_place(separator);

    quantity = atoi(separator);
    if (quantity <= 0) {
        quantity = 1;
    }

    item->url = duplicate_string(buffer);
    item->quantity = quantity;
}

void config_create_default(const char* file_path) {
    FILE* file = fopen(file_path, "w");
    if (!file) {
        printf("创建默认配置文件失败: %s\n", file_path);
        return;
    }

    fprintf(file, "# TaoBaoGoods C experimental helper configuration\n");
    fprintf(file, "window_size=1280,720\n");
    fprintf(file, "proxy=\n");
    fprintf(file, "driver_path=chromedriver.exe\n");
    fprintf(file, "username=your_username\n");
    fprintf(file, "password=your_password\n");
    fprintf(file, "item=https://example.com/item1:1\n");

    fclose(file);
    printf("默认配置文件已创建: %s\n", file_path);
}

Config* config_load(const char* file_path) {
    FILE* file = fopen(file_path, "r");
    Config* config;
    char line[MAX_LINE_LENGTH];

    if (!file) {
        printf("配置文件不存在，创建默认配置...\n");
        config_create_default(file_path);
        file = fopen(file_path, "r");
        if (!file) {
            printf("无法打开配置文件: %s\n", file_path);
            return NULL;
        }
    }

    config = (Config*)calloc(1, sizeof(Config));
    if (!config) {
        fclose(file);
        return NULL;
    }

    config->window_size = duplicate_string("1280,720");
    config->proxy = duplicate_string("");
    config->driver_path = duplicate_string("chromedriver.exe");
    config->username = duplicate_string("");
    config->password = duplicate_string("");
    config->items = (Item*)calloc(MAX_ITEMS, sizeof(Item));
    if (!config->items) {
        fclose(file);
        config_cleanup(config);
        return NULL;
    }

    while (fgets(line, sizeof(line), file)) {
        char* separator;
        char* key;
        char* value;

        trim_in_place(line);
        if (line[0] == '\0' || line[0] == '#') {
            continue;
        }

        separator = strchr(line, '=');
        if (!separator) {
            continue;
        }

        *separator = '\0';
        key = line;
        value = separator + 1;
        trim_in_place(key);
        trim_in_place(value);

        if (strcmp(key, "item") == 0) {
            if (config->item_count < MAX_ITEMS) {
                parse_item_line(value, &config->items[config->item_count]);
                if (config->items[config->item_count].url) {
                    config->item_count++;
                }
            }
            continue;
        }

        if (strcmp(key, "window_size") == 0) {
            assign_string(&config->window_size, value);
        } else if (strcmp(key, "proxy") == 0) {
            assign_string(&config->proxy, value);
        } else if (strcmp(key, "driver_path") == 0) {
            assign_string(&config->driver_path, value);
        } else if (strcmp(key, "username") == 0) {
            assign_string(&config->username, value);
        } else if (strcmp(key, "password") == 0) {
            assign_string(&config->password, value);
        }
    }

    fclose(file);
    return config;
}

void config_cleanup(Config* config) {
    int index;

    if (!config) {
        return;
    }

    free(config->window_size);
    free(config->proxy);
    free(config->driver_path);
    free(config->username);
    free(config->password);

    if (config->items) {
        for (index = 0; index < config->item_count; index++) {
            free(config->items[index].url);
        }
        free(config->items);
    }

    free(config);
}
