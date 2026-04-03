#ifndef UI_H
#define UI_H

extern void* g_ui_window;

void init_ui(void);
void cleanup_ui(void);
void update_ui_status(const char* message);
void show_error(const char* title, const char* message);
void show_info(const char* title, const char* message);

#endif
