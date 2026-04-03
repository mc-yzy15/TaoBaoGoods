#ifndef CONFIG_H
#define CONFIG_H

typedef struct {
    char* url;
    int quantity;
} Item;

typedef struct {
    char* window_size;
    char* proxy;
    char* driver_path;
    char* username;
    char* password;
    Item* items;
    int item_count;
} Config;

Config* config_load(const char* file_path);
void config_cleanup(Config* config);
void config_create_default(const char* file_path);

#endif
