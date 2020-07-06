#include "demo.h"

#include <stdio.h>

#include "../bindings/bricklet_lcd_128x64.h"
#include "../bindings/bricklet_ptc_v2.h"

TF_LCD128x64 lcd;
TF_PTCV2 ptc;

uint8_t backlight = 100;
bool invert = false;

int8_t gui_tab;
bool tab_changed = true;
bool first_run_since_tab_change = false;

bool show_ptc_resistance = false;

void check(int rc, char *msg) {
    if (rc >= 0)
        return;
    tf_hal_log_error("Failed to %s: %d", msg, rc);
}

void gui_tab_handler(TF_LCD128x64 *lcd, int8_t index, void *user_data) {
    gui_tab = index;
    tab_changed = true;
}

void demo_setup(TF_HalContext *hal) {
  check(tf_lcd_128x64_create(&lcd, "HQ6", hal), "create lcd");
  check(tf_ptc_v2_create(&ptc, "J7d", hal), "create rgb");

  tf_lcd_128x64_remove_all_gui(&lcd);
  tf_lcd_128x64_set_gui_tab_configuration(&lcd, TF_LCD_128X64_CHANGE_TAB_ON_CLICK_AND_SWIPE, true);
  tf_lcd_128x64_set_gui_tab_text(&lcd, 0, "PTC");
  tf_lcd_128x64_set_gui_tab_text(&lcd, 1, "Setup");
  tf_lcd_128x64_set_gui_tab_selected_callback_configuration(&lcd, 10, true);
  tf_lcd_128x64_register_gui_tab_selected_callback(&lcd, gui_tab_handler, &gui_tab);
}

void button_handler(TF_LCD128x64 *device, uint8_t index, bool pressed, void *user_data) {
    if(!pressed)
        return;

    switch(index) {
        case 0:
            invert = !invert;
            break;
        case 1:
            if(backlight <= 90)
                backlight += 10;
            break;
        case 2:
            show_ptc_resistance = !show_ptc_resistance;
            break;
        case 3:
            if(backlight > 0)
                backlight -= 10;
            break;
    }
}

void draw_setup() {
    if(show_ptc_resistance)
        tf_lcd_128x64_set_gui_button(&lcd, 2, 0, 28, 60, 25, "Hide PTC\xEA");
    else
        tf_lcd_128x64_set_gui_button(&lcd, 2, 0, 28, 60, 25, "Show PTC\xEA");
    if(tab_changed) {
        tf_lcd_128x64_set_gui_button(&lcd, 0, 0, 0, 60, 25, "Invert");
        tf_lcd_128x64_set_gui_button(&lcd, 1, 128-60, 0, 60, 20, "BL +");
        tf_lcd_128x64_set_gui_button(&lcd, 3, 128-60, 33, 60, 20, "BL -");
        tf_lcd_128x64_register_gui_button_pressed_callback(&lcd, button_handler, NULL);
        tf_lcd_128x64_set_gui_button_pressed_callback_configuration(&lcd, 10, true);
    }
    char line[5] = {};
    snprintf(line, sizeof(line)/sizeof(line[0]), "%d%%  ", backlight);
    tf_lcd_128x64_write_line(&lcd, 3, 14, line);
}

void draw_ptc() {
    int32_t temperature;
    tf_ptc_v2_get_temperature(&ptc, &temperature);
    int32_t temp_degrees = temperature / 100;
    int32_t temp_centidegrees = temperature - temp_degrees * 100;

    char line_0[22] = {};
    snprintf(line_0, sizeof(line_0)/sizeof(line_0[0]), "Temperature %02i.%02i\xF8 ", (int8_t)temp_degrees, (int8_t)temp_centidegrees);
    check(tf_lcd_128x64_write_line(&lcd, 0, 0, line_0), "write line");

    if(show_ptc_resistance) {
        int32_t resistance;
        tf_ptc_v2_get_resistance(&ptc, &resistance);
        char line_1[22] = {};
        snprintf(line_1, sizeof(line_1)/sizeof(line_1[0]), "Resistance %d\xEA", resistance);
        check(tf_lcd_128x64_write_line(&lcd, 2, 0, line_1), "write line");
    }
}

void demo_loop(TF_HalContext *hal) {
  if(tab_changed) {
      first_run_since_tab_change = true;
  }
  uint32_t start = tf_hal_current_time_us(hal);

  if(tab_changed && first_run_since_tab_change) {
    tf_lcd_128x64_clear_display(&lcd);
    tf_lcd_128x64_remove_gui_button(&lcd, 0);
    tf_lcd_128x64_remove_gui_button(&lcd, 1);
    tf_lcd_128x64_remove_gui_button(&lcd, 2);
    tf_lcd_128x64_remove_gui_button(&lcd, 3);
  }

  switch(gui_tab) {
      case 0:
      draw_ptc();
      break;
    case 1:
      draw_setup();
      break;
  }

  tf_lcd_128x64_set_display_configuration(&lcd, 14, backlight, invert, true);

  // If callbacks on the Raspberry Pi only work sporadically, use 1000 µs timeout here.
  tf_lcd_128x64_callback_tick(&lcd, 250);
  tf_ptc_v2_callback_tick(&ptc, 250);

  while(tf_hal_current_time_us(hal) - start < 50000) {
    tf_lcd_128x64_callback_tick(&lcd, 250);
    tf_ptc_v2_callback_tick(&ptc, 250);
  }
  if(first_run_since_tab_change)
    tab_changed = false;
  first_run_since_tab_change = false;
}

